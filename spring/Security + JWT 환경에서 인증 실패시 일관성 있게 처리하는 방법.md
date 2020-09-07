
안녕하세요. 오늘은 Spring Security + JWT 기반 인증 사용시, 예외를 일관성있게 다루는 법에 대해 소개하고자 합니다. 

## 문제

토이 프로젝트를 하면서 항상 토큰(JWT) 기반의 인증 시스템을 사용해서 프로젝트를 구성했습니다. 하지만 Security에서 발생한 오류는 @ControllerAdvice를 통해 전역에서 예외를 핸들링할 수 없어서 일관성있게 처리할    수 없는 문제가 있었습니다.

**JWT 검증 필터에서 예외를 일관성있게 처리하기 위해 억지로 사용한 방법**

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/edd7cbdfba1eb9996191995ba56ea19b7a087096/resource/image/jwt-auth-1.png" >
</div>

<br>

**@ControllerAdvice를 통해 API 예외를 일관성있게 처리하는 방법**

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/edd7cbdfba1eb9996191995ba56ea19b7a087096/resource/image/jwt-auth-2.png" >
</div>

<br>

위 코드를 보시면, GlobalExceptionHandler.java에 존재하는 코드와 동일하게 JWT 예외를 JWTAuthorizationFilter에서 핸들링합니다. 중복된 코드만으로도 벌써 불편한 감정을 불러일으킵니다.

> Spring Security에서 발생한 예외가 @ControllerAdvice를 통해 핸들링되지 않는 이유는, 실제 API가 동작하는 로직과 Security가 동작하는 로직의 CONTEXT가 다르기 때문입니다. 자세한 건 MVC 구조와 Security 구조를 참고해주세요!

<br>

## 해결

결론부터 말씀드리면, `HandlerExceptionResolver` 라는 Bean을 사용하면 문제를 해결할 수 있습니다. 다음과 같이 코드를 작성하면 @ControllerAdvice에서 동일하게 핸들링할 수 있습니다.

**HandlerExceptionResolver를 사용하도록 변경**

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/edd7cbdfba1eb9996191995ba56ea19b7a087096/resource/image/jwt-auth-3.png" >
</div>

<br>

에제 @ControllerAdvice Bean에서 자신이 원하는 Exception 타입으로 핸들링한다면, 인증 처리에 대한 예외만 담당해서 처리할 수 있습니다. (해당 오류에 한해서만 HttpStatus 401을 반환하는 등)

## HandlerExceptionResolver의 작동 원리

// 정말 별거 없으니 읽지 않으셔도 됩니다..

HandlerExceptionResolver는 어떤 식으로 @ControllerAdvice가 선언된 Bean에 예외 핸들링 처리를 위임하는지 궁금해져서 디버깅을 해봤습니다.

정말 간단히 말씀드리면, 먼저 HandlerExceptionResolver 객체는 내부적으로 `ExceptionHandlerExceptionResolver`에 요청 전달합니다. 바로 이 객체에서 @ControllerAdvice로 요청을 전달합니다.

애플리케이션 초기화시, `ExceptionHandlerExceptionResolver` 객체는 @ControllerAdvice로 등록된 Bean을 찾고 멤버변수에 저장을 해놓기 때문에, 요청을 전달할 수 있었던 것 입니다.

<br>

## 마무리

일관성을 유지하는 것은 정말 수없이 강조해도 모자랄만큼 중요하다고 생각합니다.

읽어주셔서 감사합니다.