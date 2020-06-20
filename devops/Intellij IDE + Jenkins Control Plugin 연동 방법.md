Intellij에 Jenkins Control Plugin 연동하는 방법을 간단히 소개합니다.

## Jenkins Control Plugin 설치 

우선 jenkins control plugin을 설치해줍니다. 

<img src="https://github.com/momentjin/blog-repository/blob/master/resource/image/jenkins-plugin4.png?raw=true" height=200px>

## Jenkins Control Plugin 설정

설치를 완료하셨으면, Intellij를 재시작한 뒤 아래의 루트를 통해 Jenkins plugin 설정 메뉴로 접속합니다. 
- Preferences > Tools > Jenkins Plugin

<img src="https://github.com/momentjin/blog-repository/blob/master/resource/image/jenkins-plugin3.png?raw=true" width=800px>

자신의 환경에 알맞는 값을 입력합니다.

- Server Address : Jenkins 웹페이지 주소
- Username : Jenkins 접속 계정의 ID
- Password : (아래 참고) Jenkins 접속 계정의 Credential Key
- Crumb Data : (아래 참고) Jenkins의 CrumbData

### Password 발급 받는 방법

[jenkins domain]/user/[user-id]/configure 로 접속하시면, 아래와 같은 페이지가 뜹니다.

<img src="https://github.com/momentjin/blog-repository/blob/master/resource/image/jenkins-plugin2.png?raw=true" width=800px>

Add new Token 버튼을 클릭하면, Key가 생성되고 이를 Plugin 설정 화면의 Password 필드에 넣어주면 됩니다.

### Crumb Data 발급 받는 방법

[jenkins domain]/crumbIssuer/api/json?tree=crumb로 접속하시면, 아래와 같은 json 타입의 결과값을 받을 수 있습니다. crumb의 값을 Plugin 설정 화면의 CrumbData 필드에 넣어주면 됩니다.

```json
{
    "_class":"hudson.security.csrf.DefaultCrumbIssuer",
    "crumb":"[Crumb Data가 이곳에 출력됩니다]"
}
```

## Jenkins Plugin 사용법

셋팅이 완료되면, 다음과 같이 오른쪽에 Jenkins Item List가 보입니다. 빌드하고 싶은 아이템 우클릭 후 Build 하시면 됩니다.

<img src="https://github.com/momentjin/blog-repository/blob/master/resource/image/jenkins-plugin1.png?raw=true" width=400px>

