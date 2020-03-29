OAuth2를 연동하면서 생긴 디자인 문제를 해결하면서 정리한 글 입니다.
토이프로젝트에 Kakao Login API를 연동한 과정을 튜토리얼 형식으로 작성한 글 입니다. 이 글에서 다뤄지는 모든 예제 코드는 [Github](https://github.com/momentjin/blog-code/tree/social-login-refac)에서 확인할 수 있습니다.

## 개요

Spring Boot와 Spring Security를 활용해서 REST 방식으로 카카오 로그인 API를 연동하는 방법을 알아봅니다. 튜토리얼은 다음과 같이 총 2편으로 나눠집니다.

(1) [기초](https://momentjin.tistory.com/144) : Spring Boot + Spring Security + JWT를 활용해 카카오톡 로그인 API를 무식하게 연동해보면서 Spring Security의 기초를 알아봅니다.

(2) 심화 : 기초편에서 발생한 설계적 문제들을 해결하는 과정을 다룹니다. 확장성있는 구조로 리팩토링해서 다른 소셜 로그인을 손쉽게 추가하는 법을 배웁니다.

요즘 Open API는 대부분 OAuth2 시스템을 사용한 인증/인가 방식을 사용하기 때문에, 당연히 OAuth2에 대해 알고있어야 합니다. OAuth2를 이해하지 못하면, 아래 글에서 소개하는 모든 내용들을 이해하기 어렵습니다. 생활코딩 등을 통해 OAuth2에 대해 미리 학습하는 것을 꼭!! 추천드립니다.

## 개발 환경

JDK 1.8

Spring Boot 2.x, Spring Security

[spring-security-oauth2-client](https://mvnrepository.com/artifact/org.springframework.security/spring-security-oauth2-client)

## 문제 

지난 번에 [기초](https://momentjin.tistory.com/144)편에서 어떤 문제가 있었을까요? 바로 모든 code가 kakao라는 provider에 의존하고 있다는 점입니다. 아래 코드가 대표적인 예시입니다.

![img](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_refac1.png)

왜 이게 문제일까요? 변경에는 닫혀있고, 확장에는 열려있어야 한다는 객체지향 원칙을 어기고 있기 때문입니다. 확장에 굉장히 취약한 구조이기 때문에, 향후 다른 social provider를 추가하려면 핵심 코드를 계속해서 수정해야 합니다.

물론, 빨간 네모박스에 해당하는 코드를 provider별로 분리한 뒤, 간단한 Factory 클래스를 만들어 객체 생성 책임을 위임한다면 의외로 쉽게 문제를 해결할 수 있습니다. 하지만, 우리는 프레임워크를 사용하기 때문에 최대한 프레임워크를 사용하는게 맞다고 생각합니다. 바퀴는 재발명하는게 아니니까요.

## 해결

### 목표

해결하기에 앞서 목표부터 정의하겠습니다. 우리의 목표는 다음과 같습니다.
> 기존의 Provider에 영향을 주지 않고 새로운 Provider를 추가, 수정, 삭제할 수 있다.

### 문제 해결 방법 찾기

프레임워크 측에서 뭔가 확장할 수 있는 부분이 있을 것 같아서 OAuth2 인증 플로우를 디버깅해보면서 자세히 살펴봤고, 아래와 같은 클래스를 발견했습니다.

```java
// 어떠한 설정도 하지 않았을 때, 기본값으로 사용되는 DefaultOAuth2UserService.class
public class DefaultOAuth2UserService implements OAuth2UserService<OAuth2UserRequest, OAuth2User> {
    
    public OAuth2User loadUser(OAuth2UserRequest userRequest) throws OAuth2AuthenticationException {
        // ... 생략
        ParameterizedTypeReference<Map<String, Object>> typeReference = new ParameterizedTypeReference<Map<String, Object>>(){};

        // OAuth2 회원 정보 조회 API의 Response를 파싱하는 코드
        Map<String, Object> userAttributes = (Map)this.userInfoResponseClient.getUserInfoResponse(userRequest, typeReference);
        GrantedAuthority authority = new OAuth2UserAuthority(userAttributes);
        Set<GrantedAuthority> authorities = new HashSet();
        authorities.add(authority);
        return new DefaultOAuth2User(authorities, userAttributes, userNameAttributeName);
    }
}
```

<img src="https://raw.githubusercontent.com/momentjin/study/master/resource/image/oauth_result_1.png" width="400px">

위 코드와 userAttribute 변수를 캡쳐한 이미지를 보면, API Response를 파싱했다는 사실을 알 수 있습니다. 그렇다면 우리는 OAuth2 타입에 따라 적절한 맵핑 객체를 선택하고 생성하는 방법이 있을 수도 있겠다는 추측을 해볼만 합니다. 

예를 들어 OAuth2 요청 Provider가 Kakao라면 KakaoUserResponse 클래스를 생성하고 맵핑하는 방법이 있을 것 같습니다. 우리가 흔히 API Request Data를 DTO로 맵핑하는 Jackson 처럼요!

우선 관련해서 확장할 수 있는지 한 번 알아봐야겠습니다. 위 코드로 돌아가보면 반환 타입이 `DefaultOAuth2User`입니다. 심지어 Class 이름도 `DefaultOAuth2UserService`입니다. 커스터마이징할 수 있는 여지가 있다는 건 분명해 보입니다.

[Spring 공식 문서](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/oauth2/client/userinfo/package-tree.html)를 살펴봤더니, `CustomUserTypesOAuth2UserService`라는 클래스를 찾았습니다. 이 클래스는 Custom OAuth2User Type을 지원하는 OAuth2UserService의 구현체라고 합니다. 프레임워크가 알아서 제공해주니 이제 갖다 바치면 되겠네요.

### 적용하기

우선 적용하기에 앞서 `CustomUserTypesOAuth2UserService` 클래스를 어떻게 사용하는지 공식 문서를 참고했고, 다음의 글을 보았습니다.

> The custom user type(s) is supplied via the constructor, using a Map of OAuth2User type(s) keyed by String, which represents the Registration Id of the Client.

간단히 해석하면, Custom User Type을 Map에 담아 파라미터로 넘겨서 사용하라는 말이네요. 그리고 Map의 Key는 Client의 Registration ID로 설정하라고 합니다. 무튼 어디에다 설정해야 하는지 한참을 찾다가, 겨우 찾았네요. 코드로 말씀드리는게 빠를 것 같습니다.

```java
// OAuth2 설정 부분 - CustomUserType 추가
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        // authenticate
        http.authorizeRequests()
                .anyRequest().authenticated()
                .and()
                // oauth2 login 설정
                .oauth2Login()
                    // customUserType을 추가하면, 내부적으로 'CustomUserTypesOAuth2UserService' 클래스 사용
                    .userInfoEndpoint()
                        .customUserType(KakaoOAuth2User.class, "kakao");
    }
}

// CustomUserType 추가 - OAuth2User 인터페이스를 구현해서 생성
@Getter
public class KakaoOAuth2User implements OAuth2User {
    private String id;
    private KakaoProperties properties;

    @Override
    public Map<String, Object> getAttributes() {
        Map<String, Object> attrs = new HashMap<>();
        attrs.put("id", this.id);
        attrs.put("name", this.properties.getNickname());

        return attrs;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.singleton(new OAuth2UserAuthority(getAttributes()));
    }

    @Override
    public String getName() {
        return this.id;
    }

    @Getter
    private static class KakaoProperties {
        private String nickname;
    }
}
```

WebSecurityConfig 클래스의 kakao는 KakaoOAuth2User.class를 사용하겠다고 명시했습니다. 이제 Spring Security는 OAuth2 인증시 registrationID로 적절한 Custom User Typㄷ을 찾아 데이터를 맵핑해줄 것입니다.

이제 우리는 OAuth2User를 상속하는 CustomUserType을 만들었기 때문에, 다형성의 특징을 이용할 수 있습니다. 개선한 코드를 봐주세요. 맨 처음 코드보다 변경에는 닫혀있고, 확장에는 열려있다는 사실을 알 수 있습니다. 

![img](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_refac2.png)

## 가정

만약 여러분이 Naver Login을 연동한다고 가정해봅시다. 그러면 여러분들은 현재 구조에서 어떤 설정을 추가적으로 해야할까요? 

(1) CustomOAuthProvider에 provider 정보 추가하기
(2) 구글 유저 정보 API를 맵핑할 수 있는 CustomOAuth2UserType 클래스 만들기
(3) MyOAuth2Configuration 및 WebSecurityConfig 클래스에 새로운 Provider에 대해 설정하기

단 세가지만 해도 충분합니다. 이제 Provider들은 모두 독립적으로 구성되어 있기 때문에 확장과 축소 그리고 변경이 매우 쉽습니다.

## 마무리

사실 아직 개선할 부분이 조금 있습니다만, 여기까지 따라오셨다면 그 다음부터는 스스로 해낼 수 있다고 생각합니다. 디버깅을 통해 코드 분석을 하게 되면, 이해 안되는 구조나 흐름도 잘 이해가 되거든요. 또한 무엇을 확장해야 하는지에 대해 더욱 명확하게 알게 됩니다.

저도 이번 경험을 통해 프레임워크라는게 참 대단하다고 생각했습니다. 개발을 편리하게 할 수 있도록 템플릿은 제공하되, 커스터마이징할 수 있도록 여지를 남겨둔 것이 매력적입니다. 그렇지만 우리 모두 프레임워크는 도구일 뿐이라는 사실과 프레임워크의 밑바탕이 되는 지식이 더 중요하다는 사실을 잊지 맙시다. 저의 경우에는 이렇게 코드 분석을 하면, 그 코드의 디자인 패턴을 기억하려고 노력합니다.

읽어주셔서 감사합니다.

