Factory Pattern에 대해 정리한 글 입니다.

개발을 할 때 누구나 한 번쯤은 다음과 같은 코드를 작성해봤으리라 감히 예상해봅니다.
```java
public Pizza getPizza (String type) {
    if (type.equals("cheese"))
        return new CheesePizza();
    else if (type.equals("greek"))
        return new GreekPizza();

    ...
}
```

이 코드는 매번 다른 타입의 Pizza가 추가될 때마다 수정해야 한다는 문제점이 있습니다. 확장에는 열려있고 변경에는 닫혀있어야 하는 객체지향원칙 중 OCP를 어기고 있습니다.

바로 이러한 문제점을 해결하기 위해 Factory Pattern을 사용합니다. 엄밀하게 말하면, 객체를 생성하는 부분에서 발생하는 다양한 문제점을 해결하기 위해 Factory Pattern을 사용합니다. 

> 단순히 위 코드에서 객체를 생성하는 부분을 클래스로 캡슐화하는 것은 Pattern이 아니라고 합니다. 단순하게 SimpleFactory라고 지칭합니다.

Factory Pattern에는 크게 2종류가 있습니다. 
- Factory Method Pattern
- Abstract Factory Pattern


## Factory Method Pattern

`객체를 생성하기 위한 인터페이스를 정의하고, 서브클래스에서 어떤 클래스의 인스턴스를 만들지 결정하는 디자인 패턴`

이 패턴은 객체를 사용하는 일련의 로직 중 객체를 생성하는 부분을 유연하게 만들고 싶을 때 유용한 Factory 패턴입니다. 아래 코드를 보면 `피자를 만드는 순서`는 고정된 채로, `피자를 생성하는 방법`을 유연하게 확장할 수 있다는 사실을 알 수 있습니다.

```java
public abstract class PizzaFactory {
    public Pizza createPizza(String type) {
        Pizza pizza = createPizza(type);
        pizza.prepare();
        pizza.bake();
        pizza.cut();
        pizza.box();

        return pizza;
    }

    // Factory Method 
    protected abstract Pizza createPizza(String type);
}

// PizzaFactory를 상속해서 피자 만드는 방법을 재정의한다.
public class ABPizzaFactory extends PizzaFactory {
    Pizza createPizza(String type) {
        if (type equals("a"))
            return new APizza();
        else if (type equas( "b")) 
            return new BPizza();

        ....
    }
}

public class XYPizzaFactory extends PizzaFactory {
    Pizza createPizza(String type) {
        if (type equals("x"))
            return new XPizza();
        else if (type equals("y")) 
            return new YPizza();

        ....
    }
}
```


## Abstract Factory Pattern

`서로 연관되거나 의존하는 객체를 구상 클래스를 지정하지 않고 생성할 수 있는 디자인 패턴`

Factory Method Pattern만 사용할 때 발생할 수 있는 문제점이 하나 있습니다. 특정 제품을 구성하는 제품 구성품들을 생성하기 위해 여러 개의 Factory가 필요하다는 점이 문제입니다.

추상 팩토리를 사용하면, 일련의 제품 구성품들을 그룹 단위로 묶어 생성하는 것이 가능합니다.

```java
interface PizzaIngredientFactory {
    public Dough createDough();
    public Sauce createSauce();
    ...
}

// 피자재료 Factory를 상속해서 구체적인 피자 재료를 정한다.

class ABPizzaIngredientFactory extends PizzaIngredientFactory {
    public Dough createDough() return new ...();
    public Dough createSauce() return new ...();
}

class CDPizzaIngredientFactory extends PizzaIngredientFactory {
    public Dough createDough() return new ...();
    public Dough createSauce() return new ...();
}

// 실제 Pizza

class CheesePizza extends Pizza {
    PizzaIngredientFacotry factory;

    // 피자 재료 공장을 통해 피자 재료를 생성한다.
    // 피자 재료 공장에 따라 유연하게 재료를 바꿀 수 있다.
    // 즉 객체를 생성하는 부분이 유연해지고, 확장에 열려있음을 알 수 있다.
    public CheesePizza(PizzaIngredientFactory factory) {
        this.factory = factory;
        dough = factory.createDough();
        sauce = factory.createSauce();
    }
}
```

## 마무리

팩토리 패턴은 처음엔 이해가 잘 안될 수도 있습니다. 굳이 뭣하러 이런 일을 하는지 생각하기도 합니다. 하지만 분명한 것은 거대한 도메인을 다룰 때 반드시 필요한 패턴입니다. 복잡한 도메인일수록 분기처리도 많아지게 됩니다. 분기처리 로직들을 효율적으로 관리하는 방법을 모른다면, 소프트웨어는 점점 유지보수하기 어려워질 것입니다.

이런 측면에서 팩토리 패턴은 정말 좋은 대안이 될 수도 있을 것 입니다.
