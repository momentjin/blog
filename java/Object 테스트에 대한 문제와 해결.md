Java를 활용해서 Object를 테스트할 때, '테스트할 수 있는 상황'을 만들기 어려워서 매번 좌절했었습니다. 그 후 마침내 하나의 결론에 도달하게 되었습니다. 이번 글에서는 Object를 테스트할 때의 문제와 이 문제를 해결하기 위한 여러가지 방안에 대해 살펴보고, 가장 합리적이라고 생각하는 방안에 대해 이야기 해보겠습니다.

## 문제 상황

간단한 예제를 통해 문제가 무엇인지 알아보겠습니다. Applyment(지원서)라는 객체가 있습니다. Applicant(지원자)가 Company에 지원하면 Applyment 객체를 생성합니다. 이 Applyment는 지원취소라는 행위인 cancel() 메소드를 갖고 있습니다. 이 메소드는 다음과 같은 비즈니스 규칙을 갖고 동작합니다. 

- 지원취소 규칙 : '지원 후 10일이 지나면 지원을 취소할 수 없다'

코드로 표현하면 아래와 같습니다.

```java
public class Applyment {

    private Long PK;
    private Applicant applicant;
    private Company company;
    private State state;
    private LocalDateTime createdAt;

    public static Applyment createNewApplyment(Applicant applicant, Company company) {
        Applyment applyment = new Applyment();
        applyment.applicant = applicant;
        applyment.company = company;
        applyment.state = State.COMPLETE;
        applyment.createdAt = LocalDateTime.now();
    }

    public void cancel() {

        LocalDateTime deadline = this.createdAt.plusDays(10);
        LocalDateTime now = LocalDateTime.now();

        if (deadline.isEquals(now) && deadline.isAfter(now)) 
            throw new RuntimeException('지원한지 10일이 경과했으므로, 지원을 취소할 수 없습니다.');

        this.state = State.CANCEL;
    }
}
```

이제 Applyment 객체의 cancel 메소드에 대한 테스트 코드를 작성해보겠습니다.

```java
@Test
public void 지원후_10일이전까지_지원을_취소할수있다() {

    // given
    Applicant applicant = ..;
    Company company = ..;
    Applyment applyment = Applyment.createNewApplyment(applicant, company);

    // when
    applyment.close();

    // then
    assertTrue(applyment.isCanceled());
}
```

Applyment에 존재하는 코드를 활용해서 작성한 테스트 코드입니다. 하지만 이 테스트는 실패합니다. applyment를 close하는 시점이 오늘이므로, close 메소드 호출시 조건문에 걸려 예외가 발생합니다. 이 문제를 해결하기 위해선 Applyment 객체의 createdAt 필드를 과거로 변경하면 됩니다. 하지만 Applyment 객체의 코드만으론 createdAt을 조작할 수 없습니다. 

## 시도해본 해결 방안

### 생성자

생성자를 만드는 건 득보다 실이 많습니다. 생성자란 객체를 생성하기 위한 필수 값을 정의한 일종의 메소드라고 생각합니다. 만약 createdAt을 외부로 부터 주입받는다면, 비즈니스 규칙에 어긋나는 상황들이 발생하고 점차 유지보수하기 힘든 코드로 변질됩니다. 실제 비즈니스에서는 방대한 규칙이 존재하는데 그 규칙을 테스트하고자, 유지보수성을 버리는 것은 말이 안됩니다. 

### Setter

Setter 또한 생성자와 동일한 이유로 인해 사용하지 않아야 합니다.

### Json 파일과 ObjectMapper

json 파일 값을 기반으로 ObjectMapper를 통해 객체를 생성하는 방식도 있습니다. 이 방식의 문제점은 특정 Context를 위해 생성해야 하는 N개의 케이스에 대한 모든 json 파일을 정의해야 합니다. 필드 1개만 추가되어도 N번의 변경 작업이 필요할 수 있기 때문에 이 방법도 그리 추천되진 않습니다.

