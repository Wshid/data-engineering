# CH03. Spark SQL, DataFrame, Dataset

## CH03_01. Structured vs Unstructured Data
- `filter/join`의 순으로 처리하는 것이 `join/filter`보다 성능이 좋음
  - 이를 계속 개발자가 고려해야 할까?
- 데이터가 구조화되어 있다면 최적화가 가능
- **Unstructured**: free form
  - 로그 파일
  - 이미지
- **Semi Structured**: 행과 열
  - CSV
  - JSON
  - XML
- **Structured**: 행과 열 + 데이터 타입(스키마)
  - 데이터베이스 
- **RDD**의 경우
  - 데이터의 구조를 모르기 때문에, 데이터 다루는 것을 **개발자**에게 의존
  - `map, flatMap, filter`등을 통해 유저가 만든 function을 수행
- **Structured Data**에선
  - 데이터의 구조를 이미 알고 있으므로, 어떤 태스크를 수행할 것인지 정의만 하면 됨
  - **최적화도 자동으로 가능**
- **SparkSQL**은 구조화된 데이터를 다룰 수 있게 해줌
  - 유저가 일일히 function을 정의할 필요가 없음
  - 자동으로 **연산 최적화**

## CH03_02. Spark SQL 소개
- Spark SQL의 목적
  - Spark 프로그래밍 내부에서 **관계형 처리**
  - 스키마 정보를 이용한 자동 최적화
  - 외부 데이터 셋을 사용하기 쉽게 하기 위함
- Spark SQL
  - 스파크 위에 구현된 하나의 패키지
    - `SQL, DataFrame Dataset`
  - 2개의 backend component
    - **Catalyst**: 쿼리 최적화 엔진
    - **Tungsten**: Serializer
- Spark Core: RDD
- Spark SQL : DataFrame
  - DataFrame
    - 테이블 데이터셋
    - RDD에 스키마가 적용된 형태
- `SparkSession`을 사용
  - `SparkContext`는 Spark Core에서 사용
- 데이터를 생성하는 방법
  - RDD에서 스키마를 정의 이후 변형
    - Schema를 자동으로 유추하여 DataFrame 만들기
      ```python
      df = spark.createDataFrame(proprecessed)
      ```
    - Schema를 사용자가 정의
      ```python
      schema = StructType(
        StructField("name", StringType(), True),
        ...
      )
      spark.createDataFrame(proprecessed, schema).show()
      ```
  - CSV, JSON 데이터를 받아오기
    ```python
    spark = SparkSession.builder.appName("...").getOrCreate()

    dataframe = spark.read.json("...")
    dataframe_txt = spark.read.text("...")
    dataframe_csv = spark.read.csv("...")
    dataframe_parquet = spark.rread.load("...")
    ```
- DataFrame을 하나의 데이터베이스 테이블처럼 사용하려면
  - `createOrReplaceTempView()`함수를 사용
- Hive Query Language와 거의 동일하게 사용 가능
- `SparkSession`으로 불러오는 데이터는 `DataFrame`
- SQL 및 function을 사용하여 쿼리가 가능 
- `df`를 `rdd`로 변환도 가능하나,
  - rdd를 덜 사용하는것이 좋음
    - MlLib이나 Spark Streaming과 같은 타 스파크 모듈과 사용하기 편함
    - 개발하기 편함
    - 최적화가 알아서 진행됨
- `DataSet`
  - **Type이 있는 DataFrame**
  - **Pyspark에서는 크게 신경쓰지 않아도 됨**

## CH03_03. SQL 기초
- X

## CH03_04. DataFrame
- DataFrame의 사용법
  - DataFrame의 데이터 타입
  - DataFrame에서 가능한 연산들
  - DataFrame에서의 Aggregation 작업
- DataFrame
  - 관계형 데이터셋: RDD + Relation
  - RDD가 **함수형 API**라면
  - DataFrame은 **선언형 API**
  - 자동으로 최적화가 가능
  - 타입이 없음
- DataFrame: RDD의 확장판
  - Lazy Execution
  - 분산 저장
  - Immutable
  - Row 객체 존재
  - SQL 쿼리를 실행할 수 있음
  - 스키마를 가질 수 있고
    - 이를 통해 성능을 더 최적화 할 수 있음
  - `csv, json, hive`등으로 읽어오거나 변환 가능
- methods
  - dtypes: 내부 변수의 스키마 파악 가능
  - `show()`
  - printSchema()
- 복잡한 데이터 타입
  - `ArrayType, MapType, StructType`

### 주요 메서드
- `select`
  ```python
  df.select(*).collect()
  df.select('name', 'age').collect()
  df.select(df.name, (df.age + 10).alias('age')).collect()
  ```
- `agg`: 그룹핑 후 데이터를 하나로 합치는 작업
  ```python
  df.agg({'age': 'max'}).collect()
  df.agg(F.min(df.age)).collect()

  # currency, avg(price)를 column으로 하는 df 생성
  df.groupBy("currency").agg(avg("price")).show()
  
  # currency, count(price)를 column으로 하는 df 생성
  df.groupBy("currency").agg(count("price")).show()
  ```
- `groupBy`: 사용자가 지정한 `Column`을 기준으로 데이터를 Grouping하는 작업
  ```python
  df.groupBy().avg().collect()
  sorted(df.groupBy('name').agg({'age': 'mean'}).collect())
  sorted(df.groupBy(df.name).avg().collect())
  sorted(df.groupBy(['name', df.age]).count().collect())
  ```
- `join`
  ```python
  # 두 데이터 프레임에 해당하는 내용을 select 할 수 있음
  df.join(df2, 'name').select(df.name, df2.height).collect()
  ```

## CH03_05. Spark SQL로 트립 수 세기
- X

## CH03_06. Spark SQL로 뉴욕의 각 행정구 별 데이터 추출하기
- X