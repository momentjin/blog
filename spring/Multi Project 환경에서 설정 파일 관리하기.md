안녕하세요. 오늘은 모놀리식 프로젝트에서 멀티 프로젝트로 변경하면서 생긴 설정 파일  (application.yml) 셋팅 문제와 이를 해결한 경험을 공유하고자 합니다. 

본 글에서 application.yml에 대한 문법적인 방법은 다루지 않았으니 참고 부탁드립니다.

## 설정 코드 중복 문제

기존 모놀리식 프로젝트 형태에서는 다음과 같은 구조를 갖고 있습니다. 
- 개발(dev) 환경 설정 : application-dev
- 운영(prod) 환경 설정 : application-prod
- 공통 설정 : application.yml

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/multi-config-1.png" height=250px>
</div>


모놀리식 프로젝트는 위와 같은 설정에서 전혀 문제가 없었습니다. 하지만 멀티 프로젝트로 전환하면서 프로젝트마다 개별적으로 설정을 해야하는 경우가 생겼는데, 설정 코드가 중복되어 관리하기 어려웠습니다.

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/multi-config-2.png" height=350px>
</div>

이 문제를 해결하기 위해선 중복 코드를 제거하고, 공통적인 설정을 import를 해야했습니다. 하지만 제가 가진 지식으론 어떻게 import를 해야할지 감이 잡히질 않았습니다.

설정 파일을 항상 개발 환경(prod, dev 등)의 관점으로만 생각했던 것이 잘못이었습니다.

## 해결

많은 글들을 참고한 결과, 그동안 설정 파일을 잘못 구성하고 있음을 깨달을 수 있었습니다. 

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/multi-config-3.png" >
</div>

위 그림은 [Spring 공식 문서](https://docs.spring.io/spring-boot/docs/1.1.x/reference/html/boot-features-profiles.html)를 캡쳐한 그림입니다. 빨간 네모친 부분을 봤을 때, 설정 파일을 특성에 맞게 구분한 것을 볼 수 있습니다. 단순히 환경(dev, prod)로만 설정 파일을 구분한 저와는 확실히 다름을 알 수 있습니다.

아래는 구조를 개선한 결과입니다.

**[멀티 프로젝트에서의 설정 파일 구조]**

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/multi-config-4.png" height=400px>
</div>

<br>

**[application-mysql.yml]**

<div>
<img src="https://raw.githubusercontent.com/momentjin/blog-repository/master/resource/image/multi-config-5.png" height=400px>
</div>

<br>

예시로, application-mysql.yml에는 mysql 관련 설정 코드만 작성합니다. 저는 환경에 따라 별도로 설정 파일을 만들지 않고, 내부적으로 환경을 구분하는 방법을 택했습니다. application-core에서는 아래와 같이 이를 include 해주면 됩니다.

```yml
spring:
  profiles:
    include:
      - mysql
      - mongo
    active: dev # default profile
```

now-admin-api 프로젝트의 application.yml도 간단합니다. 개별 설정할 부분은 개별 설정하고, 공통 설정이 필요하면 include 해줍니다. 

```yml
spring:
  profiles:
    include: core

server:
  port: 5000
```

## 끝으로 

상세하게 다루지 않은 이유는 저보다 잘 정리된 훌륭한 분들의 글들이 이미 많기 때문입니다. 이 글의 내용을 처음 접하시는 분들은 아래 참고 항목에 나열한 글들을 보시면 이해하는데 도움이 될 것입니다.

감사합니다.

## 참고한 글

- https://woowabros.github.io/study/2019/07/01/multi-module.html
- https://github.com/ihoneymon/multi-module
- https://docs.spring.io/spring-boot/docs/1.1.x/reference/html/boot-features-profiles.html

