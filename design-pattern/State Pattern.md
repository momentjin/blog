State Pattern에 대해 정리한 글 입니다.

Head First Design Patterns 에서는 State Pattern을 다음과 같이 정의했습니다.

`객체의 내부 상태가 바뀜에 따라 객체의 행동을 바꾸는 패턴`

State Pattern은 다른 패턴보다 이해가 쉬웠습니다. 그리고 인터넷에 질 좋은 예제들이 너무 많습니다. 그래도 공부했으니 간단히 정리해보았습니다.


## 못난 예제

상태에 따라 다르게 행동해야 하는 객체를 구현해야 합니다. Printer 객체를 만들어보는 것이 좋겠습니다.

Printer의 상태는 '인쇄대기', '인쇄시작' 이렇게 2가지의 상태와 문서를 인쇄하는 printDoc이라는 행위만 존재한다고 가정합시다. 아래는 가정을 토대로 작성한 Printer 클래스입니다.

```java
class Printer {

    private final static int WAIT = 0;
    private final static int ING = 1;
    private int currentState = WAIT;

    public void printDoc(Document doc) {
        if (currentState == WAIT) {
            System.out.println("Print..");
            currentState = ING;
            // print 로직
            // ...
            currentState = WAIT;
        }

        else if (currentState == ING) {
            System.out.println("이미 프린트하고 있는 문서가 있습니다. 잠시 후 요청해주세요");
        }
    }
}
```

위 코드를 보면 어떤 생각이 드시나요? 객체지향원칙에 대해 아시는 분이라면, 당연히 냄새가 날 것 같은 코드라고 생각하실겁니다. (변경의 여지가 없다면 단순히 if-else 키워드를 사용하는 것도 하나의 방법일 수 있습니다)

Printer의 상태가 추가 된다고 가정하면, printDoc 메소드는 수정해야 합니다. 상태가 추가될 때마다 계속해서 변경해야 하는 문제가 있습니다. 뿐만 아니라, state에 따라 달라지는 행위가 printDoc만이 아닌 다른 행위도 존재한다면 어떻게 될까요..? 결국 상태에 의존적인 코드로 인해 사이드 이펙트가 계속해서 발생하고, 테스트, 유지보수 모두 어려워질 것 입니다. 

바로 이런 상황에서 써볼 법한 패턴이 바로 State Pattern 입니다.

## 잘난 예제

이제 고쳐보겠습니다. 우선 위에서 상수로 정의했던 각 상태를 클래스로 만들어야 합니다.

```java
interface PrinterState {
    void printDoc(Document doc);
}

class WaitState implements PrinterState {

    Printer printer;

    public WaitState(Printer printer) {
        this.printer = printer;
    }

    @Override
    public void printDoc(Document doc) {
            System.out.println("Print..");
            this.printer.setState(this.printer.getIngState());
            // print 로직
            // ...
            this.printer.setState(this.printer.getWaitState();
    }
}

class IngState implements PrinterState {

    Printer printer;

    public IngState(Printer printer) {
        this.printer = printer;
    }

    @Override
    public void printDoc(Document doc) {
        System.out.println("이미 프린트가 진행중 입니다. 잠시후 다시 요청해주세요");
    }
}
```

그리고 Printer 클래스를 수정하겠습니다.
```java
class Printer {

    private PrinterState waitState;
    private PrinterState ingState;

    private PrinterState currentState;

    public Printer() {
        this.waitState = new WaitState(this);
        this.ingState = new IngState(this);
        this.currentState = this.waitState;
    }

    public void printDoc(Document doc) {
       state.printDoc(doc);
    }

    // getters, setters
    // ...
}
```

차이가 좀 느껴지시나요? 못난 예제에서는 상태와 행위가 추가될 때마다 수정해야 하는 범위가 늘어났지만, 현재는 Printer의 멤버변수 및 생성자의 초기화 변수만 추가로 작성하면 됩니다. 이런 것이 가능한 이유가 뭘까요? 각각의 상태를 객체로 분리해서 책임을 할당했기 때문입니다. 

못난 예제에서는 printDoc의 책임의 개수가 상태의 개수와 같았습니다. 상태가 N개면 책임도 N개가 될 수 있다는 말과 같습니다. 이런 것을 객체지향원칙에서 `단일 책임의 원칙`(SRP)을 어겼다고 말합니다. 그리고 잘난 예제는 단일 책임의 원칙을 아주 잘 보여주고 있습니다.


## 다이어그램

<img src="https://raw.githubusercontent.com/momentjin/study/master/resource/image/uml-state.png" height='300px'>


## 정리

어떤 객체가 동일한 메세지를 수신했는데, 조건에 따라 다르게 행동해야 한다?

그렇다면 State Pattern을 고려해야겠습니다. 먼 훗날 실무에서 사용하는 그 날이 왔으면 좋겠네요 ;)
