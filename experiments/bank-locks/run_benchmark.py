#!/usr/bin/env python3
"""Send 1,000 concurrent HTTP withdrawals across two Spring Boot processes."""

import asyncio
import json
import statistics
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import aiohttp

HOSTS = ["http://localhost:8081", "http://localhost:8082"]
MODES = ["naive", "atomic", "optimistic", "pessimistic", "redis"]
REQUESTS = 1000
AMOUNT = 10_000_000
INITIAL_BALANCE = 10_000_000_000
REPEATS = 3


def percentile(values, percentage):
    values = sorted(values)
    index = (len(values) - 1) * percentage / 100
    low, high = int(index), min(int(index) + 1, len(values) - 1)
    return values[low] + (values[high] - values[low]) * (index - low)


async def api(session, method, url, body=None):
    async with session.request(method, url, json=body) as response:
        data = await response.json()
        return response.status, data


async def run(session, mode, round_number, requests=REQUESTS):
    status, _ = await api(session, "POST", HOSTS[0] + "/api/reset", {})
    assert status == 200, status
    start = asyncio.Event()

    async def request(index):
        await start.wait()
        started = time.perf_counter()
        try:
            status, result = await api(
                session,
                "POST",
                HOSTS[index % 2] + "/api/withdraw/" + mode,
                {"requestId": str(uuid.uuid4()), "amount": AMOUNT},
            )
            return {"latency_ms": (time.perf_counter() - started) * 1000, "http_status": status, **result}
        except Exception as exc:
            return {"latency_ms": (time.perf_counter() - started) * 1000, "http_status": 0, "error": repr(exc)}

    tasks = [asyncio.create_task(request(index)) for index in range(requests)]
    await asyncio.sleep(0.1)
    begun = time.perf_counter()
    start.set()
    results = await asyncio.gather(*tasks)
    elapsed = (time.perf_counter() - begun) * 1000
    status, state = await api(session, "GET", HOSTS[0] + "/api/state")
    assert status == 200, status
    latencies = [r["latency_ms"] for r in results]
    errors = [r for r in results if r["http_status"] != 200]
    return {
        "mode": mode,
        "round": round_number,
        "requests": requests,
        "elapsed_ms": round(elapsed, 1),
        "p50_ms": round(percentile(latencies, 50), 1),
        "p95_ms": round(percentile(latencies, 95), 1),
        "success": sum(r.get("success", False) for r in results),
        "http_errors": len(errors),
        "error_samples": errors[:3],
        "retries": sum(r.get("retries", 0) for r in results),
        "state": state,
        "consistent": state["balance"] == INITIAL_BALANCE - state["withdrawnAmount"],
    }


async def main():
    output = Path(__file__).parent / "results"
    output.mkdir(exist_ok=True)
    timeout = aiohttp.ClientTimeout(total=180)
    connector = aiohttp.TCPConnector(limit=1200, limit_per_host=0)
    runs = []
    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        for mode in MODES:
            warmup = await run(session, mode, 0, requests=50)
            print("warmup", json.dumps(warmup, ensure_ascii=False), flush=True)
            for round_number in range(1, REPEATS + 1):
                result = await run(session, mode, round_number)
                runs.append(result)
                print("measured", json.dumps(result, ensure_ascii=False), flush=True)
    summary = {}
    for mode in MODES:
        subset = [run for run in runs if run["mode"] == mode]
        summary[mode] = {
            "median_elapsed_ms": round(statistics.median(run["elapsed_ms"] for run in subset), 1),
            "median_p95_ms": round(statistics.median(run["p95_ms"] for run in subset), 1),
            "median_retries": statistics.median(run["retries"] for run in subset),
            "consistent_rounds": sum(run["consistent"] for run in subset),
            "median_final_balance": statistics.median(run["state"]["balance"] for run in subset),
            "median_recorded_withdrawals": statistics.median(run["state"]["withdrawnAmount"] for run in subset),
            "median_http_errors": statistics.median(run["http_errors"] for run in subset),
        }
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "settings": {"hosts": HOSTS, "requests": REQUESTS, "amount": AMOUNT, "initial_balance": INITIAL_BALANCE, "repeats": REPEATS},
        "runs": runs,
        "summary": summary,
    }
    (output / "benchmark.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print("summary", json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    asyncio.run(main())
