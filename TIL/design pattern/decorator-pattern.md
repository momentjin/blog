# Decorator Pattern
> 객체에 책임을 덧붙이는 패턴으로, 객체의 기능 확장이 필요할 때 상속보다 더 유연한 대안을 제공한다. 

## UML
![image](https://raw.githubusercontent.com/momentjin/study/master/resource/image/uml-decorator.PNG)
- Component: 최상위 클래스
- ConcreteComponent: Component 클래스를 상속한 클래스
- Decorator : Component를 확장하기 위한 추상 클래스
- ConcreateDecorator : Component를 확장한 클래스

## 실제 예시
Java의 Stream API는 Decorator Pattern을 적용한 대표적인 예제이다. stackoverflow에 [좋은 예제](https://stackoverflow.com/questions/6366385/use-cases-and-examples-of-gof-decorator-pattern-for-io)가 있어서 가져왔다.

같은 InputStream을 상속한 Stream 클래스지만, 이렇게 하나의 클래스를 또 다른 클래스로 감싸면서 기능을 확장할 수 있다.

```java
// 파일 열기
FileInputStream fis = new FileInputStream("/objects.gz");

// 버퍼를 활용해 읽는 속도 높이기
BufferedInputStream bis = new BufferedInputStream(fis);

// 압축된 파일 해제
GzipInputStream gis = new GzipInputStream(bis);

// 특정 클래스로 전환
ObjectInputStream ois = new ObjectInputStream(gis);

// 실제 사용시 
SomeObject someObject = (SomeObject) ois.readObject();
```