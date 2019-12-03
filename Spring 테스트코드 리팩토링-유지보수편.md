이번에 토이프로젝트를 하면서 처음으로 테스트 코드를 작성했습니다. 단위 테스트에 대한 이론적인 지식이나 JUnit을 사용하는 방법을 모른채 진행하다보니 DB, 성능, 코드스멜 등 여러가지 문제점이 많았습니다. 이러한 문제점을 나름대로 개선해본 경험을 공유하려 합니다.

## 리팩토링 목표

크게 2가지 기준을 잡고 리팩토링 계획을 세웠습니다. 

### 유지보수

테스트 코드를 유지보수 관점에서 바라보고 리팩토링하는 과정을 다뤘습니다. 예를 들어 특정 테스트 케이스가 실패했는데, 뭐가 실패했는지 이해가 되지 않늗다면 유지보수성이 좋지 않다고 할 수 있습니다. 그 외 유지보수성이 안 좋은 사례로 하나를 바꾸면 열을 바꿔야 한다거나, 코드의 가독성이 떨어져 무엇을 테스트하는지 불명확한 상황 등이 있겠습니다.

### 성능

테스트 코드를 성능 관점에서 바라보고 리팩토링 해봤습니다. 성능에 해당되는 부분은 지금까지의  경험상 딱 하나 밖에 없습니다. 바로 `피드백 주기` 입니다. 피드백 주기란, 간단하게 테스트 실행 시간입니다. 테스트 코드의 실행 사긴아 시간이 길어지면 길어질수록 생산성이 떨어지기 마련입니다. 

## 유지보수 측면에서의 리팩토링

### 테스트의 목적을 명확하게 변경하자

Effective Unit Testing의 저자는 좋은 테스트 코드를 다음과 같이 정의했습니다.
> 테스트 대상이 **명확**하고, 결과를 신뢰할 수 있으며, 오류 발생시 쉽게 원인을 찾을 수 있는 가독성을 가진 코드

이 구절을 읽고, 제 테스트 코드를 천천히 살펴보니 문제가 바로 보이더군요. 테스트 케이스의 목적이 너무 불분명했습니다. 실제로 제가 작성한 테스트 코드를 예로 들어 설명하겠습니다.

```java
@Test
public void 자기소개서_저장() throws IOException {
    // given
    CoverletterDto.SaveReq req = loadDtoFromJsonFile("CoverletterNew.json", CoverletterDto.SaveReq.class);

    // when
    long coverletterId = service.save(member, req);

    // then
    CoverletterDto.ViewRes findCoverletter = service.getView(member, coverletterId);

    assertEquals(req.getCompanyName(), findCoverletter.getCompanyName());
    assertHasQuestions(findCoverletter, 2, "new");
    assertHasHashtags(findCoverletter.getQuestions(), 2, "new");
}
```

전달받은 requestDto가 DB에 잘 저장되는지 테스트하는 코드입니다. requestDto에 존재하는 데이터가 DB에 저장된 데이터와 일치하는지 검증하고 있습니다. 자기소개서 안에 문항, 문항 안에 태그도 잘 저장되었는지도 검증하고 있습니다.

처음에는 문제가 없는 테스트라고 생각했습니다. 하지만 이 테스트를 하려는 목적이 무엇일까? 라고 심각하게 고민한 결과 자기소개서를 저장할 때 자기소개서, 문항, 해시태그가 모두 저장된다는 것을 검증하고 싶었던 것입니다. 이 결론을 토대로 테스트 케이스를 재구성했더니 아래와 같은 결과가 나왔습니다.

```java
@Test
public void 자기소개서를_저장하면_문항도_저장된다() { ... }

@Test
public void 자기소개서를_저장하면_태그도_저장된다() { ... }

@Test
public void 자기소개서를_저장할때_태그는_중복저장되지_않는다() { ... }
```

'자기소개서를 저장'하는 복합적인 테스트 케이스가 아니라, 위와 같이 한 가지 명확한 테스트 목표를 설정하면 오류가 생겨도 쉽게 오류 원인을 파악할 수 있다는 장점이 있습니다. 예를 들어 위 코드 중 2번째 단위 테스트가 실패한다면, 태그가 올바르게 저장되지 않았다는 사실을 알 수 있습니다. 처음에는 구현 메소드를 테스트했다면, 현재는 개발자의 의도를 테스트하고 있습니다. 단순히 구현된 메소드를 테스트하는 것이 아니라, 개발자의 의도대로 동작하고 있는지 테스트하는 것이 가장 중요합니다.

### 경계를 분리하자

단위 테스트의 목적은 테스트 대상이 정상적으로 동작하는지 검증하는 것 입니다. 즉, 협력하는 주변 객체와는 상관없이 오로지 테스트 대상의 동작만 검증하는 것을 목표로 합니다. 다음 코드는 잘못된 코드입니다. 문제는 무엇일까요?

```java
@Test
public void 조회된_자기소개서가_NULL아면_EntityNotFoundException() {
    // given
    long findCoverletterId = -1;

    // when & then
    assertThrows(EntityNotFoundException.class, () -> {
        service.getView(member, findCoverletterId);
    });
}
```

