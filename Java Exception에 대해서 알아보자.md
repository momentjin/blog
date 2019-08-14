# Java Exception

> Java 언어를 지금까지 많이 해왔다고 생각했지만, 예외 처리에 대해 제대로 알아보려고 했던 적은 없었다. 지금이라도 생각난 김에 자바 예외처리에 대해 한 번 정리했다.

## Exception ?

예외란, 프로그램 실행 도중 발생하는 문제 상황을 말합니다. 

### Exception 종류

Exception의 종류는 크게 `Checked Exception`과 `Unchecked Exception`으로 나뉩니다. 

Checked Exception은 예외에 대한 처리를 반드시 해야합니다. 즉 예외를 던지든지, 예외를 처리하든지 둘 중 하나는 반드시 해야합니다.

Unchecked Exception은 예외 처리를 해도 되고 안해도 됩니다.

