토이 프로젝트에 Kakao Login API를 연동한 과정을 정리한 글 입니다.

## 개요

현재 rezoom-backend에는 자기소개서 마감일을 알려줄 때, Email만 이용합니다. 더 추가할만한 플랫폼을 생각해보다가 `Kakao 나에게 보내기 API`가 있다는 것을 알게 되어, 우선 Kakao Login API를 연동하기로 했습니다만, 문제가 발생했습니다. 기존에는 토이 프로젝트의 단순성을 위해 Spring Security + id 및 password 기반 인증 + JWT 인증 프로세스를 구축했습니다. 이런 상황에서 OAuth2를 끼워 맟추려니, 튜토리얼을 따라해도 답이 없는 상황이 되었습니다. (물론 어떻게든 끼워 맞출 수는 있지만, 저의 경우에는 프레임워크가 제공해주는 범위 내에서 구현하고 싶었습니다)

이 문제를 해결하기 위해 커스터마이징을 해야 하는데, Spring Security에 대한 이해 없이 불가능할 것 같아 이번 기회에 Spring Security 동작 원리를 코드 수준에서 학습하려고 합니다. 더불어 OAuth2를 연동한 과정도 정리하려고 합니다.

Spring Security에 대한 정의와 동작 과정에 대해 먼저 살펴보고, Kakao Login API를 연동해서 Kakao 나에게 보내기 API를 사용하는 방법을 말씀드리겠습니다.

(본 게시글은 튜토리얼이 아닙니다. 질문이 있으시면 메일 부탁드립니다. 아직 댓글 기능이 없습니다..)

### 개발 환경

- JDK 1.8
- Spring Boot 2.0.3
- Spring Security
    - spring-boot-starter-security 
    - spring-security-oauth2-client

## Spring Security 로그인의 동작 원리

로그인이란? 사용자의 `아이디`와 `비밀번호`를 이용해, 로그인을 시도하는 사용자가 시스템에 등록되었는지 판단하는 과정입니다. Spring Security에서 로그인을 하는 방법은 다양하겠지만(?), 저의 경우에는 UsernamePasswordAuthenticationFilter를 확장한 JWT 기반 로그인 프로세스를 구축했고, 동작 원리는 다음과 같습니다.

1. 다수의 기본 Filter들을 거친 뒤, 로그인에 해당되는 Filter 차례가 되면 FilterChainProxy는 해당 Filter의 doFilter 메소드를 호출합니다. 이 때 사용하는 Filter는 `UsernamePasswordAuthenticationFilter`입니다.

2. `UsernamePasswordAuthenticationFilter`에서 현재 요청이 로그인에 해당하는 요청이 맞는지 확인합니다. 따로 설정을 안했다면, 아래와 같이 생성자에서 정의된 사항을 따릅니다. URI는 /login이고 Http Method가 Post이면 로그인에 해당하는 요청이라 판단해서 Filter의 기능이 동작하게 되는 것 입니다.

    ```java
    public class UsernamePasswordAuthenticationFilter extends AbstractAuthenticationProcessingFilter {
        ... 생략

        public UsernamePasswordAuthenticationFilter() {
            super(new AntPathRequestMatcher("/login", "POST"));
        }
    ```

3. 로그인 요청이 맞다는 것을 확인한 후에는 attemptAuthentication() 메소드를 호출해서, 해당 사용자가 시스템에 등록된 사용자인지 검증하기 위한 준비 작업을 수행합니다. 마찬가지로 따로 설정을 안했다면, 아래와 같이 작동하게 됩니다. 간단히 설명하자면, Request Parameter 중 'username', 'password'가 key인 Parameter를 가져와서 인증 정보(Token)를 생성합니다. 그 후 AuthenticationManager에 인증 정보를 넘겨 사용자가 시스템에 등록되었는지 판단하는 메소드를 호출합니다.

    ```java
        public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) throws AuthenticationException {
            if (this.postOnly && !request.getMethod().equals("POST")) {
                throw new AuthenticationServiceException("Authentication method not supported: " + request.getMethod());
            } else {
                String username = this.obtainUsername(request);
                String password = this.obtainPassword(request);
                if (username == null) {
                    username = "";
                }

                if (password == null) {
                    password = "";
                }

                username = username.trim();
                UsernamePasswordAuthenticationToken authRequest = new UsernamePasswordAuthenticationToken(username, password);
                this.setDetails(request, authRequest);

                // 사용자가 시스템에 등록되었는지 판단하기 위해 AuthenticationManager에 인증 정보를 담아 호출
                return this.getAuthenticationManager().authenticate(authRequest); 
            }
        }
    ```

