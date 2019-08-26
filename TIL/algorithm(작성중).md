# Algorithm

알고리즘은 자료구조와 최적화에 관해 배울 수 있는 훌륭한 요소라고 생각합니다. 지금까지 수박 겉핥기 식으로 알고리즘을 공부했었는데, 이번에 좋은 [인터넷 강의](https://www.inflearn.com/course/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EA%B0%95%EC%A2%8C#)를 발견해서 새롭게 다시 공부하려고 합니다.

정리는 모르는 것 또는 애매하게 알고 있는 것 위주로 정리했고, 정리한 내용이나 순서 등은 강의 순서와 동일하게 정리했습니다.

## 목차

1. [Recursion](##Recursion)

2. [Sort](##Sort)


----


## Recursion
재귀 (자기 자신을 호출) <br>

무한루프에 빠지지 않도록 해야 한다. 
- base case : 종료해야 하는 경우
- recursive case : 재귀 호출해야 하는 경우

모든 반복문은 재귀로 전환이 가능하다. 그 역도 성립한다.

재귀는 오버헤드가 있다. 지속적으로 호출되는 함수의 지역변수 등의 데이터를 스택에 보관해야 한다. 그래서 함수 호출 레벨이 깊으면 java의 경우 stack overflow 오류가 발생한다.

백트래킹은 재귀를 사용한다.

분할정복은 재귀를 사용한다. 예를 들어 피보나치를 구하는 재귀문을 보면 `f(n) = f(n-1) + f(n-2)` 이런 코드가 있다. 즉 f(n)은 f(n-1) + f(n-2)로 분할, 정복할 수 있다는 말과 같다.


-----


## Sort

### Comparison Sort

Selection Sort
- 최선, 최악, 평균 O(n^2)

Bubble Sort
- 최선, 최악, 평균 O(n^2)

Insert Sort
- 최악 O(n^2)

Merge Sort
- 최선, 최악, 평균 O(nLogn)

Quick Sort
- 최악 O(n^2)
- 최선, 평균 O(nLogn)

Heap Sort
- 최선, 최악, 평균 O(nLogn)

### Non-Comparison Sort

non-comparison 정렬의 경우, 항상 정보가 제공된다(필요하다)

Counting Sort
- stable sort

Radix Sort
- stable sort

-----