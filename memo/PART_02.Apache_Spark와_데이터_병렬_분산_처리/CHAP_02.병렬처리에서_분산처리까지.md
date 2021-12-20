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

## CH02_04. RDD Transformations and Actions
- **Transformations**
  - 결과값으로 **새로운 RDD** 반환
  - Lazy Evaluation
- **Actions**
  - 결과값을 연산하여 출력하거나 저장
  - list, python object
  - Eager Execution(즉시 실행)

### Narrow Transformation
- 1:1변환
- `filter, map, flatMap, sample, union`
- 1열을 조작하기 위해 **다른 열/파티션**의 데이터를 쓸 필요가 없음
- 정렬이 필요하지 않은 경우

### Wide Transformation
- Shuffling
- Intersection, join, distinct, cartesian, reduceByKey, groupByKey
- 아웃풋 RDD의 파티션에 다른 파티션의 데이터가 들어갈 수 있음
- 최소화, 최적화 해야 좋은 성능

## CH02_05. Cache & Persist
- 지연된 연산을 하는 이유?
  - **메모리**를 최대한 활용할 수 있음
    - `disk, network`연산 최소화
  - 데이터를 다루는 `task`는 반복되는 경우가 많음
- 어떤 데이터를 메모리에 남겨야할지 알아야함
  - Transformation은 **지연 실행**되므로, **메모리**에 저장 가능
- `cache`, `persist`로 메모리 저장 가능
- 예시 코드
  ```python
  # persist를 활용하여 메모리 저장 가능
  categoryReviews = filtered_lines.map(parse).persist()
  result1 = categoryReviews.take(10)
  result2 = categoryReviews.mapValues(lambda x: (x, 1)).collect()
  ```
- Regression에 활용 가능
  ```python
  points = sc.textFile("...").map(parsePoint).cache()
  for i in range(ITERATIONS):
    gradient = points.map(gradient_descent).reduce(lambda x,y: (x+y)) / n)
    w -= gradient * learning_rate
  ```
- Storage level
  - MEMORY_ONLY
  - MEMORY_AND_DISK: 메모리에 저장 이후, 없으면 DISK
  - MEMORY_ONLY_SER, MEMORY_AND_DISK_SER
    - 구조화된 데이터를 serialize하여 저장, 단 다시 읽을때 deserialize과정이 필요
    - 저장관점에서 이점
    - 단, 추가적인 연산 비용 발생
  - DISK_ONLY: DISK에만 저장
- **Cache**: default Storage level을 사용
  - **RDD**: `MEMORY_ONLY`
  - **DF**: `MEMORY_AND_DISK`
- **Persist**: `Storage level`을 사용자가 원하는대로 지정 가능

## CH02_06. Cluster Topology
- Spark 클러스터의 내부 구조
- Spark는 데이터가 여러곳에 분산되며, 같은 연산이어도 여러 노드에서 수행
- Driver - Cluster Manager - Worker
- 실제 코드가 어디서 구동될지, 생각을 하면서 코딩해야함

## CH02_07. Reduction Operations
- Reduction
  - 요소들을 모서 하로 합치는 작업
  - 많은 Spark의 연산들이 reduction
  - **근접하는 요소들을 모아서 하나의 결과로 나타내는 것**
- Action은 어떻게 분산된 환경에서 동작할지?
- 병렬 처리가 가능한 경우
  - Parallel Reduction
  - 파티션별로 독립적으로 처리가 가능해야함
  - 순서대로 처리하지 않아도 됨
- 대표적인 Reduction Actions  
  - `Reduce, Fold, GroupBy, Aggregate`

#### Reduce
```python
sc.parallelize([1,2,3,4,5]).reduce(add)
# 15
```
- 분산된 파티션들의 연산과, 합치는 부분을 나누어 생각해야 함
  ```scala
  // 26, 2+2 =4, (4,3) => 8+3 = (11,4), 22 + 4 = 26
  sc.parallelize([1,2,3,4],1).reduce(lambda x,y: (x*2)+y)
  // 18 (4, 10) => 8 + 10 = 18
  sc.parallelize([1,2,3,4],2).reduce(lambda x,y: (x*2)+y)
  ```
- 연산의 순서와 상관 없이 결과를 보장하려면 
  - **교환 법칙**과 **결합 법칙**을 고려해야 함

#### Fold
```python
# RDD.fold(zeroValue, <func>)
sc.parallelize([1,2,3,4,5]).fold(0, add)
```
- 파티션에 따라 헷갈리는 경우 존재
  ```python
  rdd = sc.parallelize([2,3,4], 4)
  # 24
  rdd.reduce(lambda x,y: x*y)
  # 24
  rdd.fold(1, lambda x,y: x*y)


  # 9
  rdd.reduce(lambda x, y: x+y)
  # 14, (1+1) + (1+2) + ... = 14
  rdd.fold(1, lambda x, y: x+y)
  ```

#### GroupBy
```python
rdd = sc.parallelize([1,1,2,3,5,8])
rdd.groupBy(lambda x: x % 2).collect()
sorted([(x, sorted(y)) for (x,y) in result])
# [(0, [2, 8]), (1, [1, 1, 3, 5])]
```

#### Aggregate
- RDD의 데이터 타입과, Action 결과 타입이 다를 경우 사용
- 파티션 단위의 **연산 결과**를 합치는 과정
  ```python
  RDD.aggregate(zeroValue, seqOp, combOp)
  # zeroValue: 각 파티션에서 누적할 시작 값
  # seqOp: 타입 변경 함수
  # combOp: 함치는 함수

  seqOp = (lambda x, y: (x[0] + y, x[1] + 1))
  combOp = (lambda x, y: (x[0] + y[0], x[1] + y[1]))
  sc.parallelize([1,2,3,4]).aggregate((0, 0), seqOp, combOp)
  # (10, 4)
  sc.parallelize([]).aggregate((0, 0), seqOp, combOp)
  # (0, 0)
  ```
  - 실상 `SeqOp`의 결과는 무시되는 것으로 보임
- KeyValueRDD
  - `groupByKey`, `reduceByKey`