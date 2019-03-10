# Design Pattern
> 디자인 패턴이란, 소프트웨어를 개발하는 과정에서 자주 발생하는 설계 상의 문제를 해결할 수 있는 방법을 일종의 패턴 형태로 만든 것이다.

## Design Pattern을 배우는 이유
소프트웨어는 개발도 중요하지만, 유지보수가 더 중요하다. 서비스 출시만 해놓고 지속적으로 개선하지 않는다면 그 서비스는 도태되기 때문이다. 유지보수는 어렵지 않다. 예를 들어 일련의 로직에 예외사항을 부여하고자 한다면, if문을 사용해서 분기처리하는 것만으로도 가능하다. 하지만 고객의 요구사항으로 인해 예외가 점점 늘어나서 위와 같이 예외사항을 if문으로만 적용할 경우, 테스트나 코드 수정이 어렵고, 새롭게 협업할 동료 개발자는 그 코드를 해석하기 매우 힘들다. <br>

디자인패턴은 앞서 언급한 문제들을 어느 정도 해결할 수 있다. 공식적으로 사용하는 용어 덕분에 어떤 클래스의 역할이 무엇인지 이름만 봐도 짐작할 수 있고, 구조적으로 변경하기 쉬운 설계 덕분에 테스트나 수정도 수월하며, 가독성 또한 뛰어나기 때문에 원활한 협업을 가능케한다. 이러한 이유로 디자인패턴을 배우고자 한다. <br>

## Index 
> 해당 pattern을 학습만 했으면 첫째 칸에 [o] 표시 <br>
> 해당 pattern을 uml까지 그리며 자신있게 설명할 수 있으면 둘째 칸에 [o] 표시

- [o][x] [Strategy pattern](./strategy-pattern.md)
- [o][x] [Decorator pattern](./decorator-pattern.md)
- [x][x] [Observer pattern](./observer-pattern.md)
- [x][x] [Factory pattern](./factory-pattern.md)
- [o][x] [Command pattern](./command-pattern.md)

## Reference
- Head First Design Patterns