4. API를 호출한 사용자가 시스템에 등록되었는지 판단하기 위해서 해야할 일은 데이터베이스 등록 정보와 비교해보는 것 입니다. AuthenticationManager는 초기에 설정한 값에 따라 Provider를 결정합니다. DB 등록 정보와 비교하는 경우 DaoAuthenticationProvider를 사용합니다. Provider에 아까 전달 받은 인증 정보를 다시 넘겨 실제 인증을 수행합니다.

    ```java
    public class ProviderManager implements AuthenticationManager, MessageSourceAware, InitializingBean {

        // 단계3의 마지막 라인에서 호출한 메소드
        public Authentication authenticate(Authentication authentication) throws AuthenticationException {
            ... 생략
            // Manager에 등록된 Provider 조회
            Iterator var6 = this.getProviders().iterator();

            // Provider를 순회하며, 각 Provider별로 인증 진행 
            while(var6.hasNext()) {
                AuthenticationProvider provider = (AuthenticationProvider)var6.next();
                if (provider.supports(toTest)) {
                    if (debug) {
                        logger.debug("Authentication attempt using " + provider.getClass().getName());
                    }

                    try {
                        // 실제로 사용자가 유효한지 검증하는 부분
                        result = provider.authenticate(authentication);

                        // 인증 성공시 순회 중단
                        if (result != null) {
                            this.copyDetails(authentication, result);
                            break;
                        }
                    }

                    ... 생략
                }
            }
        }
    }
    ```

5. 이제 넘겨받은 인증정보를 이용해서 Provider는 자신만의 전략으로 인증을 수행합니다. 예를 들어 DaoAuthenticationProvider는 초기에 설정한 userDetailService 객체를 사용해서 DB에 값을 조회한 뒤, 사용자 검증을 수행합니다. (retrieveUser() 메소드)

    ```java
    public Authentication authenticate(Authentication authentication) throws AuthenticationException {
        String username = authentication.getPrincipal() == null ? "NONE_PROVIDED" : authentication.getName();
        boolean cacheWasUsed = true;
        UserDetails user = this.userCache.getUserFromCache(username);
        if (user == null) {
            cacheWasUsed = false;

            try {
                // userDetailService 객체를 이용해 DB에 값을 조회한 뒤, 사용자가 유효한지 검증함
                user = this.retrieveUser(username, (UsernamePasswordAuthenticationToken)authentication);
            } catch (UsernameNotFoundException var6) {
                this.logger.debug("User '" + username + "' not found");
                if (this.hideUserNotFoundExceptions) {
                    throw new BadCredentialsException(this.messages.getMessage("AbstractUserDetailsAuthenticationProvider.badCredentials", "Bad credentials"));
                }

                throw var6;
            }

            Assert.notNull(user, "retrieveUser returned null - a violation of the interface contract");
        }

        ... 생략
        return this.createSuccessAuthentication(principalToReturn, authentication, user);
    }
    ```

6. 1~5 단계가 정상적으로 수행됐으면, 후처리를 진행합니다. JWT 기반의 로그인 처리를 하고 싶으면, 아래와 같이 메소드를 확장해서 JWT를 생성하고 response 객체에 해당 토큰을 담아 클라이언트로 전달하는 코드를 작성하면 됩니다.

    ```java
    @Override
    protected void successfulAuthentication(HttpServletRequest req,
                                            HttpServletResponse res,
                                            FilterChain chain,
                                            Authentication auth) throws IOException {

        String token = JWT.create()
                .withClaim("id", ((CustomUserDetail) auth.getPrincipal()).getUsername())
                .withClaim("name", ((CustomUserDetail) auth.getPrincipal()).getName())
                .withExpiresAt(new Date(System.currentTimeMillis() + SecurityConstants.EXPIRATION_TIME))
                .sign(Algorithm.HMAC512(SecurityConstants.SECRET.getBytes()));

        res.addHeader(SecurityConstants.HEADER_STRING, SecurityConstants.TOKEN_PREFIX + token);
    }
    ```


