# Intellij에서 QueryDSL를 사용할 때  QClass 인식 문제 해결 방법

Intellij에서 QueryDSL를 사용할 때 QClass가 실제 존재함에도 불구하고, 인식하지 못하는 문제가 있었습니다. 이번 포스팅에서 이 문제를 해결하기 위한 간단한 팁을 아주 짧게 소개하고자 합니다.

## 문제 상황

분명히 QClass 파일은 존재함에도 불구하고, IDE에서는 Cannot resolve symbol 'foo'와 같은 오류를 내뿜고 있습니다. 신기하게도 실행은 잘 되지만, 코드 자동완성 기능을 이용할 수 없기 때문에 QueryDSL 작업시 매우 불편합니다. 

## 해결

먼저 아래와 같이 Intellij의 File-Project Structure 메뉴를 보면 다음과 같이 'Source Folders'에 java만 있는 것을 확인해볼 수 있습니다. 

![결과](https://github.com/momentjin/study/blob/master/resource/image/querydsl인식문제1.png?raw=true)

다음과 같이 'generated' 폴더를 Sources로 설정하면 IDE가 해당 폴더를 Source로 인식해서 더 이상 오류를 보여주지 않습니다.

![img2](https://github.com/momentjin/study/blob/master/resource/image/querydsl인식문제2.png?raw=true)

이제 신나게 QueryDSL을 사용하면 됩니다.