JPA 사용시 주의점에 대해 정리한 글 입니다.

---

### @Transactional 묶음 처리는 의도대로 작동하지 않을 수 있다.

#### 문제

동일한 Bean 내 @Transactional 부여된 메소드에서 다른 @Transactional 메소드를 호출했을 때, 트랜잭션이 묶이지 않는 문제

#### 해결

각 메소드를 별도의 Bean으로 분리한 뒤 호출하기

#### 참고
- https://cheese10yun.github.io/spring-transacion-same-bean/

---

### @ID의 IDENTITY 방식은 bulk가 안된다.

#### 문제

Entity의 Id 생성 전략이 IDENTITY인 경우, saveAll() 메소드로 Bulk Insert를 시도해도, 하이버네이트 내부적으로 삽입 1건당 하나의 트랜잭션으로 작동하는 문제

#### 해결

JDBC 등을 이용해 우회해야한다. 

#### 참고

https://homoefficio.github.io/2020/01/25/Spring-Data%EC%97%90%EC%84%9C-Batch-Insert-%EC%B5%9C%EC%A0%81%ED%99%94/


---

