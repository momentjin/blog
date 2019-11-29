# Clean Code
> 인사이트, 로버트 C.마틴 지음, 박재호. 이해영 옮김

어쩌면 개발자에게 있어 제일 어려운 것이 코드 작성일 수도 있습니다. 같은 기능을 구현하더라도 개발자마다 코드 스타일은 매우 상이하기 때문에 코드 퀄리티는 차이가 날 수 밖에 없습니다. 이를 위해 많은 조직들이 코드 리뷰를 통해 퀄리티를 높이고자 노력하고 있습니다.

코딩 실력을 쌓기 위한 노력은 필수이고, Clean Code와 같은 검증된 서적을 읽는 것은 정말 좋은 학습 방법이라고 생각합니다. 저 또한 코딩 실력을 높이고자 이 책을 읽었고, 앞으로 개발을 하면서 클린 코드에서 제시하는 부분들과 상이한 부분이 있는지 돌아볼 수 있게 간략히 정리해봤습니다. 


-----

## 함수

#### 함수는 최대한 작아야 한다
함수 내 블록, 들여쓰기는 1번이 좋다. 함수를 적당한 크기로 쪼개야 읽기도 편하고 테스트도 쉽다.

#### 함수는 하나의 역할만 담당해야 한다
하나의 역할이 말은 쉬운데 막상 함수를 작성할 때는 말처럼 쉽지 않다. 클린코드 저자는 아래 함수가 한 가지 역할만 하고 있다고 말했다.

```java
String renderPageWithSetupsAndTeardonws (PageData pageData, boolean isSuite) {
    if (isTestPage(pageData))
        includeSetupAndTeardownPages(pageData, isSuite);
    return pageData.getHtml();
}
```

세세하게 따져보면 위 함수가 하는 행동은 총 3가지다.
1. 페이지가 테스트 페이지인지 판단
2. 테스트 페이지라면, 설정페이지와 해제페이지를 삽입
3. 페이지를 HTML로 렌더링

하지만 지정된 함수 이름 아래에서 추상화 수준이 하나인 단계만 수행한다면 그 함수는 한 가지 작업만 한다고 말할 수 있다. 잘 생각해보면 함수를 만드는 이유는 결국 추상화를 통해 어떤 동작을 여러 단계로 나눠 수행하기 위함이다.

#### 함수가 한 가지만 하는지 판단하는 또 다른 방법
의미 있는 이름으로 함수 내의 로직을 다른 함수로 추출할 수 있다면 그 함수는 여러 작업을 한다고 간주할 수 있다.

#### 함수의 추상화 수준은 동일해야 한다.
저수준 코드와 고수준 코드가 섞여 있으면 가독성이 떨어진다. 그러므로 피하도록 하자.


## 주석

이 파트를 요악하면..
- 주석은 없는 게 낫다.
- 주석을 다는 것보다 코드를 깔끔하게 정리하고 표현력을 강화하는 방향으로 노력하는 편이 낫다.

그럼에도 불구하고 주석이 필요한 경우, 또는 있으면 좋은 경우는 다음과 같다.
- 저작권 표시
- TODO
- 중요성 강조

위를 제외한 모든 주석은 안 좋은 주석이라고 생각해도 무방하다.
- 의무적으로 주석을 다는 경우 (하지만, 조직의 룰이 있다면 의무적인 주석도 나쁘지 않다고 생각한다)
- 변수와 함수 이름에 의미가 잘 드러나있음에도 그 의미가 중복되게 주석을 다는 경우


## 객체와 자료구조

진정한 의미의 클래스란, 추상적인 인터페이스를 제공해 사용자가 구현을 모른 채 자료의 핵심을 조작할 수 있는 것.

자료구조를 사용하는 절차적인 코드는 
- 기존 자료구조를 변경하지 않으면서 새 함수를 추가하기 쉽다. 
- 새로운 자료구조를 추가하기 어렵다.

객체지향적인 코드는 
- 기존 함수를 변경하지 않으면서 새 클래스를 추가하기 쉽다.
- 새로운 함수를 추가하기 어렵다.

때때로, 단순한 자료구조와 절차적인 코드가 가장 적합한 상황도 있다. 이를 분별하는 것은 오로지 프로그래머의 몫이 아닐까.

> 책에서 언급하는 자료구조란, 함수 없이 오로지 공개 변수만 있는 클래스를 말한다. 

디미터 법칙 : 모듈은 자신이 조작하는 객체의 속사정을 몰라야 한다는 법칙. 객체에게 요청할 것이 무엇인지 명확히 하고, 이를 그대로 코드로 반영하자.

## 클래스

