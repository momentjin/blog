# Effective Unit Testing
> 한빛미디어, 라쎄 코스켈라 지음, 이복연 옮김

#### 이 책을 읽은 이유
단위 테스트를 작성하는 방법에 대해 배우고자 이 책을 읽었습니다. 이 책을 모두 읽고 정리하는데로, 개인프로젝트의 테스트코드도 개선해보려고 합니다.

중요하다고 생각하는 부분만 정리했습니다. 참고해주세요!
 
---

## Part1. 기반 다지기

### 테스트의 가치

#### 테스트는 생산성을 높여준다.
생산성에 영향을 주는 직접적인 요소로 `피드백 주기`와 `디버깅 시간`이 있다. 올바른 테스트는 빠른 피드백을 줄 수 있고, 디버깅에 할당하는 시간을 최소한으로 유지할 수 있도록 도움을 준다.

##### 퀄리티가 낮은 테스트 코드는 오히려 생산성의 저하를 초래한다.
- 테스트 실행 속도가 낮으면, 변경사항을 검증하고 확인하기 위해 기다리는 시간이 길어진다.
- 가독성이 떨어지면, 테스트 원인 파익이 어렵다.
- 테스트 코드를 분석하기 위해 또 다른 시간을 투자해야 한다. (디버깅 등)

### 좋은 테스트란?
좋은 테스트란, 테스트의 대상이 `명확`하고, 그 결과를 `신뢰`할 수 있으며, 문제 발생시 쉽게 원인을 찾을 수 있는 `가독성`을 가진 테스트를 말한다.

#### 가독성, 유지보수성
이해와 수정이 어려운 테스트 코드에서 오류가 생긴다면, 오류의 원인을 찾는데 많은 시간을 쏟을 확률이 높다.

#### 분명한 의도
테스트의 이름만 보고도 무엇을 테스트하려는지 명확히 해야한다. 테스트가 실패했을 때, 무엇이 실패했는지 쉽게 판단할 수 있다. <br>

#### 테스트의 독립성
테스트코드가 아래의 요소에 독립되어야 좋은 테스트다. 여러 요소에 의존하는 테스트는 불규칙한 결과를 낳고, 관리하는 것도 어렵다.

- Time
- Infra
- Networking
- Pre-existing Data
- Concurrency (동시성)
- Randomness (임의성)
- Persistency (영속성)

##### 테스트 코드의 독립성을 유지하기 위한 방법
- 서드파티 라이브러리와의 종속성을 제거한다.
- 테스트에 필요한 리소스는 테스트 코드와 같은 위치에 둔다.
- 테스트가 사용할 자원을 직접 생성하도록 한다.
- 테스트가 필요한 문맥을 직접 설정하게 한다. (다른 테스트에 의존하지 않는다.) 
- 영속성이 필요한 통합테스트는 인메모리 데이터베이스를 활용한다.
- 비동기식 테스트의 경우, 전문 테스트 그룹에 맡긴다.


### 테스트 더블

~~이론으로만 배웠더니 실전에서 어떻게 적용해야 할지 감이 오지 않음. 실전에서 활용해보면 더 잘 정리할 수 있을 것 같아서 나중에 작성할 예정~~

테스트 더블이란, 스텁/가짜객체/Mock객체 등의 개념들을 통칭하는 용어이다.

---

## Part2. 테스트 냄새

### 가독성
테스트 코드도 역시 코드다. 테스트가 어떤 것을 테스트 하는지 코드만으로 명확하게 이해할 수 있어야 한다.

아래는 가독성 파트에서 가장 인상 깊었던 문장이다.
> 테스트를 하나 작성할 때마다 한 걸음 물러나 자문해보라. '테스트가 하려는 일이 진짜 명백한가?'

#### 기본타입 단언
단언문에 너무 낮은 수준의 추상화를 사용하여 단언하려는 이유나 의도를 이해하기 어려운 상황을 말한다. 아래에 기본타입 단언이 존재하는 코드와 이를 개선한 코드가 있다. 이를 보면 쉽게 이해할 수 있을 것이다.