### DB 데이터 삽입 

테스트 시작시, 특정 Context에 해당하는 데이터들을 INSERT SQL을 통해 삽입하고, 해당 객체를 불러와 테스트하는 방법도 시도해본 적이 있습니다. 하지만 문제가 많아서 이 방법을 사용하지 않았습니다.

- DB없이 단위 테스트를 수행할 수 없다. 즉, DB에 항상 의존해야 한다. -> POJO에 대한 독립적인 테스트가 불가능해, 단위 테스트에 부합하지 않는다.

- 특정 Context에 해당하는 N개의 케이스에 대한 모든 query를 작성해야 한다. -> 수정이 번거롭다. 

### Stub 객체 사용

테스트하려는 Object를 위한 Stub 객체를 만들어, 테스트를 위한 Context를 임의로 만드는 방식입니다. 이 방식 역시 시도해봤지만, 객체 내에서 this.field로 로직을 작성하는 경우, 의도대로 동작하지 않습니다. 따라서 method를 overriding하는 stub 객체를 만들면 문제는 해결되지만, 객체 자신의 데이터를 조작할 때 getXXX() 메소드를 사용하는 것은 가독성이 좋지 않아서 개인적으로 별로라고 생각합니다.

### Test Builder의 사용

이 부분이 제가 선택한 해결 방안입니다.

## 최종 해결 방안 

제가 선택한 해결 방안은 아래와 같이 Test 전용 Builder를 만들어 활용하는 것 입니다.

```java
public class Applyment {
    
    ...

    @Builder(builderClassName="TestBuilder", builderMethodName="testBuilder")
    public Applyment(Long PK, Applicant applicant, Company company, State state, LocalDateTime createdAt) {
        
        this.PK = PK;
        this.applicant = applicant; 
        ...
        ...
    }
}
```

Builder를 통해 아래와 같이 특정 Context에 필요한 데이터만 주입해서, 적합한 Context를 만들 수 있습니다.

```java
@Test
public void 지원후_10일이전까지_지원을_취소할수있다() {

    // given
    LocalDateTime anyPastDateTime = LocalDateTime.now().minusDays(5);
    Applyment applyment = Applyment.testBuilder
            .createdAt(anyPastDateTime)
            .build();

    // when
    applyment.close();

    // then
    assertTrue(applyment.isCanceled());
}
```

반드시 Lombok이 생성해주는 Builder를 활용하지 않아도 됩니다. Builder를 커스터마이징할 수도 있습니다. 적절한 예시는 사실 딱히 없어서, 검색해서 찾은 자바지기님의 [글](https://www.slipp.net/questions/94)을 참고해주세요.

어쨌든! 이 방법이 최선이라고 생각한 이유는 다음과 같습니다.
- 테스트를 위한 특정 Context를 쉽게 생성할 수 있다.
- 테스트에서 필요한 데이터만 주입할 수 있다.
- 다른 방법보다 유지보수가 쉽다.

단점이라고 생각될 수 있는 부분도 있지만, 이에 대한 나름대로의 핑계를 대보겠습니다.

- 동료 개발자의 TestBuilder 오용 -> 말 그대로 **Test**Builder이므로, 이 문제가 발생할 가능성은 적어보입니다.

## 감사의 말씀

TestBuilder를 활용하는 것은 [jojoldu](https://jojoldu.tistory.com)님께 직접 이메일로 질문해서 얻은 조언입니다. 진심으로 감사드립니다.

## 후기

소프트웨어 공학은 답이 없는 분야라서, 상황에 적합한 최선의 솔루션을 선택해야 합니다. 이러한 판단력을 키우는 것이 개발자가 가져야할 역량 중 하나가 아닐까 생각이 이 글을 쓰면서 더더욱 느껴집니다. 읽어주셔서 감사합니다.