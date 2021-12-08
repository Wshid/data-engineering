## CH01_02. 모던 데이터 엔지니어링
- AS-IS: ETL(Extract, Transformation, Load)
- TO-BE: ELT(Extract, Load, Transformation)
- 클라우드 웨어 하우스
  - snowflake, Google Big Query
- Hadoop -> Databricks, Presto
- Source -> Ingestion & Transformation -> Storage -> Query/Processing -> Output
  - Source
    - Log, Database
  - **Ingestion & Transformation**
    - Airflow, Kafka, Pandas, Spark, Flink,Hive
  - Storage
    - Parquet, S3, HDFS
  - Query
    - Presto, Dremio
  - **Processing**
    - Tensorflow, Pytorch, Spark, SparkML, Flink
  - Output
    - Tableau, Looker

## CH01_03. Batch & Stream
- .

## CH01_04. Dataflow Orchestration
- Orchestration tool?
  - 테스크 스케줄링
  - 분산 실행
  - 테스크간 의존성 관리
- AirFlow를 사용하면 Orchestration이 가능
  - 어디까지 task가 진행되었는지 등

## CH01_05. 데이터 엔지니어링
- Michelangelo
  - 쉽게 머신러닝 알고리즘을 학습하고 배포할 수 있는 플랫폼
  - 우버 내부 툴
  - 우버 블로그에 자세히 설명되었다고 함
- 머신러닝 학습은 무거운 프로세스 -> 배치 형태
- 이후 모델을 실시간 처리에서 활용
- Batch Pipeline
  - Data(Source) -> Spark Job(Data preprocessing) -> Spark Job(ML) -> Data(저장)
  - Spark Job들은 `Airflow Orchestration`을 통해 관리
- Stream Pipeline
  - Data -> Kafka -> Flink -> Data