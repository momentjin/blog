토이프로젝트에 Kakao Login API를 연동한 과정을 튜토리얼 형식으로 작성한 글 입니다. 이 글에서 다뤄지는 모든 예제 코드는 [Github]()에서 확인할 수 있습니다.

## 개요

Spring Boot와 Spring Security를 활용해서 REST 방식으로 카카오 로그인 API를 연동하는 방법을 알아봅니다. 튜토리얼은 다음과 같이 총 2편으로 나눠집니다.

(1) 기초 : Spring Boot + Spring Security + JWT를 활용해 카카오톡 로그인 API를 무식하게 연동해보면서 Spring Security의 기초를 알아봅니다.

(2) [심화]() : 기초편에서 발생한 설계적 문제들을 해결하는 과정을 다룹니다. 확장성있는 구조로 리팩토링해서 다른 소셜 로그인을 손쉽게 추가하는 법을 배웁니다.

요즘 Open API는 대부분 OAuth2 시스템을 사용한 인증/인가 방식을 사용하기 때문에, 당연히 OAuth2에 대해 알고있어야 합니다. OAuth2를 이해하지 못하면, 아래 글에서 소개하는 모든 내용들을 이해하기 어렵습니다. 생활코딩 등을 통해 OAuth2에 대해 미리 학습하는 것을 꼭!! 추천드립니다.

## 개발 환경

JDK 1.8

Spring Boot 2.x, Spring Security

