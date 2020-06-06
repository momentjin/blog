최근 프로젝트 규모가 점점 늘어나면서 Event 기반으로 개발을 진행하면서, 실수했던 것이 있었습니다. 어쩌면 주니어 개발자가 자주 실수할 수도 있을 것 같아 경험담을 공유하고자 이 글을 작성했습니다.

이벤트를 어떻게 사용하는지, 어떤 장단점이 있는지는 다루지 않았으니 참고 부탁드립니다.

## 1. @EventListener는 동기적으로 작동한다.

아래 코드는 유저가 회원가입을 하고, 이메일로 환영 인사를 보내는 코드입니다. 회원가입 로직과 이메일 로직의 느슨한 결합을 원하므로 이벤트를 이용해 코드를 작성했습니다.

```java
class UserSignInService {

    public void signIn(User user) {
        this.userRepository.save(user);
        this.eventPublisher(new UserCreatedEvent(user));
    }
}

class UserCreatedEventListener {
    
    @EventListener
    public void handle(UserCreatedEvent event) {
        this.emailService.sendEmail(user.getEmailAddress(), "Hello world!");
    }
}
```

언뜻 보면 문제되는 건 없었지만, EmailService의 오작동으로 인해, 회원가입 시도의 결과까지 오염될 수 있습니다. 예를 들어 emailService API가 굉장히 늦은 응답을 한다면 유저의 사용성을 떨어뜨릴 수 있고, emailService API가 동작하지 않는다면, 회원가입은 정상적으로 했음에도 emailService르 인해 오류를 반환하게 됩니다.  @EventListner는 `동기적으로 작동`하기 때문에 발생하는 문제입니다. (물론, 회원가입과 이메일 송신이 하나의 트랜잭션에서 처리해야하는 비즈니스 룰이 존재한다면, 문제가 되지 않습니다)

별개의 영역에서 처리하고 싶으면 어떻게 해야할까요? @Async를 사용해서 비동기로 작동하도록 만들면 됩니다. 별도의 쓰레드에서 Event가 핸들링되기 때문에, emailService의 어떠한 행동도 영향을 주지 않게됩니다.

```java
class UserCreatedEventListener {
    
    @Aysnc
    @EventListener
    public void handle(UserCreatedEvent event) {
        this.emailService.sendEmail(user.getEmailAddress(), "Hello world!");
    }
}
```

따라서 같은 Event를 사용하더라도, 비즈니스의 룰에 맞게 처리해야될 필요가 있습니다. 같은 트랜잭션 내에서 처리되어야 하는지를 아는 것이 중요하다고 생각합니다.

## 2. @TransactionalEventListener는 비동기가 아니다.

@TransactionalEventListener는 단지, 트랜잭션의 여러 단계(commit 전후, rollback 전후 등)에 따라 이벤트를 핸들링하고 싶을 때 사용하는 어노테이션입니다. 

```java
class UserSignInService {

    @Transactional
    public void signIn(User user) {
        this.userRepository.save(user);
        this.eventPublisher(new UserCreatedEvent(user));
        log.info("회원가입 성공");
    }
}

class UserCreatedEventListener {
    
    @TransactionalEventListener
    public void handle(UserCreatedEvent event) {
        throw new RuntimeException();
        // this.emailService.sendEmail(user.getEmailAddress(), "Hello world!");
    }
}
```

만약 위와 같이 이벤트 핸들링 코드에서 오류가 발생할 때, signIn 메소드의 log는 정상적으로 출력될까요? 출력이 아주 잘 됩니다. 이 떄문에 간혹 @TransactionalEventListener가 비동기로 작동하는 것으로 알고 계시는 분들이 있는 것 같습니다. 

하지만 전혀 그렇지 않습니다. 동일한 쓰레드에서 동작하기 때문에, 이벤트 핸들링하는 로직의 처리 시간에 항상 영향을 받게 됩니다. 따라서 별개의 트랜잭션 + 별개의 쓰레드로 처리하고 싶을 때도 @Async를 사용해야 합니다. 

## 마무리

Spring Framework는 훌륭한 Event 매커니즘을 제공하고 있지만, 이를 제대로 사용하는 것은 오로지 개발자의 몫입니다. 어떤 기술을 `왜` 쓰는지, `어떻게` 쓰는지 아는 것도 중요하지만, `언제` 써야하는지를 아는 것도 중요하다는 것을 다시 한 번 깨달았습니다.