### 코드 분석 결과

1. 한 개의 요청에 대해 여러 개의 Filter를 거치며 특정 작업을 수행한다.
2. 특정 Filter의 경우, path 및 method가 일치 여부에 따라 Filter가 동작한다.

따라서 OAuth2 전용 Filter를 만들고, OAuth2 매커니즘이 동작하도록 코드를 작성하면 해결할 수 있을 것 같습니다만, 분명히 OAuth2를 제공하는 별도의 프레임워크가 있을 것 입니다. 

따라서 해당 프레임워크의 기능을 추측해본다면 로그인과 마찬가지로 특정 url 및 method와 패턴 매칭을 통해 OAuth2 인증인지 필터링하겠죠? 그 필터가 무엇인지 찾고, 해당 필터에서 시작되는 동작 과정을 분석해서 커스터마이징이 가능한지 살펴보겠습니다.


## Spring OAuth2 Client 동작 원리

> Spring에서 제공하는 OAuth를 사용하려면 의존성을 추가해줘야 합니다. 저는 `spring-security-oauth2-client` 의존성을 추가해줬습니다. 구글링하면 발견할 수 있는 다른 OAuth 의존성은 구버전입니다.

우선 [튜토리얼](https://www.baeldung.com/spring-security-5-oauth2-login)에서 필요한 의존성이 무엇인지 알아보았고, 작동 원리를 간단하게 학습했습니다. 그 후 코드 수준에서의 동작 과정을 분석했습니다.

대다수의 REST 방식의 OAuth2 인증 과정은 다음과 같습니다.
1. 인증 코드 요청
2. (1)에서 받은 인증 코드를 이용해 acesss_token 요청
3. (2)에서 받은 access_token을 이용해 resource 접근 

Spring Security에서 제공하는 OAuth Client 의존성을 추가하면, 위의 흐름들이 전부 자동으로 설정됩니다. 따라서 위 3가지 작업은 거의 커스터마이징이 필요가 없다고 봐도 무방합니다. 이제 본격적으로 위 OAuth2 인증 과정을 통해 OAuth Client가 어떻게 작동하는지 분석해보겠습니다.

1. 인증 코드 요청을 위한 준비 단계

    실제 OAuth2 Provider(Kakao 등)에 인증 코드 요청을 하기 위한 준비 단계입니다. 별도의 코드로 등록한 Provider 정보를 조회해서, OAuth2 Provider의 Authorization Uri를 호출합니다. (Kakao의 경우 https://kauth.kakao.com/oauth/authorize)

    기본 설정 값을 그대로 사용한다면, 이 단계에 들어가기 위해서는 `OAuth2AuthorizationRequestRedirectFilter` 필터가 작동되어야 합니다. 이 필터는 url이 `{domain}/oauth2/authorization/{registrationId}` 패턴과 일치할 때 작동합니다.

    아래 코드는 사전에 미리 등록한 ClientRegistration 정보 중 authorizationUri로 Redirection하는 역할을 맡고 있습니다.

    ```java
    public class OAuth2AuthorizationRequestRedirectFilter {
        private void sendRedirectForAuthorization(HttpServletRequest request, HttpServletResponse response) {
            // ...생략
            // Authorization Code를 발급받기 위해 등록된 정보를 사용해서 redirection하는 코드
            this.authorizationRedirectStrategy.sendRedirect(request, response, redirectUri.toString());
        }
    }
    ```

2. 인증 코드 수신 및 Access Token 요청

    단계1이 정상적으로 동작한다면, OAuth2 Provider의 Authorization Url을 호출할 것이고 이 Authorization Url은 파라미터에 code를 추가해서 callback url로 Redirection할 것 입니다. 
    
    이 Redirection Url을 또 다시 Filter에서 잡아서 처리해야 합니다. 이 때 동작하는 Filter는 `OAuth2LoginAuthenticationFilter`이고, 별도의 설정을 건드리지 않았다면, CallBack Url이 `/login/oauth2/code/*` 이런 패턴과 일치할 때 동작하게 됩니다. 
    
    이 필터는 access_token을 요청하기 위해 각종 데이터를 준비하고, AuthenticationManager(ProviderManager)로 위임하는 역할을 맡고 있습니다. (그리고 ProviderManager가 실제로 OAuth2 인증을 담당하는 Provider인 `OAuth2LoginAuthenticationProvider`가 인증하도록 메소드를 호출합니다)

    ```java
    // access token 요청을 위한 전반적인 처리를 담당하고 있는 Filter
    public class OAuth2LoginAuthenticationFilter extends AbstractAuthenticationProcessingFilter {
        public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) {
            // ... 많이 생략
            // access_token 요청 작업을 ProviderManager로 위임
            OAuth2LoginAuthenticationToken authenticationResult = (OAuth2LoginAuthenticationToken)this.getAuthenticationManager().authenticate(authenticationRequest);
            OAuth2AuthenticationToken oauth2Authentication = new OAuth2AuthenticationToken(authenticationResult.getPrincipal(), authenticationResult.getAuthorities(), authenticationResult.getClientRegistration().getRegistrationId());
            OAuth2AuthorizedClient authorizedClient = new OAuth2AuthorizedClient(authenticationResult.getClientRegistration(), oauth2Authentication.getName(), authenticationResult.getAccessToken());

            // 인증 결과 정보를 저장
            this.authorizedClientService.saveAuthorizedClient(authorizedClient, oauth2Authentication);
            return oauth2Authentication;
        }
    }

    // access token 요청을 실질적으로 수행하는 Provider
    public class OAuth2LoginAuthenticationProvider implements AuthenticationProvider {

        public Authentication authenticate(Authentication authentication) throws AuthenticationException {
            // 생략

            // api를 호출해서 access_token 조회
            OAuth2AccessTokenResponse accessTokenResponse = this.accessTokenResponseClient.getTokenResponse(new OAuth2AuthorizationCodeGrantRequest(authorizationCodeAuthentication.getClientRegistration(), authorizationCodeAuthentication.getAuthorizationExchange()));
            OAuth2AccessToken accessToken = accessTokenResponse.getAccessToken();

            // user 정보를 받아오기 위해 resource 접근
            // ClientRegistration 객체 생성시 설정한 userInfoUri API를 호출한다.
            OAuth2User oauth2User = this.userService.loadUser(new OAuth2UserRequest(authorizationCodeAuthentication.getClientRegistration(), accessToken));
            Collection<? extends GrantedAuthority> mappedAuthorities = this.authoritiesMapper.mapAuthorities(oauth2User.getAuthorities());
            OAuth2LoginAuthenticationToken authenticationResult = new OAuth2LoginAuthenticationToken(authorizationCodeAuthentication.getClientRegistration(), authorizationCodeAuthentication.getAuthorizationExchange(), oauth2User, mappedAuthorities, accessToken);
            authenticationResult.setDetails(authorizationCodeAuthentication.getDetails());
            return authenticationResult;
        }
    }
    ```

3. Resource 접근을 위한 access_token 등 유저 정보의 저장

    아까 살펴본 코드입니다. 코드의 맨 아래 쪽에 `this.authorizedClientService.saveAuthorizedClient()` 메소드를 호출하는 코드가 있습니다. 이 코드는 인증 정보를 저장하기 위한 코드로써, 실제 구현체인 `InMemoryOAuth2AuthorizedClientService`의 메소드(saveAuthorizedClient)를 호출합니다. 클래스 이름만 봐도 알 수 있듯이 InMemory 타입입니다. 따라서 InMemoryOAuth2AuthorizedClientService 클래스가 아닌 별도의 구현체가 필요함을 알 수 있습니다.

    ```java
    // access token 요청을 위한 전반적인 처리를 담당하고 있는 Filter
    public class OAuth2LoginAuthenticationFilter extends AbstractAuthenticationProcessingFilter {
        public Authentication attemptAuthentication(HttpServletRequest request, HttpServletResponse response) {
            // ... 많이 생략
            // access_token 요청 작업을 ProviderManager로 위임
            OAuth2LoginAuthenticationToken authenticationResult = (OAuth2LoginAuthenticationToken)this.getAuthenticationManager().authenticate(authenticationRequest);
            OAuth2AuthenticationToken oauth2Authentication = new OAuth2AuthenticationToken(authenticationResult.getPrincipal(), authenticationResult.getAuthorities(), authenticationResult.getClientRegistration().getRegistrationId());
            OAuth2AuthorizedClient authorizedClient = new OAuth2AuthorizedClient(authenticationResult.getClientRegistration(), oauth2Authentication.getName(), authenticationResult.getAccessToken());

            // 인증 결과 정보를 저장
            this.authorizedClientService.saveAuthorizedClient(authorizedClient, oauth2Authentication);
            return oauth2Authentication;
        }
    }
    ```

### 코드 분석 결과

1. 대부분 자동화가 된 것을 확인했으니, 크게 건드려야할 부분은 없다고 판단된다.
2. authorizedClientService.saveAuthorizedClient() 메소드를 분석한 결과, 기본 설정값에서는 InMemory 상태로 인증 결과를 저장함을 알 수 있다. 따라서 `InMemoryOAuth2AuthorizedClientService.class`를 분석하면 충분히 확장할 수 있어 보인다.
3. `OAuth2LoginAuthenticationFilter` 마지막에 `successfulAuthentication` 메소드가 제공되기 때문에 OAuth2 인증 후 JWT 발급을 위해 이 메소드를 확장하면 된다. (이건 위에서 따로 설명하지 않았습니다ㅜ)

커스터마이징을 위한 준비가 모두 끝났습니다. 이제 커스터마이징 하겠습니다.

## 커스터마이징 시작

### 커스터마이징 목표

커스터마이징에 앞서 OAuth2를 이용한 구현 목표가 무엇인지 짚고 넘어가겠습니다.

1. OAuth2 로그인 후, 사용자의 access_token을 포함한 기타 정보를 데이터베이스에 저장할 수 있어야 한다.
2. OAuth2 로그인 후, 사용자의 id, name 정보를 이용해 JWT를 생성하고 발급할 수 있어야 한다.

### 커스터마이징 과정

#### 데이터베이스에 인증 정보 저장하기

데이터베이스에 인증 정보 저장하는 것은 생각보다 간단합니다. Spring OAuth2 Client 동작 원리-3번 섹션에서 authorizedClientService가 인증 정보를 저장하는 책임을 갖고 있다는 사실을 알았습니다. 해당 객체의 인터페이스는 `OAuth2AuthorizedClientService`입니다. 따라서 확장을 원하는 경우 해당 인터페이스를 구현한 구현 클래스를 생성하면 됩니다.

```java
// 인증 정보 저장을 위한 표준 인터페이스
public interface OAuth2AuthorizedClientService {
    <T extends OAuth2AuthorizedClient> T loadAuthorizedClient(String var1, String var2);

    void saveAuthorizedClient(OAuth2AuthorizedClient var1, Authentication var2);

    void removeAuthorizedClient(String var1, String var2);
}

// 구현 클래스 - 인증 정보를 DB에 저장
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Component
public class MyOAuth2AuthorizedClientSerivce implements OAuth2AuthorizedClientService {

    private MemberRepository memberRepository;

    @Autowired
    public MyOAuth2AuthorizedClientSerivce(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }

    @Override
    public <T extends OAuth2AuthorizedClient> T loadAuthorizedClient(String s, String s1) {
        throw new NotImplementedException();
    }

    @Override
    public void saveAuthorizedClient(OAuth2AuthorizedClient oAuth2AuthorizedClient, Authentication authentication) {

        String providerType = oAuth2AuthorizedClient.getClientRegistration().getRegistrationId(); // kakao
        OAuth2AccessToken accessToken = oAuth2AuthorizedClient.getAccessToken(); // { tokenValue, issuedAt, expiresAt }

        String id = authentication.getName();

        LinkedHashMap<String, Object> properties = (LinkedHashMap<String, Object>) ((DefaultOAuth2User)authentication.getPrincipal()).getAttributes().get("properties");
        String name = (String) properties.get("nickname");

        Member member = Member.builder()
                .id(id)
                .name(name)
                .providerType(providerType)
                .accessToken(accessToken.getTokenValue())
                .expiresAt(LocalDateTime.ofInstant(accessToken.getExpiresAt(), ZoneOffset.UTC))
                .build();

        memberRepository.save(member);
    }

    @Override
    public void removeAuthorizedClient(String s, String s1) {
        throw new NotImplementedException();
    }
}
```

위와 같이 `MyOAuth2AuthorizedClientSerivce` 클래스를 생성해서 @Bean으로 만들었습니다. 이제 `OAuth2LoginAuthenticationFilter` 필터가 해당 Bean을 사용할 수 있도록 아래와 같이 설정해주면 됩니다.
```java
@Bean
public OAuth2AuthorizedClientService authorizedClientService() {
    return new MyOAuth2AuthorizedClientSerivce();
}
```

`MyOAuth2AuthorizedClientSerivce` 클래스는 아래와 같이 2가지 문제가 있습니다. 
1. 카카오라는 Provider에 종속적인 로직
2. Refresh Token 저장을 위해 또 다시 커스터마이징이 필요

우선은 넘어가도록 하겠습니다.. 어쨌든 **목표1**은 달성했습니다!

#### OAuth2 인증 완료시 JWT 발급하기

**문제 발생**

`OAuth2LoginAuthenticationFilter`를 보면 인증을 마친 후 successfulAuthentication() 메소드를 오버라이딩해서 확장하려고 했습니다만, 문제가 생겼습니다. `OAuth2LoginAuthenticationFilter`를 상속하는 CustomFilter를 만들고, Bean으로 설정했더니 `AuthenticationManager` NULL 오류가 발생했습니다.

**원인**
기본 설정을 이용할 때는 `AuthenticationManager` 인터페이스를 구현한 `ProvideManager`에서 OAuth2 관련 3개의 Provider가 내부적으로 생성될 수 있도록 설정 클래스가 동작하는데, 확장하게 되면 설정 클래스가 동작하지 않았던 것이 원인이었습니다. (설정 클래스가 동작하기 전에, Bean을 생성하므로 NULL 참조)

**해결**

엄청난 삽질 결과 SuccessHandler를 설정할 수 있는 Setter를 발견했습니다. "다른 것 처럼 상속해서 확장해야지"라는 편협된 생각이 몇 시간의 삽집을 하게 만들었네요..후.. 반성합니다. (아래 코드는 아직 개선해야할 부분이 많으니 참고만 부탁드립니다)

```java
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    private UserDetailsServiceImpl userDetailsService;
    private BCryptPasswordEncoder bCryptPasswordEncoder;
    private RESTAuthenticationEntryPoint authenticationEntryPoint;

    @Autowired
    public WebSecurityConfig(UserDetailsServiceImpl userDetailsService, BCryptPasswordEncoder bCryptPasswordEncoder,
                             RESTAuthenticationEntryPoint authenticationEntryPoint) {
        this.userDetailsService = userDetailsService;
        this.bCryptPasswordEncoder = bCryptPasswordEncoder;
        this.authenticationEntryPoint = authenticationEntryPoint;
    }

    @Override
    public void configure(WebSecurity web) throws Exception {
        super.configure(web);
    }

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                // ... 생략
                .anyRequest().authenticated()
                .and()
                .oauth2Login()
                    // 이 부분에서 Success Handler를 설정합니다.
                    .successHandler(new MyOAuth2SuccessHandler());
        // ... 생략
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


### 커스터마이징 결과

![결과](https://github.com/momentjin/study/blob/master/resource/image/Spring%20OAuth2%20Client%20Result.png?raw=true)

간단하게 Chrome Debugger를 이용해서 테스트 했습니다. 이미지 아래 부분에 Response Headers 항목을 보시면 정상적으로 JWT를 발급받았음을 확인할 수 있습니다. 아직 개선해야할 부분이 많지만, 코드를 하나씩 분석해서 해냈다는게 참 뿌듯합니다. :)

## 끝으로

code 분석을 통해 동작 과정을 익히면, 구조가 더 쉽게 이해될 수 있다는 점을 깨달았습니다. 앞으로도 단순히 구글링을 통해 얻은 정보들을 복붙하지 말고, Document 또는 코드를 분석하는 역량을 키워야겠습니다.

읽어주셔서 감사합니다. 