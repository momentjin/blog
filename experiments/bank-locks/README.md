# Bank concurrency experiment

This project backs the Korean concurrency-control blog draft. It is a teaching experiment, not a banking service.

## Stack

- MySQL 8.0.44, Redis 7.4.7
- Spring Boot 4.1.1, Kotlin 2.3.21, Java 21, Gradle 9.7.1
- Two application containers sharing one MySQL and one Redis
- Host ports: applications 8081/8082, MySQL 3307, Redis 6380

## Run

From this directory:

~~~sh
docker-compose up -d --build
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run_benchmark.py
.venv/bin/python write_skew_demo.py
.venv/bin/python plot_results.py
~~~

The benchmark saves all three measured rounds in [results/benchmark.json](results/benchmark.json). The write-skew script prints its result; the captured run is [results/write-skew.json](results/write-skew.json). Charts are written to the repository's `assets/concurrency-control-01` directory. On Linux, install a Korean font (for example Noto Sans CJK) before plotting.

The client starts 1,000 HTTP requests together, alternating between the two application instances. Server threads and connection pools naturally queue some work. The benchmark resets account 1 before each round to 10,000,000,000 KRW and sends 1,000 distinct 10,000,000 KRW withdrawals. It warms each mode with 50 requests and then runs three measured rounds. Outcomes are checked against the sum of withdrawal records, not only HTTP status codes.

The deliberately unsafe mode sleeps 100 ms after reading. Optimistic mode sleeps 20 ms on its first attempt, and pessimistic and Redis modes sleep 2 ms in their critical sections. Atomic mode has no artificial delay. These figures make races easy to see; they do not support a general speed ranking. The optimistic implementation has a 100-attempt limit, and its exhausted attempts return HTTP 409. Redis lock expiration is 30 seconds; the benchmark exercises normal completion, not expired-lock recovery or failover.

The schema uses a unique request ID to distinguish requests, but the API does not implement an idempotent response for duplicate IDs. Do not use this code for real money movement.

To stop:

~~~sh
docker-compose down
~~~