```java
// content에 text라는 문자열이 존재하는지 검사하는 테스트
public void test() {
    String content = "some text";
    assertTrue(content.indexOf("text") > -1);
}

// 개선
// 더 높은 추상화를 활용해 테스트 코드가 훨씬 직관적이다.
public void test() {
    String content = "some text";
    assertTrue(content.contains("text"));
}
```

#### 광역 단언
너무 세세하게 테스트 하려는 상황이다. 무엇을 테스트하는 것인지 명확하게 판단하기 어렵다. <br>
하나의 케이스에 대해 많은 테스트를 수행하는 것은 분명 좋다. 하지만, 테스트가 실패했을 때 무엇이 잘못되었는지 판단하기 어렵다. 

광역 단언을 개선하는 방법은 테스트 목적을 이룰 수 있을 만큼의 테스트만 코드로 작성하면 된다.

#### 부차적 상세정보
어떤 테스트를 수행하기 위해 준비하는 객체 등은 테스트의 핵심이 아니다. (물론 상황에 따라 다르다) 따라서 핵심이 아닌 코드로 인해, 테스트의 의도를 파악하기 힘든 경우가 생긴다.

이 문제를 개선하는 방법은 테스트의 목적을 명확히 하는 것 그 뿐이다.. 책에서는 다음과 같은 지침을 따르길 권한다.
- 핵심이 아닌 설정은 private 메소드나 셋엄 메소드로 추출하라.
- 적절한 인자와 서술형 이름을 사용하라.
- 하나의 메소드 안에서 모두 같은 수준으로 추상화하라.

#### 다중인격
하나의 테스트에 여러 개의 테스트 목적이 포함된 것을 말한다. 테스트의 목적을 알기 어렵고, 테스트가 실패할 때 무엇이 실패했는지 파악하는 것도 힘들다. 

다중인격을 개선하는 방법은 테스트의 목적을 명확하게 파악해서 나누는 것이다. 이렇게 하면 테스트 메소드 이름도 훨씬 구체적으로 지을 수 있다.

```java
// 개선 전
@Test
public void testParsingCommandLineArgs() {
    String args[] = { "-f", "hello.txt", "-v", "--version" };
    Configuration c = new Configuration();
    c.processArguments(args);
    assertEqauls("hello.txt", "c.getFileName()");
    assertFalse(c.isDebuggingEnabled());
    assertFalse(c.isWarningsEnabled());
    assertTrue(c.isVerbose());
    assertTrue(c.shouldShowVersion());

    c = new Configuration();
    try {
        c.proccessArguments(new String[] {"-f"});
        fail("Should've failed");
    }
}

// 개선 후
// 메소드명이 훨씬 더 명확해져서 테스트 목적을 파악하기 쉬워졌다.
@Test
public void validArgumentsProvided() {
    String args[] = { "-f", "hello.txt", "-v", "--version" };
    Configuration c = new Configuration();
    c.processArguments(args);
    assertEqauls("hello.txt", "c.getFileName()");
    assertFalse(c.isDebuggingEnabled());
    assertFalse(c.isWarningsEnabled());
    assertTrue(c.isVerbose());
    assertTrue(c.shouldShowVersion());
}

@Test(expected=InvalidArgumentException.class)
public void missingArgument() {
    c.processArguments(new String[] {"-f"});
}
```

#### 쪼개진 논리
테스트의 범위나 목적을 명확히 하기 위해 메소드 등을 과하게 분리한 상황을 말한다. 보통 테스트 클래스나 메소드를 작게 나누면 가독성이나 유지보수성이 좋아진다. 하지만, 의미없고 무분별하게 나누는 것은 오히려 해당 테스트를 더욱 파악하기 어렵게 만든다.

> 테스트를 분리하거나 통합하는 경계는 책을 읽어도 깨닫기 어렵다. 하지만 분리가 가독성을 보장하지 않는다는 사실을 꼭 기억하고 싶어서 정리했다. 테스트를 의미있게 분리하는 연습을 해야겠다.

<br>

