# CH05. Spark Streaming

## CH05_01. Spark Streaming
- SQL엔진 위에 만들어진 분산 스트림 처리 프로세싱
- 시간대별로 데이터를 aggregate
- Kafka, Amazon Kinesis, HDFS 등과 연결 가능
- Checkpoint를 만들어서 **부분적인 결함**이 발생해도
  - 다시 돌아가서 데이터를 처리할 수 있음
  - Fault Tolerant
- 데이터 스트림은 **무한한 테이블**

### DStream
- Spark Stream의 기본적인 추상화
- 내부적으론 **RDD의 연속**이고 **RDD의 속성**을 이어받음
  - 불변, 분산저장된다는 RDD의 특징을 가져옴
- DStream
  - 시간대별로 RDD의 snapshot을 가짐(구간별)

### Window
- 지금의 데이터를 처리하기 위해, **이전 데이터**에 대한 정보가 필요할 때

### Stream 쿼리 예시
- 데이터를 어디에서 가져올지 명시
- 여러 데이터 소스를 `join(), union()`등으로 합쳐 사용 가능
- 코드 예시
  ```python
  spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", ...)
    .option("subscribe", "topic")
    .load()
    # transformation
    .selectExpr("cast(value as string) as json")
    .select(from_json("json", schema).as("data"))
    # save
    .writeStream.format("parquet")
    .trigger("1 minute") # micro batch 실행 간격
    .option("checkpointLocation", "...")
    .start()
  ```

### Spark Streaming의 특징
- 여러 **Transformation** 사용 가능
  - `Map, FlatMap, Filter, ReduceByKey, ...`
- 이전 데이터에 대한 정보를 `State`로 주고 받을 수 있음
  - 카테고리별(**키값 별**) 총합