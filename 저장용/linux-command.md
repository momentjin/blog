# Linux Command
'리눅스 커맨드라인 완벽 입문서'라는 책을 보면서 중요하거나 기억하고 싶은 부분만 정리한 자료입니다. 명령어와 그 역할에 대해서 간단히 기술했고, 실전에서 리눅스를 다뤄보며 좀 더 상세하게 내용을 채우고자 합니다.


## Shell vs Terminal
궁금해서 찾아봤습니다 :)
- Shell : 명령어 해석기
- Terminal : 명령어를 입력하고 출력하는 환경


## 파일, 디렉토리 조작 관련 명령어
- cp : 복사 (copy)
- mv : 이동, 이름 바꾸기 (move)
- mkdir : 디렉토리 생성 (make a directory)
- rm : 삭제 (remove)

옵션
- -i, --interactive : 어떤 작업을 수행하기 전 동의를 구하겠다.
- -r, --recursive : 디렉토리와 그 안의 파일, 내용까지 포함하겠다.
- -v, --verbose : 명령어 수행을 완료했다는 메세지를 보여주겠다.

## 파일 검색 관련 명령어

`locate` : 글로벌 파일 찾기

`find` : 현재 디렉토리 내에서 파일 찾기


## 파이프라인
명령어의 출력을 또 다른 명령어의 입력과 연결시킬 수 있는 기능이다. 흔하게 사용하는 `grep`를 떠올리면 쉽다. 예를 들어 history 중에 mysql이 포함된 command만 보고 싶다면, history | grep mysql 라고 입력하면 된다. 이 때, history의 출력을 파이프라인을 이용해 grep의 입력과 연결시킨 것이다. 

현재 폴더 내 하위 폴더/파일 중 이름에 work가 포함된 항목의 갯수를 구하고 싶다면? 아래와 같이 파이프라인을 이용하면 쉽게 해결할 수 있다.
```
ls -al | grep work | wc -l 
```

## head와 tail

출력의 처음 몇 줄 또는 끝의 몇 줄만 확인하고 싶을 때 사용하는 명령어다. -n 옵션을 통해 출력할 라인 수를 지정할 수도 있다. 
```
tail -n 5 output.txt
```

`tail` 명령어는 실시간으로 파일을 확인할 수 있는 옵션을 지원한다. 로그 파일이 기록되는 동안 최근 내용을 확인하고 싶은 상황에서 사용하면 편리하다. follow라는 의미의 f옵션을 주면 된다.
```
tail -f output.txt
```

## I/O 리다이렉션

입력과 출력에 대한 방향을 재지정하는 방법이다. 예를 들어 ls 커맨드의 결과를 txt파일에 저장하고 싶다면? 아래와 같이 커맨드를 입력하면 ls 커맨드의 결과가 list.txt 파일에 저장된다. (파일이 존재하지 않으면 자동 생성)
```
ls -al > list.txt
```

'>' 연산자는 기본적으로 출력할 대상 파일의 값을 덮어쓴다. 이 때는 > 대신 `>>` 연산자를 사용해서 덧붙이면 된다.

오류 메세지의 경우 > 연산자로 출력이 불가능하다. 어떤 이유로 `2>` 연산자를 사용하라고 한다. ~~파일 디스크립터라고 하는데, 아직은 디테일하게 알고 싶지 않다!~~

기본 출력 및 오류를 한 번에 출력하고 싶다면 `&>` 연산자를 사용하면 된다.


## 텍스트 편집 관련 명령어

### cat 
cat 명령어는 concatenate, 연결하다의 줄임말이다. cat은 단순히 텍스트를 출력할 때 사용하는 커맨드인 줄 알았는데 아니었다는 사실에 놀랐다. 아래와 같이 입력하면 a.txt와 b.txt의 내용을 이어서 보여준다.
```
cat a.txt b.txt 
```

대용량 파일이 분산되서 저장되어 있는 경우, 아래와 같이 입력하면 분산된 파일을 하나로 합칠 수 있다. (실제로 해보진 않았다)
```
// movie.mpeg.0 ~ movie.mpeg.9 까지의 파일들이 존재하는 상황에서
cat movie.mpeg.0* > movie.mpeg
```

### sort

이 커맨드는 텍스트를 정렬할 때 유용하다. 예를 들어 다음과 같은 텍스트 파일이 있을 때 sort 커맨드를 수행하면 다음의 결과를 출력한다
```
// foo.txt
1
2
3

// execute
sort foo.txt

// output
3
2
1
```

