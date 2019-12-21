# Java Exception

> Java 언어를 지금까지 많이 해왔다고 생각했지만, 예외 처리에 대해 제대로 알아보려고 했던 적은 없었습니다. 지금이라도 생각난 김에 예외처리에 대해 한 번 정리해봤습니다.

## Exception ?

예외란, 프로그램 실행 도중 발생하는 문제 상황을 말합니다. 

### Exception 종류

Exception의 종류는 크게 `Checked Exception`과 `Unchecked Exception`으로 나뉩니다. 

`Checked Exception`은 예외에 대한 처리를 반드시 해야합니다. 즉 예외를 던지든지, 예외를 처리하든지 둘 중 하나는 반드시 해야합니다. 

`Unchecked Exception`은 예외 처리를 해도 되고 안해도 됩니다. 이런 예외를 `Runtime Exception`이라고도 합니다.

#### 예시

File API 관련 method 중 하나인 createNewFile 메소드를 사용하면 컴파일 오류가 발생합니다. 이 때 try-catch를 이용해 예외를 핸들링하거나, 예외를 상위로 던졌던 (throws) 던져야 합니다. 이런 예외를 CheckedException 라고 합니다.

반면에 ArrayIndexOutOfBoundsException와 같이 별다른 처리를 하지 않아도 되는 것이 Unchecked Exception 입니다. 물론 try-catch, throws를 이용해 처리해도 무방합니다. 


## 끝으로

생각보다 내용이 많이 부실해서 당황했습니다. 정리하고 보니, 자바의 예외 처리가 복잡하지 않다는 사실을 깨달았습니다. ~~이렇게 단순한 시스템을 이제서야 알게되어 솔직히 좀 부끄럽..~~

예외처리도 마찬가지로, 결국엔 프로그래밍을 위한 하나의 도구라고 생각합니다. 이 도구를 적재적소에 활용하는 방법은 사실 잘 모르겠습니다. 앞으로 오픈소스 등 타인의 코드를 보며 어떻게 예외를 처리했는지 유심히 관찰해야겠습니다.