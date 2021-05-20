# Kotlin Scope Functions


## 개요

어떤 object의 context 내에서 코드 블록을 실행하는 함수

Kotlin 표준 라이브러리에서 제공하는 함수이며, 각각의 유사성이 매우 높아 잘 알고 사용해야 한다. 잘못 사용했다고 해서 버그가 생기는 건 아니다. 예를 들어, let 대신 apply를 썼다고 제대로 동작하지 않는 건 아니다. 하지만, 적재적소에 맞게 사용해야 의도를 더 잘 표현할 수 있다.

→ 실제로 코틀린 공식 문서에도 다음과 같이 말하고 있다.

> Due to the similar nature of scope functions, choosing the right one for your case can be a bit tricky. The choice mainly depends on your intent and the consistency of use in your project.

## Scope Functions 차이점

<img src="https://raw.githubusercontent.com/momentjin/blog-repository/ac13acd93edc089610669e088bb7f7ef66f891ae/resource/image/kotlin_scope_functions.png" width="700px"> 
</div>

위 표를 보면 알겠지만, Function 간 주요한 차이점은 다음과 같다.

### 1) Context object reference 방식

it : lambda argument

- 수신자 객체의 멤버에 액세스 할 때, this 키워드를 생략해서 마치 클래스 내에서 접근하는 것처럼 사용할 수 있다.

this : lambda receiver

- 수신자 객체의 멤버에 액세스 할 때, this 키워드를 생략해서 마치 클래스 내에서 접근하는 것처럼 사용할 수 있다.
- 반면에 this를 생략하게 되면, 이게 내부 프로퍼티를 참조하는건지 외부 프로퍼티를 참조하는 건지 헷갈리는 경우가 생길 수 있다. 따라서 this 사용은 되도록 Reference Object의 프로퍼티에 접근하는 용도로 사용하는  편이 좋다.

### 2) 함수의 반환 값

context object

- context object를 그대로 반환하기 때문에, 하나의 object에 대한 체이닝 연산을 적용하기에 좋다.
- 어떤 함수의 결과를 context object로 반환하는 경우, 추가적인 연산을 정의할 때 좋다

    ```kotlin
    fun getRandomInt(): Int {
        return Random.nextInt(100).also {
            writeToLog("getRandomInt() generated value $it")
        }
    }	
    ```

lambda result

- context object에 대한 연산 이후 다른 결과로 mapping 하는 경우 유용하다. 결과에 대한 타입이 달라져도 체이닝이 가능하다.
- scope를 한정짓기 위해서도 사용한다.

    ```kotlin
    val numbers = mutableListOf("one", "two", "three")
    with(numbers) {
        val firstItem = first()
        val lastItem = last()        
        println("First item: $firstItem, last item: $lastItem")
    }
    ```

## Scope Function 종류

### Let

it, lambda result

not null object에 대한 람다를 실행할 때 사용

context object에 대한 참조 범위를 블록 내로 한정지을 때 사용

lambda result를 반환하기 때문에, context object의 연산 이후 다른 값으로 mapping 할 때 유용

### With

this, lambda result

확장함수) context object를 사용해서 계산하고, 그 결과를 반환할 때 사용

비확장함수) 
→ 'With' this object, do the following!
→ 반환값 없이, context object를 활용한 계산 작업에 유용
→ 코틀린 공식문서에서는 이것을 더 추천한다고 한다.

### Run

this, lambda result / non extention function

확장함수) 람다식내에 context object를 초기화하고 계산하는 로직이 둘 다 있을 때 유용

비확장함수)
→ 여러 표현식들을 한 범위의 블록에서 실행시키고, 람다의 결과값을 반환해서 활용할 떄 유용
→ With와 유사하지만, with는 아규먼트가 필요하다. run은 그렇지 않다.

### Apply

this, context object result

Object 설정하고, 이를 그대로 반환해서 활용하려 할 때 유용

### Also

it, context object return

자기자신을 반환하면서, 어떤 부가적인 행동을 할 때 좋다. (아래 코드를 보는게 이해가 훨씬 빠를 듯)

```kotlin
val numbers = mutableListOf("one", "two", "three")
numbers
    .also { println("The list elements before adding new one: $it") }
    .add("four")
```

## 왜 사용할까?

Scope Function이 없어도 코드를 작성하는데 아무 문제 없다. 단지 표현이 달라질 뿐이다.

그렇다. 표현이 중요하다. 표현이 왜 중요할까?

- 어떤 변수를 특정 블록 내에서 쓰기 위해 참조 범위의 제한을 두겠다고 표현할 수 있다.
- 어떤 행위가 어떤 결과를 낳는지 표현할 수 있다.
- Scope Function을 쓰기 전보다 코드의 흐름을 더 자연스럽게 표현할 수 있다.

결국은 편의다. 

- 로컬 변수의 스코프를 제한하면 디버깅하기 쉽고,
- 각각의 Scope 함수의 용도를 알고 있다면 대략적으로 예측이 가능하기 때문에 코드 작성자의 의도를 추측하기 쉽다.
- 코드의 흐름을 자연스럽게 표현한다는 것 또한, 코드를 이해하는데 도움이 된다.

그래서 더더욱 도구는 주의해서 사용해야 한다. 오용과 남용은 동료들에게 잘못된 지식을 전파할 수 있다.
최소한 내가 사용하는 도구가 무엇인지 / 왜 쓰는지 / 단점은 무엇인지는 알고 써야한다. 도구를 만든 사람은 그 도구를 생각없이 만들지 않는다. 그들이 왜 그 도구를 만들었는지에 대해 의문을 갖자. 

## References

[https://kotlinlang.org/docs/scope-functions.html](https://kotlinlang.org/docs/scope-functions.html)

Kotlin In Action