### 유지보수성
매번 언급하는게 맞나 싶을 정도로 지겹지만, 테스트코드 또한 코드라는 사실. 따라서 관리하지 않으면 향후 테스트 코드의 유지보수성이 떨어진다. 이번 파트에서는 유지보수성을 위협하는 다양한 원인을 알아본다.

#### 중복
중복은 `불필요한 반복`이다. 따라서 중복이 많으면, 유지보수하기 매우 어렵다.

일부러 중복을 남겨야 하는 상황도 있다. (지금은 와닿지는 않는다.)

중복의 종류는 크게 3가지
- 상수 중복 : 하드코딩 등..
- 구조 중복 : 유사한 로직 등..
- 의미 중복 : 같은 기능이나 개념을 서로 다른 방식으로 구현해서 발생하는 중복

상수중복과 구조중복은 단순히 문자열이나 로직의 중복을 뜻하고, 의미 중복은 예시로 정리해봤다. (사실 이 책의 저자가 남겨놓은 과제다)
 
```java
// 의미가 중복되는 2개의 테스트 메소드
// 특정 기준으로 직원을 필터링 하는 기능을 서로 다른 방식으로 구현했다. 

public void 그룹은_2명의_감독관을_포함해야_한다() {
    List<Employee> all = group.list();
    List<Employee> employees = new ArrayList<>(all);
    Iterator<Employee> i = employees.iterator();
    while (i.hasNext()) {
        Employee employee = i.next();
        if (!employee.isSupervisor()) i.remove();
    }

    assertEquals(2, employees.size());
}

public void 그룹은_5명의_신입사원을_포함해야_한다() {
    List<Employee> newcomers = new ArrayList<>();
    for (Employee employee : group.list()) {
        DateTime oneYearAgo = DateTime.now().minusYear(1);
        if (employee.startingDate().isAfter(oneYearAgo)) {
            newcomers.add(employee);
        }
    }

    assertEquals(5, employees.size());
}
```

```java
// 의미 중복을 제거하는 순서
// 1. 구조 중복으로 번경한다.
// 2. 구조 중복을 개선한다.

// 구조 중복으로 변경한 테스트 메소드
// 필터링 대상을 저장할 변수를 선언하고, 루프를 돌며 조건부 필터링하는 로직이 같다. (즉, 조건만 다르다)
public void 그룹은_2명의_감독관을_포함해야_한다() {
    List<Employee> supervisors = new ArrayList<>();
    for (Employee employee : group.list()) {
        if (employee.isSupervisor()) {
            supervisors.add(employee);
        }
    }

    assertEquals(2, supervisors.size());
}

public void 그룹은_5명의_신입사원을_포함해야_한다() {
    List<Employee> newcomers = new ArrayList<>();
    for (Employee employee : group.list()) {
        DateTime oneYearAgo = DateTime.now().minusYear(1);
        if (employee.startingDate().isAfter(oneYearAgo)) {
            newcomers.add(employee);
        }
    }

    assertEquals(5, newcomers.size());
}
```

```java
// 구조 중복을 개선한 테스트 코드 (직접 작성)
// 위에서 설명한 조건을 파라미터(Predicate)로 넘겨 처리했다.
@Test
public void 그룹은_2명의_감독관을_포함해야_한다() { 
    assertMemberNumInGroup(2, employee -> employee.isSupervisor());
}

@Test
public void 그룹은_5명의_신입사원을_포함해야_한다() { 
    DateTime oneYearAgo = DateTime.now().minusYear(1);
    assertMemberNumInGroup(5, employee -> employee.startingDate().isAfter(oneYearAgo);
}

// util method
private int assertMemberNumInGroup(int n, Predicate<Employee> isMatch) {
    List<Employee> members = new ArrayList<>();
    for (Employee employee : group.list()) {
        if (isMatch.test(employee)) {
            members.add(employee);
        }
    }

    assertEquals(members.size(), n);
}
```

#### 조건부 로직
테스트 코드에 조건에 따라 단정하는 상황을 말한다. 말보다 코드를 보는게 더 빠르겠다.

