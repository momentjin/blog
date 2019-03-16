# Vue.js 기초
> Vue.js를 사용하면서 반드시 알아야할 기본 지식을 정리하고 있는 중..

## Vue.js
- 초경량 UI Framework 

## LifeCycle
- beforeCreate
- created
- beforeMount
- mounted
- beforeUpdate
- updated
- beforeDestory
- destroy

## Directive

#### 데이터 바인딩

- v-text : 콧수염표현식(```{{}}```)과 같은 기능
- v-html : v-text와 같지만, html 태그에 대해 인코딩하지 않고 파싱해서 출력
- v-bind : 엘리먼트의 속성을 바인딩한다. 단방향 바인딩
- v-model : 양방향 바인딩

#### 조건문

- v-show : 일단 렌더링 후, 조건에 따라 display 속성을 변경해 화면에 표시하거나 숨긴다. 화면이 자주 변경되는 경우, v-if보다 v-show를 사용하는 것이 성능상 낫다.

- v-if, v-else-if, v-else : 조건에 따라 렌더링한다.

#### 반복문

- v-for : 단순 배열일 경우, 객체 배열일 경우, 인덱스를 사용하고 싶은 경우, 사용하는 문법이 약간 다르다. v-for 뒤에 v-if를 삽입해 조건을 부여할 수도 있다.
 

 #### 그 외
- v-pre : 템플릿을 컴파일하지 않고, 있는 그대로 출력
- v-once : 렌더링을 단 한 번만 설정, 데이터가 변경되도 재렌더링 X
- v-cloak : 컴파일되지 않은 템플릿 출력 막기 (style에 display: none 정의해야함)

## Vue Option

- el : element, 단일 HTML DOM만 선택가능
- data : vue 인스턴스가 관찰하는 데이터 객체. 변경사항 발생시 즉시 감지됌
- computed : 함수 형태지만 속성처럼 사용할 수 있는 옵션. data에 정의된 data를 연산하여 새로운 data를 생성한다. get, set 함수를 추가적으로 만들 수 있다. 해당 속성이 참조될 때 실행된다.
- methods : Vue 인스턴스에서 사용할 여러 개의 메서드를 등록하는 옵션. Vue 인스턴스 내부에 접근하려면 this가 Vue 인스턴스를 가리켜야 하므로 람다표현식을 사용하면 안된다.
- watch : computed와 마찬가지로 함수 형태지만 속성처럼 사용할 수 있는 옵션. 주로 긴 처리 시간이 필요한 비동기처리에 적합

#### methods와 computed의 차이
computed 옵션은 결과값이 캐싱되고, methods는 캐싱되지 않는다. 

#### computed와 watch의 차이
computed는 값을 직접 리턴하기 때문에 동기식처리만 가능하다.
watch는 값을 직접 리턴하지 않는다. watch에 정의된 속성이 변경을 일으킬 때, 내부에 정의한 로직을 수행한다.

## Event 

### 기본 이벤트 처리
이벤트 처리시 ```v-on``` 디렉티브를 사용한다. <br>
- 문법: v-on:이벤트명 = "method || inline logic" 
- 예시: v-on:click="getList"
- @로 대체할 수 있다. @click="getList"

### 이벤트 객체 활용
> 이벤트를 처리하는 메소드는 첫 번째 파라미터로 이벤트 객체를 전달 받는다. W3C 표준 HTML DOM Event 모델을 그대로 따르면서, vue.js만의 추가적인 속성(이벤트 수식어)을 제공한다.

#### Default Event 발생 방지
- 함수내에서 e.preventDefault() 선언
- 디렉티브 선언시 prevent 선언 (@click.prevent="method")

#### Event Bubbling 발생 방지
- 함수내에서 e.stopPropagation() 선언
- 디렉트브 선언시 stop 선언 (@click.stop="method")

#### Key 이벤트 처리
> vue.js의 코드 수식어를 사용하면 편리하다.
- @keyup.enter 등..

#### HTML의 이벤트 처리 3단계
> HTML 기본 지식이지만 몰라서 적어봤다.
1. CAPTURING : 이벤트 포착 단계; 이벤트가 발생했을 때 HTML 문서의 밖에서부터 이벤트를 발생시킨 HTML 요소까지 포착해 들어간다.
2. RASING : 이벤트 발생 단계; 요소의 이벤트에 연결된 함수를 직접 호출시킨다.
3. BUBBLING : 이벤트가 발생한 요소로부터 상위 요소로 거슬러 올라가면서 동일한 이벤트를 호출시킨다.

#### 이벤트 속성 참고
- https://developer.mozila.org/ko/docs/Web/Reference/Events
- https://www.w3schools.coom/tags/ref_eventattributes.asp


---















---


## Reference
- [Vue.js 퀵 스타트](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=116453349)