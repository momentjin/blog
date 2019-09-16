# Algorithm

알고리즘은 자료구조와 최적화에 관해 배울 수 있는 훌륭한 요소라고 생각합니다. 지금까지 수박 겉핥기 식으로 알고리즘을 공부했었는데, 이번에 좋은 [인터넷 강의](https://www.inflearn.com/course/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EA%B0%95%EC%A2%8C#)를 발견해서 새롭게 다시 공부하려고 합니다. 

정리는 모르는 것 또는 애매하게 알고 있는 것 위주로 정리했습니다. 정리하는 내용은 강의 위주이고, 강의에서 다루지 않는 알고리즘도 추가해서 정리할 예정입니다.

## 목차

1. [Recursion](##Recursion)

2. [Sort](##Sort)

3. [Binary Search Tree](##Binary&nbsp;Search&nbsp;Tree)

4. [Red Black Tree](##Red&nbsp;Black&nbsp;Tree)

5. [Graph](##Graph)

6. [Hashing](##Hashing)

----


## Recursion
재귀 (자기 자신을 호출) <br>

무한루프에 빠지지 않도록 해야 한다. 
- base case : 종료해야 하는 경우
- recursive case : 재귀 호출해야 하는 경우

모든 반복문은 재귀로 전환이 가능하다. 그 역도 성립한다.

재귀는 오버헤드가 있다. 지속적으로 호출되는 함수의 지역변수 등의 데이터를 스택에 보관해야 한다. 그래서 함수 호출 레벨이 깊으면 java의 경우 stackoverflow 오류가 발생한다.

백트래킹은 재귀를 사용한다.

분할정복은 재귀를 사용한다. 예를 들어 피보나치를 구하는 재귀문을 보면 `f(n) = f(n-1) + f(n-2)` 이런 코드가 있다. 즉 f(n)은 f(n-1) + f(n-2)로 분할, 정복할 수 있다는 말과 같다.


-----


## Sort

### Comparison Sort
> 모든 로그는 밑이 2 입니다.. 특수문자 어디에 ~~

#### Selection Sort, Bubble Sort
- 무조건 전체 탐색해서 정렬한다.
- 최선, 최악 O(n^2)

#### Insert Sort
- 최선 O(n) : 이미 정렬되어 있는 상태에서 정렬할 때, 총 N-1번의 비교만 수행한다.
- 최악 O(n^2) : 반대로 정렬된 데이터를 정렬할 때, 총 n + n-1 + n-2 + .. + 1번, 즉 n(n-1)/2번의 비교를 수행한다.

#### Merge Sort
- 최선, 최악 O(N * Log N)
- 데이터를 분할하는 횟수는 log N번 -- N이 2의 거듭제곱이라면 N = 2^k, N=8일 때 8 -> 4 -> 2 -> 1로 분할된다. 즉, 일반화하면 logN이라는 걸 알 수 있다. 그리고 각 분할된 단계별로 이를 병합하는 횟수는 총 N번. 따라서 N logN이라는 시간복잡도를 도출할 수 있다.

#### Quick Sort
- 최악 O(n^2) : 이미 정렬된 데이터에서 마지막 원소를 피벗으로 선택하는 경우 분할시 항상 한 쪽은 0개, 다른 쪽은 n-1개로 분할된다. 이 때의 시간 복잡도를 계산해보면 T(n) = T(0) + T(n-1) + n-1 ---- n은 데이터 비교 연산 횟수. 즉, 한 번 분할할 때마다 n-1번 비교하므로, 총 분할의 횟수 n-1 + n-2 + n-3 + ... + 1. 즉, n(n-1)/2번이므로 시간복잡도는 O(n^2)임을 알 수 있다.

- 최선 O(N * log N) : 항상 절반으로 분할되는 경우 --- Merge Sort와 같다. 즉 분할되는 횟수 * 각 분할 단계별 데이터 비교 횟수이므로 총 연산의 수는 log N * N = N log N임을 알 수 있다.

#### Heap Sort
- Heap이라는 자료구조를 사용해서 정렬하는 방법 (Heap? 완전이진트리이면서, Heap Property 만족하는 자료구조)
- Heap Sort 방법
    1. N/2번 노드부터 1번 노드까지 Heapify를 수행해서 먼저 Heap을 만든다. (루트는 1번이라고 가정)
    2. (max heap인 경우) Heap에서 최대값(루트)를 가장 마지막 값과 바꾼다.
    3. 루트 노드에 대해 다시 Heapify를 수행한다. 이 때 마지막값은 제외한다. (Heap size 1 감소)
    4. 2~3단계 반복

- 최선, 최악 O(N * Log N)
    - 단계1 - Heapify를 수행하는데 총 n번의 연산 수행
    - 단계2,3 - n번 순회하면서, 루트와 마지막 노드의 값을 바꾸고 다시 루트에 대해서만 Heapify를 수행하므로 logN번의 연산 수행
    - 즉, O(n) + O(N * log N)이므로 시간복잡도는 O(N * log N)이다.

- Heapify 알고리즘
    ```
    // code
    ```

### Non-Comparison Sort

non-comparison 정렬의 경우, 항상 정보가 제공된다 (필요하다)

비교를 기반으로 하지 않는 정렬은 선형시간으로 정렬이 가능하다. 반면, 비교기반 정렬의 경우 아무리 빨라도 시간복잡도는 O(nlogn)이다.

Radix, Counting Sort 둘 다 Stable Sort이다. 
> Stable Sort란, 동일한 값에 대해서 정렬을 수행해도 입력으로 들어온 순서와 동일하게 유지되는 정렬을 말한다.

#### Counting Sort
- 정렬할 데이터를 카운팅해서 정렬하는 방법
- 주어지는 정보 예시 : N개의 정수를 정렬, 단 모든 정수는 0에서 K사이의 정수이다.

- 정렬 방법
    1. 각 데이터의 key값을 카운팅 후 누적합을 구해 별도의 배열(C)로 저장-- (a[0]<-a[0], a[1]<-a[0]+a[1]...)
    2. 정렬할 배열 크기만큼 내림차순으로 순회하면서 누적합을 이용해 정렬한다. (정렬할 데이터를 담을 빈 배열(B)이 필요)

- Source Code

    ```
    // A는 정렬할 배열
    // B는 결과값을 저장할 배열 (정렬된 배열)
    // C는 누적합 배열

    countingSort()

        // counting
        for i <- 1 to A.length
            do C[A[i]] <- C[A[i]] + 1

        // accumulating
        for i <- 1 to C.length
            do C[i] <- C[i] + C[i-1]
        
        // sorting
        for i <- A.length downto 1
            do B[C[A[i]]] <- A[i]
            C[A[i]] <- C[A[i]] - 1
    ```

- 시간복잡도 O(n+k) or O(n)
    - k는 누적합 배열 C의 크기
    - Counting Sort는 일반적으로 N >> K일 때 사용. (K가 더 크면 비실용적)

#### Radix Sort
- 수의 자릿수를 이용해 정렬하는 방법
- 주어지는 정보 예시 : N개의 D자리 정수들 (즉, 길이가 정해져있고 각 자리의 범위가 상수일 때 Radix Sort를 사용할 수 있다)

- 정렬 방법
    1. 가장 낮은 자릿수를 기준으로 정렬한다.
    2. 그 다음 낮은 자릿수를 기준으로 정렬한다.
    3. 첫 번째 자릿수까지 1,2단계 반복
        - 각 자릿수는 Counting Sort로 정렬하기 적합하다. (stable sort라면 무엇이든 가능)

- Source Code
```
// A: 정렬할 배열
// d: d자리 정수
radixSort(A, d)
    for i <- 1 to d
        use stable sort to sort array a on digit i 
```

- 시간복잡도 O(d(n+k))
    - 위 시간복잡도는 각 자릿수를 Counting Sort로 정렬했을 때 기준
    - counting sort의 시간복잡도 O(n+k)
    - radix sort는 그 counting sort를 d번 반복하기 때문에 d(n+k)이므로 시간복잡도는 O(d(n+k))


-----


## Binary&nbsp;Search&nbsp;Tree

: 정리 예정


-----


## Red&nbsp;Black&nbsp;Tree

: 정리 예정


-----


## Hashing

- 해시함수란 데이터의 효율적 관리를 목적으로 임의의 길이의 데이터를 고정된 길이의 데이터로 매핑하는 함수. 해시함수의 결과값을 해시테이블의 인덱스로 활용하여 데이터를 저장하는 과정을 해싱(Hashing)이라고 표현한다. 

- 특정 데이터(Key)를 해싱해서 나온 결과값이 해시테이블의 인덱스가 되므로, random access가 가능함 -> 검색의 시간 복잡도는 O(1), 그러나 이건 이상적인 경우..

- 충돌 (Collision)
    - 두 개 이상의 키가 동일한 위치로 해싱되는 경우

   충돌 해결 방법
    1. Chaning
        - 동일한 인덱스로 해싱된 모든 키들을 하나의 연결리스트로 저장
    2. Open Addressing
        - 모든 키는 hash table에 저장 (하나의 인덱스에 반드시 하나의 key가 맵핑됌)
        - 종류
            1. Linear Probing
                - 해시함수를 h, Key를 k라고 할 때 h(k)가 이미 해시테이블에 존재하면 h(k)+1, h(k)+2 .. 이렇게 순차적으로 빈 곳을 찾아 맵핑하는 방법
            2. Quadratic Probing
                - Linear와 유사, h(K)가 존재하면 h(k)+1^2, h(k)+2^2 규칙으로 검사해서 해싱하는 방법
            3. Double Hashing
                - 서로 다른 두 해시함수 h1, h2를 이용하는 방법
                - h(k, i) = (h1(k) + i*h2(k)) mod m : i=0일 때 h(k)가 존재하면, i=1 시도. 빈 곳을 찾을 때까지 i는 1씩 증가

    Java에서는 Chaning 방식으로 충돌을 해결하고, load factor(0~1 사이의 실수)를 지정하여 저장된 key의 갯수가 해시테이블의 크기 * load factor개를 초과하면 해시테이블의 크기를 늘리고 re-hashing을 수행한다.


----


## Graph

: 정리 예정


-----


## 그 외 정리할 알고리즘
- 다익스트라 (우선순위 큐)
- 문자열 찾기 알고리즘
- ?


-----


## 나중에 정리할 것
- merge, quick sort 둘다 평균 nlogn인데, 왜 quicksort를 가장 빠른 알고리즘이라고 하는건지?
- ?