텍스트 안의 내용을 정렬하는 경우가 별로 많아보이지 않을 수도 있다. 하지만 다음과 같이 활용되기에 반드시 알아야 할 필요가 있다고 본다. 

```sh
// 현재 디렉토리 내의 폴더 및 파일들의 크기가 가장 큰 순서대로 정렬한다.
du ./* | sort -nr | head
```

-k 옵션을 사용하면 특정 컬럼을 기준으로 정렬할 수 있다.
```shell
// 정렬 전
ls -al

drwxr-xr-x  20 momentjin  staff      640 11  1 18:42 .
drwxr-xr-x   3 momentjin  staff       96  5  5  2019 ..
-rw-r--r--   1 momentjin  staff    20798  5  5  2019 ERD.PNG
-rw-r--r--   1 momentjin  staff    57525 11  1 18:42 rezoom-notificator.png
-rw-r--r--   1 momentjin  staff  1202596 10 30 18:02 rezoom-schema.png
-rw-r--r--   1 momentjin  staff   452583 11  1 16:49 rezoom-screenshot1.png
-rw-r--r--   1 momentjin  staff    57118 10 30 19:28 rezoom-screenshot2.png
-rw-r--r--   1 momentjin  staff   506462 11  1 16:49 rezoom-screenshot3.png
-rw-r--r--   1 momentjin  staff    71885 10 22 01:26 uml-adapter.png
-rw-r--r--   1 momentjin  staff    23206  5  5  2019 uml-command.PNG
-rw-r--r--   1 momentjin  staff    15619  5  5  2019 uml-decorator.PNG
-rw-r--r--   1 momentjin  staff    15876  5  5  2019 uml-observer.PNG
-rw-r--r--   1 momentjin  staff    45231 10 15 00:59 uml-proxy.png
-rw-r--r--   1 momentjin  staff    58945 10 15 23:32 uml-state.png
-rw-r--r--   1 momentjin  staff     8920  5  5  2019 uml-strategy.PNG
-rw-r--r--   1 momentjin  staff    39670 10 17 21:25 uml-template-method.png
-rw-r--r--   1 momentjin  staff    89924  6  2 15:16 테스트코드리팩토링_1.png
-rw-r--r--   1 momentjin  staff    69027  6  2 15:23 테스트코드리팩토링_2.png
-rw-r--r--   1 momentjin  staff    31881  6  2 16:56 테스트코드리팩토링_3.png
-rw-r--r--   1 momentjin  staff   262769  6  3 00:03 테스트코드리팩토링_4.png

// 정렬 후
// 5번째 컬럼을 기준, 역순 정렬
ls -al | sort -r -k 5

-rw-r--r--   1 momentjin  staff  1202596 10 30 18:02 rezoom-schema.png
-rw-r--r--   1 momentjin  staff   506462 11  1 16:49 rezoom-screenshot3.png
-rw-r--r--   1 momentjin  staff   452583 11  1 16:49 rezoom-screenshot1.png
-rw-r--r--   1 momentjin  staff   262769  6  3 00:03 테스트코드리팩토링_4.png
-rw-r--r--   1 momentjin  staff    89924  6  2 15:16 테스트코드리팩토링_1.png
-rw-r--r--   1 momentjin  staff    71885 10 22 01:26 uml-adapter.png
-rw-r--r--   1 momentjin  staff    69027  6  2 15:23 테스트코드리팩토링_2.png
-rw-r--r--   1 momentjin  staff    58945 10 15 23:32 uml-state.png
-rw-r--r--   1 momentjin  staff    57525 11  1 18:42 rezoom-notificator.png
-rw-r--r--   1 momentjin  staff    57118 10 30 19:28 rezoom-screenshot2.png
-rw-r--r--   1 momentjin  staff    45231 10 15 00:59 uml-proxy.png
-rw-r--r--   1 momentjin  staff    39670 10 17 21:25 uml-template-method.png
-rw-r--r--   1 momentjin  staff    31881  6  2 16:56 테스트코드리팩토링_3.png
-rw-r--r--   1 momentjin  staff    23206  5  5  2019 uml-command.PNG
-rw-r--r--   1 momentjin  staff    20798  5  5  2019 ERD.PNG
-rw-r--r--   1 momentjin  staff    15876  5  5  2019 uml-observer.PNG
-rw-r--r--   1 momentjin  staff    15619  5  5  2019 uml-decorator.PNG
-rw-r--r--   1 momentjin  staff     8920  5  5  2019 uml-strategy.PNG
drwxr-xr-x  20 momentjin  staff      640 11  1 18:42 .
drwxr-xr-x   3 momentjin  staff       96  5  5  2019 ..
```

