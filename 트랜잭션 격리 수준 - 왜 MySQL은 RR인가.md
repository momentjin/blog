>아주 예전에 트랜잭션 격리 수준에 대해서 알아보다가, DB마다 기본값이 다르다는 점을 깨달은 적이 있었습니다. MySQL의 InnoDB는 REPEATABLE READ(RR)를 기본값으로 사용하지만, Oracle과 PostgreSQL은 READ COMMITTED(RC)를 기본값으로 사용합니다. 같은 SQL 표준을 따르는 관계형 데이터베이스인데 왜 기본값은 다른지 궁금했었는데, 이번 기회에 이 궁금증을 다뤄보고자 합니다.

이번 글에서는 공식 문서와 개발자 기록을 바탕으로 각 DB가 서로 다른 기본값을 사용하게 된 배경을 살펴본다. MySQL에 대한 설명은 InnoDB를 기준으로 한다.

## MySQL과 Oracle, PostgreSQL은 왜 기본값이 다를까?

| DB | 기본 격리 수준 |
| --- | --- |
| MySQL InnoDB | REPEATABLE READ |
| Oracle | READ COMMITTED |
| PostgreSQL | READ COMMITTED |

기본값이 다르다는 사실만으로는 각 DB가 어떤 기준으로 선택했는지 알 수 없다. Oracle과 PostgreSQL이 RC를 기본으로 사용하는 이유를 먼저 살펴보고, MySQL의 선택에는 어떤 배경이 있었는지 이어서 알아보자.

### Oracle과 PostgreSQL: 많은 처리에서 트랜잭션 전체의 읽기 시점을 고정할 필요가 없다

Oracle과 PostgreSQL의 문서는 RC가 많은 애플리케이션에 적절하다고 설명한다. 그렇다면 어떤 요구사항을 RC만으로 충족할 수 있다는 뜻일까?