```java
// 딕셔너리에 키,값을 넣고 딕셔너리를 순회하며 넣었던 값이 존재하는지 찾는 테스트
public class DictionaryTest {

    @Test
    public void returnsAnIteratorForContents() throws Exception {
        Dictionary Dict = new Dictionary();
        dict.add("A", new Long(3));
        dict.add("B", "21");

        for (Iterator e = dict.iterator(); e.hasNext();) {
            Map.Enty entry = (Map.Entry) e.next();
            if ("A".eqauls(entry.getKey()))
                assertEquals(3L, entry.getValue());

            if ("B".equals(entry.getKey()))
                assertEquals("21", entry.getValue());
        }
    }
}
```

위 코드에는 총 2개의 조건부 로직이 존재한다. 언뜻 보면 크게 문제되지 않는 것 같다. 저자는 이 테스트의 목적이 명확하게 드러나지 않았다고 지적했다. 그리고 아래와 같이 이러한 조건부 로직을 간소화할 수 있는 방법을 소개했다. (많이 쓰이는 패턴이라고 강조하셨다!!)

```java
public class DictionaryTest {

    // 조건부로직을 별도의 메소드로 추출했다. -> 테스트 목적이 분명해졌다.
    @Test
    public void returnsAnIteratorForContents() throws Exception {
        Dictionary Dict = new Dictionary();
        dict.add("A", new Long(3));
        dict.add("B", "21");
        
        assertContains(dict.iterator(), "A", 3L);
        assertContains(dict.iterator(), "B", "21");
    }

    private void assertContains(Iterator i, Object key, Object value) {
        while (i.hasNext()) {
            Map.Enty entry = (Map.Entry) e.next();
            if (key.eqauls(entry.getKey())) {
                assertEquals(value, entry.getValue());
            }
        }

        // 비어있는 Iterator 또는 조건에 맞지 않았을 때 실패 처리.
        // 은근히 깜빡하는 경우가 많다고 한다
        fail("Iterator didn't contain key, value");
    }
}
```

#### 양치기 테스트
어떤 경우에는 성공하지만, 어떤 경우에는 실패하는 테스트를 말한다.
간헐적 결과를 낳는 테스트는 신뢰성이 없고, 테스트가 실패했을 때 원인 파악도 어려워 유지보수를 힘들게 만든다.

난수, 시스템 시계, 쓰레드, 공유자원에 대한 동시접근 등이 주 원인이다. 저자는 이것에 대한 해결방법으로 문제가 되는 대상을 `회피`하거나, `제어`하거나, `격리`하라고 조언했다. 

양치기 테스트 상황에 직면했을 때, 불규직적인 상황을 최대한 컨트롤할 수 있는 로직을 작성하자. 

#### 파손된 파일 경로
절대 경로, 특정 운영체제에서만 사용가능한 경로 등을 사용했을 때 나타나는 문제다. 테스트를 작성한 개발자의 컴퓨터에선 잘 동작하겠지만, 다른 컴퓨터에선 동작하지 않을 수 있다.

-> 프로젝트 루트 내 파일을 두고, 상대경로로 참조하면 해결할 수 있다.

#### 잠자는 달팽이
동시성 테스트든 뭐든, Thread.sleep()을 쓰는 것은 낭비다. 전체 테스트 슈트를 수행할 때 피드백을 받는 시간이 느려 작업 효율이 떨어지기 때문이다.

동시성을 제어할 수 있는 방법을 찾고 해결해야 한다. 자바의 경우 java.util.concurrent를 사용해 동시성을 제어할 수 있다고 한다. (안써봐서 잘 모르겠다..)


### 신뢰성

#### 주석
테스트가 주석처리 된 경우, 주석의 내용이 테스트 내용과 다른 경우 테스트에 대한 신뢰도가 떨어진다.

위와 같은 상황을 예방하는 방법은 주석을 최대한 아끼는 것이다. 코드의 의도를 전달할 책임은 `코드 자신`에 있다. 

피치 못하게 주석을 달아야 한다면? `Why`를 설명하는 주석을 달자. 코드를 그렇게 작성할 수 밖에 없었던 이유, 당위성을 설명해야 한다. 반면에, `What`을 설명하는 주석의 경우는 코드의 가독성이 떨어지는 경우가 많다.