위 단위 테스트의 테스트 대상은 service.getView() 메소드이고, 존재하지 않는 Entity를 조회했을 때 예외가 발생한다는 것을 검증하는 것을 목표로 합니다.

근데 이 코드는 실제로 Database에 질의하여 Entity를 가져옵니다. service.getView()가 내부적으로 repository.findById()를 호출하기 때문입니다.

따라서 위 단위 테스트는 repository 또는 database 관련 문제가 발생하면 무조건 실패합니다. 분명히 테스트 코드만 보고 단위 테스트의 목적이나 의도를 분명히 알 수 있어야 함에도 불구하고, 이 단위 테스트는 그렇지 못합니다.

```java
@Test
public void 조회된_자기소개서가_NULL아면_EntityNotFoundException() {
    // given
    long findCoverletterId = -1;

    // repository가 항상 Optional.empty()를 반환한다고 설정
    given(repository.findByIdAndMember(findCoverletterId, member))
        .willReturn(Optional.empty());

    // when & then
    assertThrows(EntityNotFoundException.class, () -> {
        service.getView(member, findCoverletterId);
    });
}
```

위 코드는 이전 단위 테스트의 문제점을 개선한 단위 테스트입니다. repository.findByIdAndMember()가 항상 빈 객체를 반환한다고 설정했기 때문에 데이터베이스나 repository 객체와는 `독립적으로`으로 단위 테스트를 수행할 수 있습니다.

또 다른 예시가 있습니다. MultipartFile을 인자로 받아 로직을 수행하는 convertFromFileToCoverletter() 메소드가 있습니다. 이 메소드는 내부적으로 MultipartFile을 file로 변환 후 객체로 변환하는 로직을 수행하고 이를 DB에 저장하는 역할을 담당하고 있습니다.

아래는 맨 처음 작성했던 코드입니다.

```java
@Test
public void 텍스트파일_변환_테스트_성공() {
    // given
    File file = new File(..);
    MultipartFile multipartFile = convertFile(file);
    MultipartFile[] multipartFiles = { multipartFile };

    // when
    converterService.convertFromFileToCoverletter(member, multipartFiles);

    // then
    // ...
    // db에서 저장된 객체를 조회한 뒤, 내용을 검증하는 코드가 있었음
}
```

이 코드의 문제점은 convertFile이라는 별도의 메소드에 종속되었다는 점입니다. convertFile에 문제가 생긴다면 이 단위테스트는 실패하게 되겠죠. 하지만 이 단위 테스트의 목적은 텍스트 파일이 객체로 변환되서 DB에 저장되는지 검증하는 것입니다. 따라서 converFile 메소드와는 독립적으로 만들어야할 필요가 있습니다. 아래 코드는 위 코드를 개선한 단위 테스트입니다.

```java
public class MultipartFileStub implements MultipartFile {

    @Override
    public String getName() {
        return "A사 2019 하반기 신입.txt";
    }

    @Override
    public String getOriginalFilename() {
        return "A사 2019 하반기 신입.txt";
    }

    @Override
    public byte[] getBytes() {
        String fileContents = "...";
        return fileContents.getBytes();
    }

    ... 생략
}

 @Test
public void 텍스트파일_변환_테스트_성공() {
    MultipartFile[] multipartFiles = { new MultipartFileStub() };

    // when
    converterService.convertFromFileToCoverletter(member, multipartFiles);

    // then
    verify(coverletterRepository, atLeastOnce()).save(any(Coverletter.class));
}
```
MultipartFile을 구현한 Stub 객체를 만들었습니다. 작성하고 있는 단위 테스트는 MultipartFile이 정상적인지에 대해 전혀 관심이 없기 때문에 항상 정상적인 MultipartFile을 생성하도록 만든 것 입니다. 이렇게 하면 File을 MultipartFile 타입으로 변환하지 않아도 됩니다.

## 성능 측면에서의 리팩토링

지금까지 저는 단위 테스트할 때 항상 Spring의 모든 Context를 로드했었습니다. 그래서 단위 테스트를 한 번 실행시킬 때마다 시간이 오래걸리곤 했습니다. 그래서 필요한 Context만 로드하도록 수정했습니다. 그 결과 POJO 클래스를 테스트하는 것만큼 단위 테스트의 속도가 빨라졌습니다. ~~당연한건데, 처음이라 잘 몰랐습니다 ;)~~

```java
// 변경 전
// @SpringBootTest 어노테이션으로 인해, Spring의 모든 Context가 로드된다.
@SpringBootTest
@ExtendWith(SpringExtension.class)
public class MemberServiceTest {

    @Autowired
    private MemberService service;

    @Autowired
    private MemberRepository memberRepository;

    @Autowired
    private PasswordEncoder encoder;
    
    ...
}

// 변경 후
// MemberService.class만 로드되도록 수정
@SpringBootTest(classes = {MemberService.class})
@ExtendWith(SpringExtension.class)
public class MemberServiceTest {

    @Autowired
    private MemberService service;

    // MemberService에서 필요한 의존성은 Mock으로 대체
    
    @MockBean
    private MemberRepository memberRepository;

    @MockBean
    private PasswordEncoder encoder;
    
    ...
}
```
