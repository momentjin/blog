package dev.momentjin.banklocks

import org.springframework.data.redis.core.StringRedisTemplate
import org.springframework.data.redis.core.script.DefaultRedisScript
import org.springframework.http.HttpStatus
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.transaction.support.TransactionTemplate
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.server.ResponseStatusException
import java.time.Duration
import java.util.UUID

data class WithdrawalRequest(val requestId: String, val amount: Long)
data class WithdrawalResult(val success: Boolean, val retries: Int)
data class AccountState(val balance: Long, val version: Long, val withdrawals: Long, val withdrawnAmount: Long)
private data class Snapshot(val balance: Long, val version: Long)

@RestController
@RequestMapping("/api")
class WithdrawalController(
    private val jdbc: JdbcTemplate,
    private val tx: TransactionTemplate,
    private val redis: StringRedisTemplate,
) {
    private val initialBalance = 10_000_000_000L
    private val releaseScript = DefaultRedisScript<Long>().apply {
        setScriptText("if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end")
        resultType = Long::class.java
    }

    @PostMapping("/reset")
    fun reset(): AccountState {
        tx.executeWithoutResult {
            jdbc.update("DELETE FROM withdrawal")
            jdbc.update("INSERT INTO account(id,balance,version) VALUES (1,?,0) ON DUPLICATE KEY UPDATE balance=VALUES(balance),version=0", initialBalance)
        }
        return state()
    }

    @GetMapping("/state")
    fun state(): AccountState = jdbc.queryForObject(
        """SELECT a.balance, a.version, COUNT(w.request_id) AS withdrawals,
                  COALESCE(SUM(w.amount),0) AS withdrawn_amount
           FROM account a LEFT JOIN withdrawal w ON w.account_id=a.id WHERE a.id=1
           GROUP BY a.id, a.balance, a.version""".trimIndent(),
        { rs, _ -> AccountState(rs.getLong("balance"), rs.getLong("version"), rs.getLong("withdrawals"), rs.getLong("withdrawn_amount")) }
    )!!

    @PostMapping("/withdraw/{mode}")
    fun withdraw(@PathVariable mode: String, @RequestBody request: WithdrawalRequest): WithdrawalResult {
        if (request.amount <= 0 || request.requestId.isBlank()) throw ResponseStatusException(HttpStatus.BAD_REQUEST)
        return when (mode) {
            "naive" -> naive(request)
            "atomic" -> atomic(request)
            "optimistic" -> optimistic(request)
            "pessimistic" -> pessimistic(request)
            "redis" -> redisLock(request)
            else -> throw ResponseStatusException(HttpStatus.BAD_REQUEST, "unknown mode")
        }
    }

    private fun snapshot(lock: Boolean = false): Snapshot = jdbc.queryForObject(
        "SELECT balance,version FROM account WHERE id=1" + if (lock) " FOR UPDATE" else "",
        { rs, _ -> Snapshot(rs.getLong(1), rs.getLong(2)) }
    )!!

    private fun record(request: WithdrawalRequest) {
        jdbc.update("INSERT INTO withdrawal(request_id,account_id,amount) VALUES (?,1,?)", request.requestId, request.amount)
    }

    // Deliberately unsafe control: all contenders can read the same old balance.
    private fun naive(request: WithdrawalRequest): WithdrawalResult = tx.execute {
        val current = snapshot()
        if (current.balance < request.amount) return@execute WithdrawalResult(false, 0)
        Thread.sleep(100)
        jdbc.update("UPDATE account SET balance=?,version=version+1 WHERE id=1", current.balance - request.amount)
        record(request)
        WithdrawalResult(true, 0)
    }!!

    private fun atomic(request: WithdrawalRequest): WithdrawalResult = tx.execute {
        val changed = jdbc.update(
            "UPDATE account SET balance=balance-?,version=version+1 WHERE id=1 AND balance>=?",
            request.amount, request.amount
        )
        if (changed == 0) return@execute WithdrawalResult(false, 0)
        record(request)
        WithdrawalResult(true, 0)
    }!!

    private fun optimistic(request: WithdrawalRequest): WithdrawalResult {
        for (attempt in 0..99) {
            val result = tx.execute {
                val current = snapshot()
                if (current.balance < request.amount) return@execute WithdrawalResult(false, attempt)
                if (attempt == 0) Thread.sleep(20)
                val changed = jdbc.update(
                    "UPDATE account SET balance=balance-?,version=version+1 WHERE id=1 AND version=? AND balance>=?",
                    request.amount, current.version, request.amount
                )
                if (changed == 0) return@execute null
                record(request)
                WithdrawalResult(true, attempt)
            }
            if (result != null) return result
            Thread.sleep((1..10).random().toLong())
        }
        throw ResponseStatusException(HttpStatus.CONFLICT, "retry limit")
    }

    private fun pessimistic(request: WithdrawalRequest): WithdrawalResult = tx.execute {
        val current = snapshot(lock = true)
        if (current.balance < request.amount) return@execute WithdrawalResult(false, 0)
        Thread.sleep(2)
        jdbc.update("UPDATE account SET balance=balance-?,version=version+1 WHERE id=1", request.amount)
        record(request)
        WithdrawalResult(true, 0)
    }!!

    private fun redisLock(request: WithdrawalRequest): WithdrawalResult {
        val key = "lock:account:1"
        val token = UUID.randomUUID().toString()
        var waits = 0
        val deadline = System.nanoTime() + Duration.ofSeconds(60).toNanos()
        while (redis.opsForValue().setIfAbsent(key, token, Duration.ofSeconds(30)) != true) {
            if (System.nanoTime() > deadline) throw ResponseStatusException(HttpStatus.CONFLICT, "lock timeout")
            waits++
            Thread.sleep((2..8).random().toLong())
        }
        try {
            return tx.execute {
                val current = snapshot()
                if (current.balance < request.amount) return@execute WithdrawalResult(false, waits)
                Thread.sleep(2)
                jdbc.update("UPDATE account SET balance=balance-?,version=version+1 WHERE id=1", request.amount)
                record(request)
                WithdrawalResult(true, waits)
            }!!
        } finally {
            redis.execute(releaseScript, listOf(key), token)
        }
    }
}
