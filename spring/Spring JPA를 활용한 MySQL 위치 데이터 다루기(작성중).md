# Spring JPA를 활용한 MySQL 위치 데이터 다루기

> 부제: 반경 'n' KM 이내 포함되는 모든 데이터 찾기

## 개요

특정 위치(x,y)로 부터 n KM 떨어진 데이터를 찾아야 합니다. 현재는 매번 Table Full Scan해서 데이터를 필터링하고 조회하기 때문에 성능이 매우 나쁩니다. 이 문제를 해결한 경험을 공유하고자 이 글을 작성했습니다.

## 용어 정리

MySQL 5.7부터 공간 데이터 타입을 지원합니다. 이것을 활용해 위치 데이터를 인덱싱할 수 있습니다. 알아두어야 할 용어부터 정리하고 넘어가겠습니다.

**MBR** 
- Minimum Bounding Rectangles의 약자로, 최소 경계 사각형이라는 뜻 입니다. 
- 지도 상의 임의의 사각형 구역이라고 생각하시면 됩니다.
- 공간 관련 연산시 사용하는 용어입니다.

**POINT**(longitude, latitude) // 여기에 링크 추가하기 (document
- 지도 상의 경도, 위도 값을 표현하는 객체입니다.
- MySQL의 Spatial Data Type 중 하나입니다.
 
**LINESTRING**(POINT1, POINT2) // 여기에 링크 추가하기 (document
- 지도 상의 하나의 선을 의미하며, 일련의 Point들로 이루어진 객체입니다.
- MySQL의 Spatial Data Type 중 하나입니다.

## Practice In DBMS

먼저 DB를 활용해서 실습해보겠습니다. 우선 최종적인 쿼리의 형태는 다음과 같습니다. 이 쿼리는 기준 좌표 x,y로 부터 nKM 떨어진 모든 범위의 gym_location 데이터를 조회하는 쿼리입니다.

```sql

# 기준 좌표 : x,y
# 기준 좌표의 북동쪽으로 nKM에 위치한 좌표 : x1, y1
# 기준 좌표의 남서쪽으로 nKM에 위치한 좌표 : x2, y2
# // 최소값 표기해야됌

SELECT *
FROM gym_location as g
WHERE MBRCONTAINS(ST_LINESTRINGFROMTEXT('LINESTRING(x1 y1, x2 y2)'), g.location);
```

워 쿼리에 대해 구체적으로 알아보겠습니다.
// 여기에 링크 추가하기 (document
- ST_LINESTRINGFROMTEXT : 

## Practice In Spring Boot + JPA

이번에는 Spring Boot, JPA 환경에서 실습해보겠습니다. 

### 개발 환경

- Spring Boot 2.x, 
- Hibernate 5.x, 
- MySQL 5.7
- Gradle

### Install Library

먼저 필요한 라이브러리에 대한 의존성을 추가해야 합니다. 필요한 라이브러리는 [hibernate-spatial](https://mvnrepository.com/artifact/org.hibernate/hibernate-spatial)입니다. 저는 Gradle을 사용하므로 아래와 같이 build.gradle 파일에 의존성을 추가했습니다.

```kotlin
dependencies {
    ...
    compile group: 'org.hibernate', name: 'hibernate-spatial', version: '5.4.4.Final'
}
```

### Practice



// 아래는 임시 기록

MBRContains(g1, g2)
: Returns 1 or 0 to indicate whether the minimum bounding rectangle of g1 contains the minimum bounding rectangle of g2.

A Point is a geometry that represents a single location in coordinate space.