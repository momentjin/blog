# Java 8 in Action
> 한빛미디어, 라울-게이브리얼 우르마 / 마리오 푸스코 / 앨런 마이크로프트 지음, 우정은 옮김

#### 책을 읽은 동기
Java 8이 릴리즈된지 벌써 4~5년이 지났지만, Java 8에 제대로 알고 있는 지식이 하나도 없었습니다. 이 책을 읽고 Java 8의 탄생 배경, 추가된 API, 주의점을 중점적으로 간단히 학습해보고자 합니다.


---------


### 기존 Java는 데이터를 병렬로 처리하기 어려웠다.
기존 Java는 데이터를 병렬로 처리하려면 먼저 분할하고 분할된 각 데이터의 처리를 각각의 쓰레드로 할당해서 결과를 합쳐야 한다. 이런 일련의 과정을 기존 Java7에서는 Fork/Join Framework를 이용해서 구현했다. 하지만 Java8에서는 병렬 스트림(Parallel Stream)을 이용해서 훨씬 쉽게 구현할 수 있다.

하지만 쉽게 구현할 수 있다는 것이 곧 올바르게 사용한다는 말과 같지 않음을 알아야 한다. 병렬스트림은 코어간 데이터 교환 + 스트림의 분할 등의 추가적인 비용이 따른다. 즉, 올바르게 사용하지 못하면 오히려 배보다 배꼽이 더 큰 상황이 있을 수 있다.

### 기존 Java는 보일러 플레이트 코드가 너무 많았다.
Java의 익명클래스를 이용하는 경우, 보일러플레이트 코드가 너무 많았다. Collections.sort()의 정렬 전략을 구현해본 사람은 다들 알 것이다. Java 8에서는 함수를 일급객체로 사용하기 때문에 람다 또는 메소드 레퍼런스 등을 활용하면 불필요한 코드 없이 간결한 코드를 작성할 수 있다.
```java
// 보일러 플레이트 코드가 많은 Java 코드
Arrays.asList(1, 2, 3, 4).sort(new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return Integer.compare(o1, o2);
    }
});

// 개선된 Java 코드
Arrays.asList(1, 2, 3, 4).sort(Integer::compare);
```

### 기존 Java는 모두 명령형으로 코드를 작성했다.
컬렉션에서 특정 조건에 부합하는 원소들을 추출하고, 추출된 원소들의 ID를 List로 재구성하고자 할 때 기존의 Java는 다음과 같은 코드를 작성했다.
```java
List<String> result = new ArrayList<>();

for (Item item : result) {
    if (!test(item)) continue;
    result.add(item.ID);
}
```

Java 8에서는 Stream을 이용하면 `선언형`으로 명시적으로 표현이 가능하다. 컬렉션을 이용한 로직의 경우 `어떻게`를 기술한다. 반면 스트림은 `무엇을` 해야 하는지 기술한다.
```java
List<String> result = 
    items.stream()
        .filter(item -> test(item))
        .map(item -> item.ID)
        .collect(Collectors.toList());
```

### Stream 잘 알고 쓰자
확신이 없을 땐, 반드시 성능 측정을 하자!!

for 루프는 언박싱/박싱을 수행하지 않는다. 반면, 스트림은 언박싱/박싱을 사용하는 경우가 있다. 이러한 경우 당연히 저수준 행위인 for 루프가 더 빠르다. `기본형 특화 스트림`을 사용해야 박싱/언박싱 오버헤드가 없다.

병렬 스트림(parallel stream)을 사용하는 경우

- 미리 준비된 데이터를 사용해야 한다. 병렬 스트림은 각각의 스레드에서 처리할 수 있도록 스트림 요소를 여러 청크로 분할한 스트림이다. stream.iterate(..).parallel() 이 코드와 같이 작성하면, 스트림이 병렬로 처리하기 위해 여러 청크로 분할할 수 없다. 따라서 순차처리와 같아지므로 병렬 처리의 이점을 얻을 수 없다.

- 공유되는 가변 상태를 피해야 한다. synchronized 키워드를 사용해서 동기화로 문제를 해결하면, 병렬화의 이점을 잃는다.

- filter 등의 연산을 피해야 한다. 어느 정도의 데이터가 필터링될지 모르기 때문에, 효과적으로 스트림을 병렬 처리할 수 있을지 알 수 없게 된다.

- findFirst(), findAny() 함수는 비슷한 동작을 수행하지만, 병렬 스트림에서 차이가 있다. 병렬 스트림에서는 첫 번째 요소를 찾는 것이 어렵다 (작업 데이터를 분할해서 처리하므로).  반면에 아무거나 1개를 찾는 건 쉽다. 따라서 병렬 스트림에서는 findAny() 함수를 사용하는 것이 성능 측면에서 더 낫다.


### 기존의 Java는 인터페이스 설계를 변경하기 어려웠다. 
기존 Java는 인터페이스의 추상 메소드를 수정하면, 해당 인터페이스를 구현한 모든 클래스도 함께 수정했어야 했다. 하지만 Java8에서 제공하는 디폴트 메소드를 사용하면, 기존 구현 클래스를 수정하지 않고 인터페이스를 수정할 수 있다. 또한 기존의 구현 클래스는 디폴트 메소드를 그대로 상속 받는다.


### 기존의 Java는 null인 상황을 처리할 명시적인 방법이 없었다.
우선 기존 Java의 null 처리 방법을 살펴보자. 한 눈에 봐도 코드 구조가 지저분하고, 가독성도 떨어짐을 알 수 있다.

```java
// 1. 깊은 의심
public String getCarInsuranceName(Person person) {
    if (person != null) {
        Car car = person.getCar();
        if (car != null) {
            Insurance insurance = car.getInsurance();
            if (insurance != null) {
                return insurance.getName();
            }
        }
    }

    return "unknown";
}

// 2. 너무 많은 출구
public String getCarInsuranceName(Person person) {
    if (person == null)
        return "unknown";
    
    Car car = person.getCar();
    if (car == null)
        return "unknown";

    Insurance insurance = car.getInsurance();
    if (insurance == null)
        return "unknown";

    return insurance.getName(); 
}
```

Java 8에서는 null인 상황을 처리할 수 있는 명시적인 방법을 제공한다. 바로 Optional&lt;T&gt; 이다. 다음 코드는 위 예제를 Optional로 해결한 코드다. 

```java
public String getCarInsuranceName(Optional<Person> person) {
    return person.flatMap(Person::getCar)
                .flatMap(Car::getInsurance)
                .map(Insurance::getName)
                .orElse("unknown")
}
```

이전 코드에 비해 가독성이 좋아졌다. 또한 Optional을 사용함으로써 인자로 주어진 person 객체가 있을 수도 있고, 없을 수도 있다는 사실을 알렸다. 즉, 명시적으로 null일 수 있다는 상황을 정의했다.


