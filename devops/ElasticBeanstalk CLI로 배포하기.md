# ElasticBeanstalk CLI로 배포하기

ElasticBeanstalk에 어플리케이션 배포시 CLI로 간단히 배포한 경험을 정리한 글 입니다.

## 개요

최근 회사에서 작은 신규 프로젝트를 진행하고 있습니다. 변경사항이 잦아 배포를 해야될 일이  많은데, 매번 배포할 때마다 빌드하고 웹페이지에서 jar파일을 업로드하면서 배포하고 있습니다. 아직 배포 자동화 인프라가 갖춰지지 않은 환경에서 어떻게 하면 반복되는 배포 작업을 간단히 CLI로 쉽게 처리할 수 있을지 고민해 보았습니다.

## 준비

개발 환경은 다음과 같습니다.

- Mac 
- Intellij
- SpringBoot / Java 

ElasticBeanstalk CLI를 사용하려면, 관련 패키지를 설치해야 합니다. [공식 문서](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html)에 잘 나와있으니 참고해서 설치하시면 됩니다. 공식 문서도 보기 귀찮으시면, 아래의 명령어를 본인의 터미널에 입력해주세요.

```shell
> pip3 install awsebcli --upgrade --user
> export PATH=~/Library/Python/3.7/bin:$PATH
> source ~/Library/Python/3.7/bin
```

설치가 끝났으면, 아래와 같이 설치가 잘 됐는지 확인해보세요.

![img1](https://raw.githubusercontent.com/momentjin/study/master/resource/image/eb-cli%20설치%20확인.png)

## eb init

먼저 deploy하려면 해당 프로젝트가 위치한 디렉토리로 이동해서 `eb init` 커맨드를 실행해야 합니다. 실행하면 다음과 같이 몇가지 선택을 해야하는데 환경에 맞게 선택해주시면 됩니다.

![img2](https://raw.githubusercontent.com/momentjin/study/master/resource/image/eb-cli%20init.png)


이제 배포할 환경을 선택해야할 차례입니다. 환경이란, ElasticBeanstalk에서 Application을 생성하고, 여러 개의 환경을 만들게 되는데 바로 그 환경을 말하는 것입니다. `eb list` 커맨드를 입력하면 다음과 같이 어플리케이션 내에 여러 환경을 볼 수 있습니다. 배포할 환경을 선택하시려면 `eb use [환경 이름]` 커맨드를 입력하면 됩니다.

![img3](https://raw.githubusercontent.com/momentjin/study/master/resource/image/eb-list.png)


이제 본격적으로 배포를 해야될 차례입니다. 우선 ElasticBeanstalk에서 배포하는 방법들은 여러 가지가 있습니다. 저는 아주 심플한 배포방식이 필요하므로 가장 단순한 방법을 사용했으니 참고 부탁드립니다.

지금 잘 따라오셨다면, `프로젝트 루트/.elasticbeanstalk/config.yml` 파일이 생성되어있을 것입니다. 내용은 다음과 같습니다.

```yml
branch-defaults:
  master:
    environment: ToyRezoom-prod
environment-defaults:
  ToyRezoom-prod:
    branch: null
    repository: null
global:
  application_name: toy-rezoom
  default_ec2_keyname: null
  default_platform: arn:aws:elasticbeanstalk:ap-northeast-2::platform/Java 8 running
    on 64bit Amazon Linux/2.10.3
  default_region: ap-northeast-2
  include_git_submodules: true
  instance_profile: null
  platform_name: null
  platform_version: null
  profile: eb-cli
  sc: git
  workspace_type: Application
```

해당 파일에 아래와 같이 내용을 추가해줍니다. 배포할 jar파일의 경로를 입력해주시면 됩니다.

```yml
deploy:
  artifact: target/rezoom-0.0.1-SNAPSHOT.jar
```

이제 deploy를 해보겠습니다. `eb deploy` 커맨드를 입력해줍니다.


![img4](https://raw.githubusercontent.com/momentjin/study/master/resource/image/eb-deploy.png)

이제 ElasticBeanstalk에서 해당 환경의 페이지를 열어보면 다음과 같이 배포가 진행되는 모습을 볼 수 있습니다.

![img5](https://raw.githubusercontent.com/momentjin/study/master/resource/image/eb-deploy%20배포중.png)

## 마무리

정말 간단하게 ElasticBeanstalk에 어플리케이션을 배포하는 방법을 소개해드렸습니다. 언젠가는 배포 자동화 인프라를 구축해야하지만, 오버스펙이라고 생각되면 이 방식도 괜찮아 보입니다.

앞으로 ElasticBeanstalk를 자주 사용하게 될 것 같아 더 심화된 내용도 정리해서 올려보겠습니다. 읽어주셔서 감사합니다 :)