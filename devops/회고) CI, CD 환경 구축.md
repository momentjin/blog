
회사에서 담당하고 있는 프로젝트의 빌드와 배포 방식을 변경하기 위한 과정을 간단히 회고하고 정리한 글입니다.

개발환경은 다음과 같습니다.

- Java 8 + Spring Boot 2.x
- Gradle 기반 Multi Project (Mono Repository)
- ElasticBeanstalk

## 개요

이 글은 다음과 같이 구성되었습니다.

1. 지금까지의 배포 방식과 그에 따른 문제점
2. 문제 해결 방안
3. Jenkins 구축 과정
4. 마무리

## 1. 지금까지의 배포 방식, 현 배포 방식의 문제

#### 지금까지의 배포 방식

프로젝트를 처음 시작했을 때는 ElasticBeanstalk Console에서 직접 빌드된 파일을 배포하는 방식이었습니다. 그 때는 단일 프로젝트였고, 혼자 개발했기에 딱히 큰 문제는 없었습니다.

이후 ElasticBeanstalk CLI와 Shell Script를 사용해서 배포 과정을 개선했습니다. 점점 프로젝트 규모가 커짐에 따라 멀티 프로젝트로 구성해서 모듈을 나누면서 ElasticBeanstalk Console에서 프로젝트별 빌드된 파일을 배포하는 것이 귀찮고, 번거로웠기 때문입니다.  

#### 현 배포 방식의 문제

**근거없는 배포**

멀티 프로젝트의 경우, ElasticBeanstalk CLI를 사용하게 되면, 원격 저장소 기준 최신 commit으로 배포하기가 어렵습니다. 그래서 항상 로컬 저장소 기준으로 빌드하고, 이를 배포하게 됩니다. 

따라서 모든 기준이 local이 되므로 함께 개발하는 동료들과 충돌이 날 가능성도 많고 배포의 신뢰성과 일관성도 떨어집니다. 뿐만아니라 누가, 언제 배포했는지 추적하기가 어렵습니다.

**EB-CLI**

이 부분은 좀 오버일 수 있지만, 다른 동료가 배포하려면 ElasticBeanstalk CLI를 셋팅해야 합니다. 셋팅 작업이 오래걸리지는 않지만, 일일히 셋팅하는 자체가 비효율적이라고 생각했습니다. 

그 외 많은 문제가 있었지만, 너무 창피해서 말을 못하겠네요 ㅋ

## 2. 문제 해결 방안

원격저장소의 최신 커밋 기준으로 빌드하고 배포할 수 있는 방법은 아래와 같았습니다.
- AWS CodePipeline
- Shell Script + AWS CLI
- Jenkins + Shell Script + AWS CLI

저는 Jenkins를 선택했습니다. AWS CodePipeline은 멀티프로젝트 환경에서 셋팅하기  번거로웠습니다. Project와 각 Project의 Profile별로 셋팅을 해줘야하고, 이를 또 각각의 ElasticBeanstalk에 배포해야 했습니다. 꽤 시간을 들였지만 결국 포기했습니다.

Shell Script + AWS CLI를 사용하면 생각보다 편리했습니다. 누가 배포했는지 추적하기 위해 배포 파일명을 커스터마이징하는 것도 가능했고, 로컬이 아닌 원격저장소 기준으로 빌드했기에 위에서 언급한 문제들을 충분히 해결해주었습니다. 하지만, 동료 개발자가 또 AWS CLI를 설치해야 하는 번거로움이 있었고, 이것 역시 기록이 별도로 남지 않았기에 다른 방법을 알아봤습니다.

Jenkins를 선택한 이유는 다음과 같습니다.
- 추적이 편리합니다. 누가, 언제 배포했는지 한 눈에 알 수 있습니다. 
- 셋팅이 필요 없습니다. 개발자는 그저 Jenkins 페이지에서 빌드 버튼만 누르면 됩니다.


## 3. Jenkins 구축 과정

저는 [jojoldu님의 Jenkins 셋팅 글](https://jojoldu.tistory.com/290?category=777282)을 기반으로, 커스터마이징해서 CI/CD 환경을 구축했습니다. 따라서 Jenkins 설치부터, 멀티 프로젝트 기반 ElasticBeanstalk 배포 과정은 위 글을 보시는 것을 강력히 추천드립니다. 여기서는 어떤 것을 커스터마이징했는지만 소개하려고 합니다.

첫 번째는 `Jenkins Pipeline`입니다. 빌드 / 테스트 / 배포 과정에서 어떤 부분에 문제가 생겼는지 한 눈에 파악하기 위해 도입했습니다.

<img src="https://github.com/momentjin/blog-repository/blob/master/resource/image/cicd1.png?raw=true" width=800px>

위 사진에서 알 수 있는 것처럼, 파이프라인은 각 단계별 상태를 한 눈에 파악하기 편리합니다. 

그리고 파이프라인 코드는 별도의 파일로 관리했습니다. 별도의 파일로 관리하면, 변경사항을 추적할 수 있고, 프로젝트 단위로 파일을 관리할 수 있기 때문에 훨씬 좋습니다.

<img src="https://github.com/momentjin/blog-repository/blob/master/resource/image/jenkins-config2.png?raw=true" width=800px>

위와 같이 파이프라인 설정화면에서 Github - master branch의 파일 중 프로젝트 루트에 위치한 JenkinsFile을 사용하겠다고 설정하시면 됩니다.

두 번째는 `Intellij Jenkins Plugin` 연동입니다. 매번 jenkins 사이트에 접속해서 마우스 클릭으로로 빌드하는 것이 귀찮았습니다. Plugin을 연동하면 조금 더 편리합니다. 플러그인 연동 방법은 [여기](https://momentjin.tistory.com/150)에 따로 정리했습니다.

## 4. 마무리

항상 이런 작업들을 하면서 드는 의문은 `내가 맞게 하고 있는가` 입니다. 체계가 갖춰져 있지 않아, 스스로 문제를 찾고 해결하기 때문인 것 같습니다. 하지만 이에 대한 답변은 사실 간단합니다. 아래 질문들을 자신에게 던져보고, 그 대답을 확실하게 할 수 있으면 맞게 하고 있다고 생각합니다.

- 유지보수하기 쉬운가?
- 이전보다 무엇이 나아졌는가?

읽어주셔서 감사합니다.