클래스 정의 컨벤션 지키기 -> [링크](https://www.oracle.com/technetwork/java/codeconventions-141855.html)

클래스의 크기는 항상 작아야 한다. 
- 크기는 클래스가 갖고 있는 책임의 개수에 비례한다. 즉 SRP를 지키면, 클래스의 크기를 작게 유지할 수 있다. Manager, Processor 등과 같이 모호한 단어가 있다면 클레스가 여러 책임을 갖고 있다는 증거다.
- 큰 클래스 몇 개가 아닌, 작은 클래스 여럿으로 이뤄진 시스템이 더 바람직하다. 항상 작아야 한다는 말이 반드시 라인 수가 적거나, 메소드의 갯수가 10개 이하로 유지하라는 말이 아니라고 생각한다. 해당 클래스가 맡고 있는 책임과 역할에 따라 적절한 크기로 만들자는 말이다.

클래스의 응집도를 높이자. 응집도가 높다는 말은 클래스에 속한 메서드와 변수가 서로 의존하며 논리적인 단위로 묶인다는 의미다. 클래스가 응집력을 잃는다면 클래스를 쪼개야 한다. (응집력이 낮은 예: 클래스 내 일부 메서드만 사용하는 인스턴스 변수가 많을 때)

클래스간 결합도를 낮추자. 즉 인터페이스를 활용하자. (DIP)


## 오류처리

오류코드보다 예외를 사용히자. 오류코드를 사용하면 로직의 흐름이 오류코드와 뒤섞여 가독성을 해친다.

`unchecked exception`을 사용하자. 아주 중요한 라이브러리를 작성한다면 모든 예외를 잡아야 하므로 이 경우엔 checked exception이 유용하다. 하지만 checked exception은 하위 단계에서 코드를 변경하면, 상위까지 영향을 준다. 즉, OCP를 위반한다. 이런 일을 방지하기 위해서라도 unchecked exception을 권장한다.

호출자를 고려해 예외 클래스를 정의하자. 어플리케이션에서 오류를 정의할 때 프로그래머에게 가장 중요한 관심사는 **오류를 잡아내는 방법**이 되어야 한다. 아래 코드는 외부 라이브러리가 던질 예외를 모두 잡아내는 똥코드다.
```java
ACMEPort port = new ACMEPort(12);
try {
    port.open();
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log(...);
} catch (ATMUnlockedException e) {
    reportPortError(e);
    logger.log(...);
} catch (GMXError e) {
    reportPortError(e);
    logger.log(...);
} catch (DeviceResponseException e) {
    reportPortError(e);
    logger.log(...);
} finally {
    ...
}
```

다음은 새로운 클래스를 정의해서 코드를 간결하게 만든 것이다. 외부 API를 감싸서 의존성을 크게 줄였다. 게다가 테스트 코드를 넣어주는 방법으로 기능 테스트하기도 쉬워진다.
```java
MyPort port = new MyPort(12);
try {
    port.open();
} catch (PortDeviceFailure e) {
    reportError(e);
    logger.log(...);
} finally {
    ...
}

public class LocalPort {
    private ACMEPort innerPort;

    public LocalPort (int portNumber) {
        innerPort = new ACMEPOrt(portNumber);
    }

    public void open() {
        try {
            port.open();
        } catch (DeviceResponseException e) {
            throw new PortDeviceFailure(e);
        } catch (ATMUnlockedException e) {
            throw new PortDeviceFailure(e);
        } catch (GMXError e) {
            throw new PortDeviceFailure(e);
        } catch (DeviceResponseException e) {
            throw new PortDeviceFailure(e);
        } 
    }
}

클라이언트가 반드시 특별한 처리를 해야하는지 의심해보자. 클라이언트가 이용하는 객체를 조작해서 클라이언트가 별다른 처리를 하지 않도록 만들어야 한다. 이렇게 하면 코드가 훨씬 간단해지고, 의미도 명확해진다. 아래 예시를 통해 확인하자. (사소해보일지도 모르지만, 정말 중요하다고 생각한다)
```java
// 변경 전
try {
    MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
    m_total += expenses.getTotal();
} catch (MealExcepnseNotFound e) {
    m_total += getMealPerDiem();
}

// 변경 후
// DAO 객체를 조작해 항상 MealExpenses 객체를 반환하도록 수정
MealExpenses expenses = expenseReportDAO.getMeals(employee.getID());
m_total += expenses.getTotal();
```

null을 반환하지 말자. 예를 들어 컬렉션을 조회하는 DAO에서 어떠한 데이터도 조회하지 못했을 때 null보다 비어있는 리스트를 반환하면 된다. 

null 전달을 막자. 인자로 null을 넘겨서 오류가 발생하지 않을 순 없다. 그러나 최대한 막아보자는 것이다. 인자가 null이면 새로운 유형의 예외를 던진다든지, 단정문을 사용하든지의 방법이 있겠다. Java에서는 Optional 객체를 사용하는 방법도 있다.


## 경계
> 경계란 외부 라이브러리, 오픈소스, Open API 등 외부적인 것들을 지칭함

경계에 외치한 코드는 분리하자. 새로운 클래스로 Wrapping해서 클라이언트에게 제공할 인터페이스를 축소시키거나 Adapter 패턴을 이용해 우리가 원하는 인터페이스에 맞게끔 변환하는 등의 방법이 있다. 