> “is appropriate for most applications.” — [Oracle 공식 문서: Using Serializable Transactions for Concurrency Control](https://docs.oracle.com/en/database/oracle/oracle-database/26/adfns/sql-processing-for-application-developers.html)

> “adequate for many applications” — [PostgreSQL 공식 문서: Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html)

먼저 주문 상세 화면처럼 주문과 주문 항목을 하나의 `SELECT`로 조회하는 경우를 생각해보자. 필요한 것은 그 조회가 일관된 시점의 결과를 반환하는 것이다. Oracle과 PostgreSQL은 RC에서도 이 요구를 충족한다. 조회 도중 다른 트랜잭션이 주문과 주문 항목을 함께 변경하고 커밋하더라도, 변경 전 주문과 변경 후 주문 항목을 섞어 읽지 않는다. 다음 조회까지 이전 결과를 유지해야 한다는 요구가 없다면, 트랜잭션 전체의 읽기 시점을 고정할 필요가 없다.

> “all rows that a query reads must be committed before the query begins.” — [Oracle 공식 문서: Transaction Set Consistency Differences](https://docs.oracle.com/en/database/oracle/oracle-database/26/adfns/sql-processing-for-application-developers.html)

갱신도 어떤 조건을 지켜야 하는지에 따라 RC로 처리할 수 있다. 예를 들어 상품 한 개를 구매할 때 재고를 음수로 만들지 않는 것이 요구사항이라면, 재고 확인과 차감을 하나의 SQL로 묶을 수 있다.

```sql
UPDATE product
SET stock = stock - 1
WHERE id = 1 AND stock >= 1;
```

재고가 1개인 상품에 두 구매 요청이 동시에 들어오면, 먼저 갱신한 트랜잭션이 해당 행을 잠근다. 다른 트랜잭션은 기다렸다가 앞선 변경이 커밋되면 재고 조건을 다시 확인한다. 재고가 이미 0개이므로 두 번째 요청은 행을 변경하지 못한다. 애플리케이션은 변경된 행이 1개인지 확인해 재고 확보 성공 여부를 판단한다. 이 경우에는 별도로 조회한 과거 재고를 계속 유지할 필요 없이, 갱신할 때 해당 행의 조건을 검사하면 요구사항을 충족할 수 있다.

PostgreSQL 문서도 미리 정해진 계좌 행의 잔액을 갱신하는 이체 예시를 들어, 이런 처리에서는 변경된 행을 기준으로 갱신하는 것이 적절하다고 설명한다.

> “each command is affecting only a predetermined row” — [PostgreSQL 공식 문서: Read Committed Isolation Level](https://www.postgresql.org/docs/18/transaction-iso.html)

이처럼 한 번의 조회 결과가 일관되면 되는 처리나, 갱신 대상 행의 조건을 SQL 안에서 검사할 수 있는 처리에서는 RC로도 필요한 보장을 얻을 수 있다.

### 여러 번의 조회 결과에 대한 일관성이 필요하다면?

그렇다면 한 번의 조회로 결과를 만들 수 없는 경우는 어떨까? 주문 보고서를 만들면서 주문 총액을 먼저 조회하고, 대량의 주문 항목은 여러 SQL로 나눠 조회한다고 해보자. 보고서의 총액과 항목별 금액의 합계는 서로 맞아야 한다. 다른 트랜잭션이 주문을 수정할 때도 총액과 주문 항목을 같은 트랜잭션에서 함께 변경한다고 가정한다.

| 순서 | 트랜잭션 A: 보고서 생성 | 트랜잭션 B: 주문 수정 |
| --- | --- | --- |
| 1 | 주문 총액 10만 원을 조회한다. | |
| 2 | | 2만 원짜리 항목을 추가하고 총액을 12만 원으로 변경한 뒤 커밋한다. |
| 3 | 주문 항목을 조회한다. 추가된 항목까지 포함해 합계가 12만 원이다. | |

RC에서는 A를 하나의 트랜잭션으로 묶어도 **보고서의 총액은 10만 원인데 항목의 합계는 12만 원인 결과**가 나올 수 있다. B는 총액과 항목을 함께 커밋했지만, A가 두 조회에서 서로 다른 시점의 데이터를 읽었기 때문이다. 각 조회 결과가 올바르다는 것만으로 이 보고서의 요구사항을 충족하지는 못한다.
> “two successive SELECT commands can see different data” — [PostgreSQL 공식 문서: Read Committed Isolation Level](https://www.postgresql.org/docs/18/transaction-iso.html)

이런 경우에는 조회들을 하나의 SQL로 합칠 수 있는지 검토하거나, 여러 조회가 같은 스냅샷을 사용하도록 해야 한다. 여러 SQL을 유지하면서 보고서의 읽기 시점을 고정하려면 PostgreSQL에서는 RR을, Oracle에서는 READ ONLY 트랜잭션을 사용할 수 있다. **여러 번 조회한다는 사실보다, 그 결과들이 반드시 같은 시점의 상태를 나타내야 하는지가 기준**이다. 따라서 RC가 많은 처리에 충분하더라도, 이런 요구가 있는 트랜잭션에는 추가 보장이 필요하다.

### MySQL: 잠금을 줄이는 선택이 과거 복제 방식의 정확성에 영향을 주었다

그렇다면 MySQL도 RC를 기본값으로 사용하면 되지 않았을까? 라는 합리적 의문이 든다. MySQL에는 과거 기본 복제 방식과의 호환성이라는 제약이 있었다. 여기서 원본 DB(source, 기존의 master)는 애플리케이션의 변경 요청을 처리하고 복제할 내용을 보내는 DB이고, 복제 DB(replica)는 그 내용을 전달받아 반영하는 DB다. SQL문 기반 복제는 원본 DB에서 실행한 SQL을 기록하고 복제 DB에서도 실행하는 방식이다. 트랜잭션의 변경 SQL은 커밋할 때 바이너리 로그에 기록된다. 원본 DB에서는 서로 다른 n개의 트랜잭션이 겹쳐 실행되더라도 복제 DB에서는 로그에 기록된 순서로 다시 실행되므로, 두 실행 방식이 같은 결과를 내야 한다.
> “Prior to MySQL 5.7.7, statement-based format was the default.” — [MySQL 공식 문서: Replication Formats](https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-formats.html)

문제는 **원본 DB에서 동시에 실행한 SQL과 복제 DB에서 순서대로 다시 실행한 SQL이 서로 다른 행을 변경할 수 있다는 것**이다. 2006년 MySQL 버그 중에 RC에서 일부 잠금을 생략하면 이런 불일치가 발생한다는 재현 사례와 개발자의 설명이 남아 있다.
> “InnoDB skips some locking which is needed to make mixed or statement-based binlogging work.” — [MySQL 버그 #23051: READ COMMITTED breaks mixed and statement-based replication](https://bugs.mysql.com/bug.php?id=23051)

이를 주문 처리 예시로 바꿔보자. 처음에는 주문 1만 처리 대기 상태인 `READY`이고 주문 2는 보류 상태인 `HOLD`다. 두 주문 모두 `processed = 0`이며, `status`에는 인덱스가 없어 아래 갱신이 두 행을 모두 스캔한다고 가정한다.

| 순서 | 트랜잭션 A: 대기 주문 처리 | 트랜잭션 B: 보류 해제 |
| --- | --- | --- |
| 1 | `UPDATE orders SET processed = 1 WHERE status = 'READY'`를 실행한다. 주문 1만 변경하고 아직 커밋하지 않는다. | |
| 2 | | 주문 2의 상태를 `READY`로 바꾸고 커밋한다. |
| 3 | 커밋한다. | |

RC에서는 A가 조건에 맞지 않는 주문 2의 잠금을 해제하므로 B가 먼저 커밋할 수 있다. 원본 DB에서는 A가 주문 2를 검사할 때 `HOLD`였으므로 주문 2는 처리되지 않는다. 하지만 로그에는 먼저 커밋한 B의 SQL이 A보다 앞에 기록된다. 복제 DB에서 B를 실행하면 두 주문 모두 `READY`가 되고, 이어 A를 실행하면 두 주문 모두 처리된다. **원본 DB에서는 주문 1만 처리했는데 복제 DB에서는 주문 2까지 처리한 결과가 된다.**

이 실행 순서를 막는 것이 잠금이다. InnoDB의 RR에서는 이 예시의 A가 스캔한 주문 2의 잠금을 유지하므로 B가 기다린다. A가 먼저 커밋하고 B가 그 뒤에 실행되면 로그를 순서대로 재실행해도 같은 결과를 얻을 수 있다. MySQL 공식 문서도 RR과 RC에서 조건에 맞지 않는 행의 잠금을 유지하는 방식이 달라진다고 설명한다.
> “Record locks for nonmatching rows are released after MySQL has evaluated the WHERE condition.” — [MySQL 공식 문서: InnoDB Locking](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html)

즉, MySQL 5.1에서는 **SQL 문 기반 복제를 유지한 채 RC로 잠금을 줄일 수 없었다. RC를 사용하려면 행 기반 복제로 바꿔야 했다.**

### 현재도 복제 때문에 RR을 사용해야 할까?

행 기반 복제는 SQL을 다시 실행하는 대신 실제로 바뀐 행의 결과를 전달한다. 앞의 예시에서도 A가 주문 1만 변경했다는 결과를 전달하므로, 복제 DB가 A의 검색 조건을 다시 평가해 주문 2까지 처리하는 문제가 생기지 않는다. MySQL은 5.7.7부터 행 기반 로깅을 기본으로 사용한다.
> “Only row-based binary logging is supported with the READ COMMITTED isolation level.” — [MySQL 공식 문서: Transaction Isolation Levels](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html)

현재 MySQL의 기본 로깅 방식인 행 기반 로깅에서는 RC를 사용할 수 있다. 따라서 과거의 복제 제약이 현재 모든 MySQL 트랜잭션에 RR이 필요하다는 의미는 아니다. 기본값을 RC로 바꾸면 기존 애플리케이션의 반복 조회 결과와 잠금 동작이 달라지는 호환성 비용도 있다. 다만 확인한 자료에는 이 비용이 현재 RR 기본값을 유지하는 공식적인 결정 사유라고 명시되어 있지는 않다.

## 정리

격리 수준을 선택할 때 중요한 기준은 **다른 트랜잭션이 동시에 데이터를 변경하더라도, 지금 처리하는 요청에서 어떤 조건이 유지되어야 하는가** 라고 생각한다. 주문 상세를 한 번의 조회로 읽거나, 재고 조건 확인과 차감을 SQL 하나로 처리하는 예시에서는 RC로도 필요한 보장을 얻을 수 있다. 이런 요구사항을 충족한다면 RC를 사용하는 데 문제가 없다.

반면 주문 보고서처럼 여러 번 조회한 결과가 모두 같은 시점의 데이터를 나타내야 한다면, RC의 조회별 일관성만으로는 부족하다. 이때는 필요한 트랜잭션에 같은 스냅샷을 유지하는 설정을 적용할 수 있다. MySQL InnoDB와 PostgreSQL에서는 RR을, Oracle의 조회 전용 처리에서는 READ ONLY 트랜잭션을 선택할 수 있다. **RC를 기본으로 사용하면서, 더 강한 보장이 필요한 트랜잭션에만 별도의 격리 수준을 적용하는 방식도 가능하다.**

또한 격리 수준은 일반 조회의 스냅샷뿐 아니라 갱신 과정의 잠금에도 영향을 준다. MySQL에서 RC와 RR이 조건에 맞지 않는 행의 잠금을 다르게 관리했던 것처럼, 실제 동작은 사용하는 DB와 SQL의 검색 조건까지 함께 확인해야 한다. 애플리케이션에서는 각 트랜잭션에 필요한 보장을 기준으로 적절한 격리수준을 선택할 수 있어야 한다.