### 그 외

`uniq` : 인접한 행을 비교해서 중복을 제거한다. 따라서 sort 명령어와 함께 사용하는 경우가 많다.
`cut` : 텍스트에서 특정 기준을 갖고 문자열을 뽑아낸다.
`paste` : 파일들의 행을 합친다.
`join` : RDB의 join과 마찬가지로 공통 필드를 이용해 두 파일의 행을 합친다.


## 커맨드라인 조작

mac에는 home, end 키가 없다. 물롤 shell이 아닌 경우에는 command+방향키로 home, end 키를 대체할 수 있지만, 터미널에선 불가능하다. shell에서는 다음과 같은 단축키를 사용해야 한다.

- CTRL-A : 줄 맨 앞으로 이동
- CTRL-E : 줄 맨 끝으로 이동


## history

입력한 커맨드 내역을 조회할 수 있는 커맨드이다.

history를 입력하면, 과거 커맨드 내역과 함께 번호가 주어지는데 !번호를 쉘에 입력하면 해당 커맨드가 명령줄에 복사된다. (어떤 환경에서는 바로 실행되기도 한다)

shell 입력 공간에서 ctrl+R을 누르면 히스토리를 `검색`할 수 있다. 이것에 관해 다양한 단축키들을 제공하지만, 많이 알면 머리 아프니 grep를 사용해서 history 내역을 검색하자.


## Permission 관련 명령어

### 파일 권한

파일 권한은 10개의 문자로 표현한다.
- 파일종류(1) Owner 권한(3) Group 권한(3) World 권한(3)

파일종류에는 다음과 같은 문자가 올 수 있다.
- `-` : 일반 파일
- `ㅇ` : Directory
- `ㅣ` : 심볼릭 링크
- `c` : 문자 특수 파일
- `b` : 블록 특수 파일

Owner등의 권한에는 다음과 같은 문자가 올 수 있다.
- r : 읽기 권한
- w : 쓰기 권한
- x : 실행 권한 (파일이 프로그램으로 처리되고 실행되도록 허용하는 것)

예시
```shell
// 파일 소유자에 의해 읽기, 쓰기, 실행 가능한 일반 파일. 소유자 외 접근 불가능
-rwx------ 

// 소유자 및 소유 그룹은 디렉토리 안으로 들어갈 수 있고, 디렉토리 내 파일들을 생성하거나 삭제 및 변경 가능
drwxrwx---
```

### 파일 권한 변경

`chmod` 명령어를 사용하면 파일 모드(권한)를 변경할 수 있다. 8진법 또는 문자열을 이용해서 바꿀 수 있는데, 하나만 아는게 속 편한 것 같아서 8진법만 외웠다.

```
0 - 000 - ---
1 - 001 - --x
2 - 010 - -w-
3 - 100 - r--
...
7 - 111 - rwx
```

8진법의 각 수에 해당하는 권한을 간략하게 정리했다. 만약 해당 파일을 자기 자신만 읽고 쓸수 있도록 권한을 주고 싶다면 `chmod 600 [file]` 명령어를 입력하면 된다. 6은 110이므로 rw-이고 0은 ---이므로 600은 -rw-------가 되기 때문이다.

### 파일 소유자, 그룹 변경하기

`chown` 명령어를 사용하면 된다.

[owner][:[group]] file ..

예시
```shell
// 파일의 소유권을 bob으로, 그룹 소유권은 users로 변경
chown bob:users file1 
```

## 사용자 관련 명령어

id : 자신의 id 정보 확인

whoami : 자신의 username 확인

passwd : 사용자 비밀번호 변경


## Network 관련 명령어

ping, traceout, scp, ftp, sftp, netstat 등


## 프로세스 관련 명령어

ps : 프로세스의 상태를 보여준다.

kill, killall : 프로세스에 신호를 보낸다 (종료, 중지 등)

프로세스를 종료하고 싶으면?
1. ps 명령어를 이용해 종료할 프로세스의 PID를 알아낸다.
2. kill PID를 입력해서 종료한다.


## 그 외

su : 다른 사용자로 쉘을 시작하기 위해 사용하는 명령어

sudo : 다른 사용자로 명령어를 실행하기 위해 사용하는 명령어 (보통은 관리자)

type : 커맨드의 종류 표시

which : 실행 파일의 위치 표시

alias : 명령어 만들기

nl : 출력값에 행 번호를 지정한다. ( ls -al | tr )