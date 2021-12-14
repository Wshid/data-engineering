# CH02. 병렬처리에서 분산처리까지

## CH02_01. 병렬처리와 분산처리
- 병렬처리(Parallel)
- 분산처리(Distributed)
- Data-Parallel
  ```scala
  RDD.map(<task>)
  ```
  - 데이터를 여러개로 쪼개고
  - 여러 스레드에서 각자 task 수행
  - 각자 만든 값을 합치기
- Distributed Data-Parallel
  - 데이터를 여러개로 쪼개 **여러 노드로 보냄**
  - 여러 노드에서 독립적으로 task 적용
  - 각자 만든 결과값을 합치는 과정
- 노드간 통신 처럼 신경쓸 것이 많아지며
  - Spark를 사용하면 **분산된 환경**에서도
    - **일반적인 병렬처리**하듯 코드 구성이 가능
- Spark는 분산된 환경에서
  - 데이터 **병렬 모델**을 구현해 추상화 시켜주기 때문
- 노드간 통신
  - 통신 속도를 신경써야 함

## CH02_02. 분산처리와 Latency_1
- 분산처리 -> 신경써야할 문제가 많음
  - **부분 실패**: 노드 몇개가 `프로그램과 상관없는 이유`로 인해 실패
  - **속도**: `많은 네트워크 통신`을 필요로 하는 작업은 속도 저하
- 예시 코드
  ```python
  // 사전 필터링이 적용된 첫번째 라인이 빠름
  // reduceByKey: 여러 노드에서 데이터를 가져옴
  RDD.map(A).filter(B).reduceByKey(C).take(100)
  RDD.map(A).reduceByKey(C).filter(B).take(100)
  ```
- 속도
  - 메모리 > 디스크 > 네트워크
  - **네트워크는 메모리 연산에 비해 1M배정도 느림**

## CH02_03. Key-Value RDD
- `Pairs RDD`
- 간단한 데이터 베이스처럼 다룰 수 있음
- Single Value RDD / Key-Value RDD
- 키 단위 집계가 되기 때문에, 그에 대한 연산 가능
- 예시
  ```python
  pairs = rdd.map(lambda x: (x, 1))
  ```
  단순 값 뿐만 아니라 `list`도 `value`가 될 수 있음
- Reduction: key를 기준으로 데이터를 묶어 처리
  - `reduceByKey`: 키 값을 기준으로 task 처리
  - `groupByKey`: 키 값을 기준으로 `value` 묶기
  - `sortByKey`: 키 값을 기준으로 정렬
  - `keys`: key 값 추출
  - `values`: value 값 추출
- 예시
  ```python
  count = pairs.reduceByKey(lambda a, b: a + b)
  ```
- 추가 연산
  - `join, rightOuterJoin, leftOuterJoin, subtractByKey`
- `key`를 변경하지 않는다면 `mapValues`를 사용하기
  - `Spark`내부에서 **파티션을 유지**하기 때문에 더 효율적
  - `mapValues()`, `flatMapValues()`