[spring-security-oauth2-client](https://mvnrepository.com/artifact/org.springframework.security/spring-security-oauth2-client)

## Spring Security 로그인의 동작 원리

먼저 Security에서 제공하는 로그인의 동작 원리를 이해해야 합니다. 결국 소셜 로그인 또한 로그인이기 때문입니다. 

Spring Security는 기본적으로 필터 기반으로 동작합니다. 클라이언트의 Http Request가 특정 Filter의 조건에 부합하면, 그 Filter가 동작합니다. 로그인도 마찬가지입니다. Spring Security에는 `UsernamePasswordAuthenticationFilter`라는 필터가 있고, 해당 클래스의 내부를 탐색해보면 다음과 같이 실행조건이 있는 것을 확인할 수 있습니다.

```java
public UsernamePasswordAuthenticationFilter() {
    super(new AntPathRequestMatcher("/login", "POST"));
}
```

그렇다면, OAuth2도 별도의 filter를 제공할 수도 있겠다는 생각을 해볼 수 있습니다. spring oauth2 client 라이브러리를 추가하면, 관련된 filter를 사용할 수 있으니 의존성을 추가해주세요.

[Maven Repository 바로가기](https://mvnrepository.com/artifact/org.springframework.security/spring-security-oauth2-client) 

## Kakao Open API 설정

카카오 Login API를 사용하려면 client Id, Secret 정보가 필요합니다. kakao open api에서 앱을 만든 뒤 플랫폼에 웹을 추가하고, 다음과 같이 client ID와 Secret 값을 확인해주세요.

플랫폼은 웹, 사이드 도메인은 localhost:8080으로 추가해줍니다.

![img](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_kakao_setting4.png)

redirect url도 아래와 같이 설정해주세요.

![img](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_kakao_setting3.png)

REST API키는 client ID로 사용됩니다.

![img](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_kakao_setting1.png)

아래는 Secret Key 입니다.

![img](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_kakao_setting2.png)


## Spring OAuth2 Client 동작 원리

먼저 동작 원리를 알아보기전에 간단히 카카오 API를 Spring Configuration에 등록해봅시다.

우선 Spring에 OAuth2 Login을 사용하겠다고 알려주기 위해 다음과 같이 클래스를 만들고 설정해줍니다.

```java
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .antMatchers("/oauth2/**").permitAll()
                .anyRequest().authenticated()
                .and()
                .oauth2Login();
    }
}
```

그리고 kakao API에 대한 정보를 다음과 같이 클래스를 만들고 설정해줍니다.

```java
public enum CustomOAuthProvider {

    KAKAO {
        @Override
        public ClientRegistration.Builder getBuilder() {
            return getBuilder("kakao", ClientAuthenticationMethod.POST)
                    .scope("profile", "talk_message") // 요청할 권한
                    .authorizationUri("https://kauth.kakao.com/oauth/authorize") // authorization code 얻는 API
                    .tokenUri("https://kauth.kakao.com/oauth/token") // access Token 얻는 API
                    .userInfoUri("https://kapi.kakao.com/v2/user/me") // 유저 정보 조회 API
                    .clientId("69779556a1e86bbc4883911ac6062eb8")
                    .clientSecret("tm0oPlUDEyltKNYEpcjvtse5PGmPz5T5")
                    .userNameAttributeName("id") // userInfo API Response에서 얻어올 ID 프로퍼티
                    .clientName("Kakao"); // spring 내에서 인식할 OAuth2 Provider Name
        }
    };

    private static final String DEFAULT_LOGIN_REDIRECT_URL = "{baseUrl}/login/oauth2/code/{registrationId}";

    protected final ClientRegistration.Builder getBuilder(String registrationId,
                                                          ClientAuthenticationMethod method) {

        ClientRegistration.Builder builder = ClientRegistration.withRegistrationId(registrationId);
        builder.clientAuthenticationMethod(method);
        builder.authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE);
        builder.redirectUriTemplate(CustomOAuthProvider.DEFAULT_LOGIN_REDIRECT_URL);
        return builder;
    }

    public abstract ClientRegistration.Builder getBuilder();
}
```

이제 설정을 마쳤으니 본격적으로 실습해봅니다. 하지만 소셜 로그인을 하려면 우선 OAuth2에 대해 알아야 합니다. OAuth2에 대해 잘 모르신다면, 한 번쯤은 OAuth2에 대한 학습을 추천드립니다. 

대다수의 REST 방식의 OAuth2 인증 과정은 다음과 같습니다.
1. 인증 코드 요청
2. (1)에서 받은 인증 코드를 이용해 access_token 요청
3. (2)에서 받은 access_token을 이용해 resource 접근 

Spring Security에서 제공하는 OAuth Client 의존성을 추가하면, 위의 흐름들이 전부 자동으로 설정됩니다. 이제 OAuth Client가 어떻게 작동되는지 실제 Flow와 동일한 순서로 분석해보겠습니다.

### 1. 인증 코드 요청

OAuth2 로그인 플로우의 첫 번째 단계는 인증코드 요청이라고 했습니다. Spring Security와 OAuth2 프레임워크를 사용해서 자신이 등록한 Kakao API의 인증코드 API를 호출하려면 어떻게 해야할까요? 해당 역할을 하는 EndPoint를 알아야하고, 그 EndPoint는 Filter입니다. 해당 역할을 하는 Filter는 `OAuth2AuthorizationRequestRedirectFilter`입니다. 이 필터는 아래와 같은 조건을 만족할 때 실행되는 필터입니다.

```java
public class OAuth2AuthorizationRequestRedirectFilter extends OncePerRequestFilter {
	public static final String DEFAULT_AUTHORIZATION_REQUEST_BASE_URI = "/oauth2/authorization";
}
```

구체적인 실행 방식은 코드를 탐색해보시면 알겠지만, `localhost:8080/oauth2/authorization/kakao`로 호출하면, kakao라는 registrationId로 등록된 설정을 가져와서, redirection을 수행합니다. 이미 우리는 kakao라는 OAuth2Provider를 추가했기 때문에 Spring은 스스로 설정 정보를 찾아 인증코드를 호출할 준비를 합니다. 다음 코드를 보시면 이해가 되실 겁니다.

다음 코드는 `OAuth2AuthorizationRequestRedirectFilter` 클래스의 실질적인 실행 로직이 담겨있는 doFilterInternal 메소드의 일부입니다. this.authorizationRequestResolver가 registrationId인 kakao값으로 설정 정보를 조회합니다.

```java
@Override
protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
        throws ServletException, IOException {

    try {
        OAuth2AuthorizationRequest authorizationRequest = this.authorizationRequestResolver.resolve(request);
        if (authorizationRequest != null) {
            this.sendRedirectForAuthorization(request, response, authorizationRequest);
            return;
        }
    } catch (Exception failed) {
        this.unsuccessfulRedirectForAuthorization(request, response, failed);
        return;
    }

    // ... 생략
}
```

위 코드는 최종적으로 인증 코드를 얻기 위해 호출할 API 주소를 만들고, 해당 주소로 redirection 합니다. `sendRedirectForAuthorization` 메소드를 참고하시면 이러한 로직이 담겨 있습니다. 아래는 인증 코드를 얻기 위해 Spring에서 만든 API 주소입니다.

`https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=69779556a1e86bbc4883911ac6062eb8&scope=profile%20talk_message&state=Lf_Z7buQNi87ryfmqOMtJ497_9hziNqpqRR5M3QxZjA%3D&redirect_uri=http://localhost:8080/login/oauth2/code/kakao`

여기까지 잘 따라오셨다면, 브라우저를 열고 주소창에 `http://localhost:8080/oauth2/authorization/kakao`을 입력해봅시다. 그러면 카카오톡 로그인 페이지가 나올 것입니다. 로그인을 하게 되면, 카카오쪽에서 우리가 처음에 등록한 callBack URL인 redirect_uri를 호출해줄 것입니다.

### 2. Access Token 요청

OAuth2 인증 플로우의 2번째 과정인 Access Token 요청입니다. 첫 번째 과정인 Code를 요청할 때 redirect uri를 보냅니다. 이 redirect_uri를 어떻게 처리해서 acesss token을 얻어와야 할까요? 직접 controller를 만들어서 카카오의 access token을 획득하는 API를 호출해야 할까요? 우리는 프레임워크를 이용하기 때문에 당연히 직접 만들지 않습니다!

해당 역할을 하는 Filter는 바로 `OAuth2LoginAuthenticationFilter` 입니다. 이 필터는 다음과 같은 조건에서 작동합니다. 보시면 아시겠지만, redirect_uri와 패턴이 일치하다는 사실을 알 수 있습니다.

```java
public class OAuth2LoginAuthenticationFilter extends AbstractAuthenticationProcessingFilter {
	public static final String DEFAULT_FILTER_PROCESSES_URI = "/login/oauth2/code/*";
}
```

이 필터를 디버깅 해서 access token을 잘 가져오는지 확인해보겠습니다. 다시 처음으로 돌아가서 EndPoint를 호출해봅시다. 브라우저를 열고 주소창에 `http://localhost:8080/oauth2/authorization/kakao`을 입력해서 해당필터가 실행되는 시점에 Break Point를 걸고 확인하면 됩니다.

![oauth2_debug.png](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_debug.png)

authenticationResult 값을 살펴보면 아래와 같습니다. access token 뿐만 아니라, 카카오 user 정보 조회 API를 통해 호출한 정보도 갖고 있는 것을 확인할 수 있습니다.

<div style="text-align: center;">
    <img src="https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_response.png" width="400">
</div>


### 3. Access Token을 사용해서 사용자의 resource 사용하기

만약 우리의 서비스에 카카오 API 중 `나에게 보내기 API`를 사용하고 싶다고 가정해봅시다. 이 API를 사용하기 위해선 당연히 access token이 필요합니다. 따라서 소셜 API를 호출하고 싶다면, access token을 계속 알고 있어야 한다는 것을 알 수 있습니다. 즉, access token을 저장해야 합니다.

아까 디버깅한 `OAuth2LoginAuthenticationFilter` 클래스의 `attemptAuthentication` 메소드 아래 부분을 살펴보면, `this.authorizedClientService.saveAuthorizedClient(authorizedClient, oauth2Authentication);` 라는 코드가 보일 것입니다. 이 코드가 인증정보를 저장하는 역할을 담당하고 있습니다. 

위 코드를 호출하는 인터페이스는 `OAuth2AuthorizedClientRepository`이며, Default 구현체는 `InMemoryOAuth2AuthorizedClientService` 입니다. 클래스명에서 알 수 있듯이, 메모리 전략을 사용합니다. 우리는 데이터베이스에 저장해야 하므로 별도의 구현체가 필요합니다.

생각보다 간단하게 데이터베이스에 인증 정보를 저장할 수 있습니다. 별도의 구현체를 우리가 직접 만들면 되기 때문입니다. `OAuth2AuthorizedClientService` 인터페이스를 구현한 구현체를 만들어봅시다.

```java
// 인증 정보 저장을 위한 표준 인터페이스
public interface OAuth2AuthorizedClientService {
    <T extends OAuth2AuthorizedClient> T loadAuthorizedClient(String var1, String var2);
    void saveAuthorizedClient(OAuth2AuthorizedClient var1, Authentication var2);
    void removeAuthorizedClient(String var1, String var2);
}

// 직접 생성한 구현 클래스 - 인증 정보를 DB에 저장
@Service
public class MyOAuth2AuthorizedClientService implements OAuth2AuthorizedClientService {

    @Autowired
    private MemberRepository memberRepository;

    @Override
    public void saveAuthorizedClient(OAuth2AuthorizedClient oAuth2AuthorizedClient, Authentication authentication) {
        String providerType = oAuth2AuthorizedClient.getClientRegistration().getRegistrationId();
        OAuth2AccessToken accessToken = oAuth2AuthorizedClient.getAccessToken();

        OAuth2User oauth2User = (OAuth2User) authentication.getPrincipal();
        String id = String.valueOf(oauth2User.getAttributes().get("id"));
        String name = (String) ((LinkedHashMap) ((LinkedHashMap) oauth2User.getAttribute("kakao_account")).get("profile")).get("nickname");

        Member member = new Member(id, name, providerType, accessToken.getTokenValue());
        memberRepository.save(member);
    }

    @Override
    public <T extends OAuth2AuthorizedClient> T loadAuthorizedClient(String s, String s1) {
        throw new NotImplementedException();
    }

    @Override
    public void removeAuthorizedClient(String s, String s1) {
        throw new NotImplementedException();
    }
}
```

위와 같이 `MyOAuth2AuthorizedClientService` 클래스를 생성한 뒤, `OAuth2LoginAuthenticationFilter` 필터가 해당 Bean을 사용할 수 있도록 설정해주시면 됩니다.

```java
@Bean
public OAuth2AuthorizedClientService authorizedClientService() {
    return new MyOAuth2AuthorizedClientSerivce();
}
```

`MyOAuth2AuthorizedClientSerivce` 클래스는 문제가 있습니다. 카카오라는 Provider에 종속적인 로직이 그대로 담겨 있다는 것입니다. 만약에 facebook, google, naver 등 여러 종류의 social 로그인을 추가한다고 가정해봅시다. 그러면 if문으로 분기처리하는 로직이 필요하고, 새로운 provider가 추가될 때마다 코드가 수정되어야 합니다.

하지만 걱정 마세요! [심화편]()에서 확장하기 쉬운 구조로 리팩토링하는 방법을 알려드리겠습니다.

## 로그인 상태 처리 

클라이언트가 소셜 로그인을 수행했으므로, 로그인이 되었다는 상태를 클라이언트 또는 서버에서 알고 있어야 합니다. 아시다시피 로그인 상태를 서버에서 관리하는 전략은 보통 세션을 사용하고, 클라이언트가 관리하는 전략은 토큰이죠. 

Spring Security는 기본적으로 세션 기반으로 동작합니다. 즉, 로그인 상태를 서버에서 관리합니다. 하지만, stateless로 만들고 싶은 경우가 있습니다. 이럴 때는 OAuth2 인증 처리 후 실행되는 success handler를 커스터마이징하면 됩니다.

아래와 같이 handler를 만들고 security config에 추가해줍니다.

```java
@EnableWebSecurity
@RequiredArgsConstructor
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .anyRequest().authenticated()
                .and()
                .oauth2Login()
                    // 이 부분에서 Success Handler를 설정합니다.
                    .successHandler(new MyOAuth2SuccessHandler());
    }
}

public class MyOAuth2SuccessHandler implements AuthenticationSuccessHandler {

    @Override
    public void onAuthenticationSuccess(HttpServletRequest req, HttpServletResponse res, Authentication authentication) {
        String id = authentication.getName();

        LinkedHashMap<String, Object> properties = (LinkedHashMap<String, Object>) ((DefaultOAuth2User)authentication.getPrincipal()).getAttributes().get("properties");
        String name = (String) properties.get("nickname");

        String token = JWT.create()
                .withClaim("id", id)
                .withClaim("name", name)
                .withExpiresAt(new Date(System.currentTimeMillis() + SecurityConstants.EXPIRATION_TIME))
                .sign(Algorithm.HMAC512(SecurityConstants.SECRET.getBytes()));

        res.addHeader(SecurityConstants.HEADER_STRING, SecurityConstants.TOKEN_PREFIX + token);
    }
}
```

눈치채셨을지도 모르지만, 이 역시 kakao라는 provider에 의존하는 문제가 있습니다만 [심화편]()에서 이 문제를 해결할 것입니다.


## 저장된 인증 정보를 사용하는 방법

드디어 Spring OAuth2 Client의 동작 원리를 모두 살펴봤습니다. 하지만 이 다음부터 어떻게 해야할지 모르시는 분들도 계실 것 같습니다. 우선 Spring Security는 인증을 하면 인증 정보를 SecurityContextHolder 클래스를 통해 메모리에 저장합니다. 

현재 세션 Key로 메모리에 저장된 인증 정보를 꺼내서 무언가를 처리하려 할 때는 다음과 같이 하면 됩니다. Spring에서 알아서 인증 정보를 바인딩해줍니다.

![oauth2_using.png](https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/oauth2_using.png)

이 외에 코드로 얻는 방법이 있습니다.

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();
```

## 마무리

프레임워크라는 것이 편리하기도 하지만, 제대로 사용하는 것도 어렵고 심지어 어떻게 사용해야 하는지도 모르는 경우가 태반입니다. 이런 상황에서는 먼저 공식 문서, 튜토리얼을 참고하는 것이 제일 좋고, 그 이후에는 엔드포인트부터 하나씩 Break Point를 역순으로 잡으며 디버깅하는 것을 추천드립니다.

간단하게나마 Spring Security + OAuth2 Client를 활용해 카카오 로그인 API를 연동해보았습니다. 연동 과정에서 구조적인 문제가 있었는데 이는 다음 편에서 해결해보도록 하겠습니다.

감사합니다 :)