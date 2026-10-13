package dev.momentjin.banklocks

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
class BankLocksApplication

fun main(args: Array<String>) {
	runApplication<BankLocksApplication>(*args)
}
