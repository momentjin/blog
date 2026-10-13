#!/usr/bin/env python3
"""Demonstrate a cross-row invariant violation under MySQL REPEATABLE READ."""

import json
import threading

import mysql.connector

CONFIG = {"host": "127.0.0.1", "port": 3307, "user": "bank", "password": "bank", "database": "bank"}
barrier = threading.Barrier(2)
observed = {}


def connection():
    return mysql.connector.connect(**CONFIG)


with connection() as db:
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM account WHERE id IN (2,3)")
        cursor.execute("INSERT INTO account(id,balance,version) VALUES (2,10000000,0),(3,10000000,0)")
    db.commit()


def withdraw(account_id):
    db = connection()
    try:
        db.start_transaction(isolation_level="REPEATABLE READ")
        with db.cursor() as cursor:
            cursor.execute("SELECT SUM(balance) FROM account WHERE id IN (2,3)")
            total = int(cursor.fetchone()[0])
            observed[str(account_id)] = {"total_seen": total}
            barrier.wait(timeout=10)
            if total - 10_000_000 >= 10_000_000:
                cursor.execute("UPDATE account SET balance=balance-10000000 WHERE id=%s", (account_id,))
                observed[str(account_id)]["accepted"] = True
            else:
                observed[str(account_id)]["accepted"] = False
        db.commit()
    finally:
        db.close()


threads = [threading.Thread(target=withdraw, args=(account_id,)) for account_id in (2, 3)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

with connection() as db:
    with db.cursor() as cursor:
        cursor.execute("SELECT id,balance FROM account WHERE id IN (2,3) ORDER BY id")
        final = {str(account_id): balance for account_id, balance in cursor.fetchall()}

result = {"minimum_total": 10_000_000, "transactions": observed, "final_balances": final, "final_total": sum(final.values())}
assert all(item["accepted"] for item in observed.values())
assert result["final_total"] < result["minimum_total"]
print(json.dumps(result, ensure_ascii=False, indent=2))
