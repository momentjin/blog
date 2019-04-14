# Java String과 불변성
> 자주 사용하는 데이터 타입인 String에 대한 몇 가지 궁금증을 해소하고자 이 글을 작성했습니다.


## String ?

String은 문자열을 표현하는 용도로 사용되는 Class입니다.

Java의 데이터타입은 크게 원시타입(primitive type)과 참조타입(reference type)으로 나뉘는데, String은 참조타입에 해당하는 Class Type입니다. 따라서 모든 문자열 데이터는 String 클래스의 인스턴스라고 볼 수 있습니다.

또한, String은 클래스이므로 이에 대한 여러가지 행위를 메소드로 표현할 수 있습니다. 대표적으로 split, replace 등의 메소드가 이에 해당합니다.


## String is immutable ?
'+' 연산을 사용한 문자열 붙이기는 새롭게 객체를 생성하며, 이는 성능에 좋지 않기 때문에 StringBuilder 또는 StringBuffer를 사용해야 한다는 말은 한 번쯤은 들어봤을 것입니다.

저 또한 Java로 알고리즘 문제 풀 때 마르고 닳도록 들었는데, 이제서야 왜 String은 변할 수 없게 만들었는지 궁금해서 찾아봤습니다.

구글링을 해보니 'String Immutable' 관련하여 어떤 분께서 번역해주신 포스트가 있었습니다. 아래는 이것을 단순히 요약한 것이므로 자세히 알고 싶으신 분은 원문을 참고해주세요.
[출처](http://www.mimul.com/pebble/default/2015/10/10/1444466677572.html)

#### String이 불변 객체인 이유

최적화 <br>
: Java의 설계자가 String이 가장 많이 사용되는 클래스일거라 예측했고, 그러한 예측이 최적화의 필요성으로 이어졌다고 한다. 최적화의 일환으로 String 객체를 공유해 String 객체 생성이 최소화될 수 있게 만들었다. 

- 보안 <br>
: host, port, url, password, file path 등의 값을 가진 String이 변경될 수 있다면, 심각한 보안 문제를 일으킬 수 있다. <br>
: JVM의 클래스 로딩시 String이 자주 사용되는데 이를 테면 java.io.Reader 자바 표준 클래스를 로딩할 때, 어떠한 위협에 의해 보안에 치명적인 클래스가 로드될 수 있다고 한다.

- 멀티 쓰레드 환경
: 변경 불가능하면 멀티 쓰레드 환경에서 동기화를 고려할 필요가 전혀 없다. String의 Immutable한 속성으로 인해 쓰레드 간 공유가 가능하고, 동기화 처리가 필요 없으므로 코드가 간단해진다는 장점이 있다. 


## StringBuilder(or Buffer)는 뭐가 다르길래?

앞서 말씀드렸듯이 +연산은 String 객체를 생성하기 때문에 Builder나 Buffer를 사용해야 합니다. 객체를 다시 만들지않고, 어떻게 문자열을 수정할 수 있는지 궁금해서 소스코드를 찾아봤습니다.

StringBuilder가 상속받는 AbstractStringBuilder 추상 클래스는 기본적으로 character type의 array 멤버변수가 존재합니다. 이 array를 조작해서 값을 수정하는 것입니다. 아래 코드는 String 문자열 중 특정 위치의 값을 변경하는 setCharAt 메소드입니다. 이 메소드를 참고하시면 StringBuilder는 왜 새로운 객체를 생성하지 않고, 값을 변경할 수 있는지 쉽게 이해할 수 있을 것 같습니다.

```java
abstract class AbstractStringBuilder implements ... {
    /**
     * The value is used for character storage.
     */
    char[] value;
    
    public void setCharAt(int index, char ch) {
        if ((index < 0) || (index >= count))
            throw new StringIndexOutOfBoundsException(index);
        value[index] = ch;
    }
    ...
}
```
