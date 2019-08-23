# Java 8에 대하여

Java 8이 릴리즈된지 벌써 4~5년이 지났지만, ,Java 8에 제대로 알고 있는 지식이 하나도 없었습니다. 이번 기회에 Java 8이 탄생한 이유가 무엇인지, 그 핵심에 대해서 확실하게 알아보려 합니다. 뿐만 아니라, Stream과 같은 중요 API에 대한 동작원리와 사용시 주의점도 정리할 것 입니다.

### 기존 Java는 멀티코어를 제대로 활용하지 못했다.
thread, synchronized 등을 직접 다룰 때의 문제가 많았다. 즉, 다루기 어려웠다.

### 기존 Java는 보일러 플레이트 코드가 너무 많았다.
Java의 익명클래스를 이용하는 경우, 보일러플레이트 코드가 너무 많았다. Collections.sort()의 정렬 전략을 구현해본 사람은 다들 알 것이다. Java 8에서는 함수를 일급객체로 사용하기 때문에 람다 또는 메소드 레퍼런스 등을 활용하면 불필요한 코드 없이 간결한 코드를 작성할 수 있다.
```java
// 보일러 플레이트 코드가 많은 Java 코드
Arrays.asList(1, 2, 3, 4).sort(new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return 0;
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


