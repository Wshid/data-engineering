## CH01_01. 기초 환경 설정(맥)
- anaconda를 통한 python 설치
- brew를 통한 java 설치
```bash
# open jdk8
brew install -cask adoptopenjdk8
# scala
brew install scala
# spark
brew install apache-spark
# pyspark
pip --version
pip install pyspark
```

## CH01_03. 모빌리티 데이터 다운로드
- 아래 데이터 다운로드(2020.03)
  - https://nyc-tlc.s3.amazonaws.com/trip+data/fhvhv_tripdata_2020-03.csv
- raw-data의 필드명
  - hvfhs_license_num: 회사 면허 번호
  - dispatching_base_num: 지역 라이선스 번호
  - pickup_datetime: 승차 시간
  - dropoff_datetime: 하차 시간
  - PULocationID: 승차 지역 ID
  - DOLocationID: 하차 지역 ID
  - SR_Flag: 합승 여부 Flag

## CH01_04. 우버 트립 수 세기
- spark 코드 구동시 `pandas`를 찾지 못하는 상황 발생
```log
(base) ➜  01-spark git:(main) ✗ spark-submit count_trips.py
21/12/11 18:27:52 WARN Utils: Your hostname, wshid-MacBookPro.local resolves to a loopback address: 127.0.0.1; using 192.168.0.18 instead (on interface en0)
21/12/11 18:27:52 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
WARNING: An illegal reflective access operation has occurred
WARNING: Illegal reflective access by org.apache.spark.unsafe.Platform (file:/usr/local/Cellar/apache-spark/3.2.0/libexec/jars/spark-unsafe_2.12-3.2.0.jar) to constructor java.nio.DirectByteBuffer(long,int)
WARNING: Please consider reporting this to the maintainers of org.apache.spark.unsafe.Platform
WARNING: Use --illegal-access=warn to enable warnings of further illegal reflective access operations
WARNING: All illegal access operations will be denied in a future release
Traceback (most recent call last):
  File "/Users/sion/Workspace/data-engineering/01-spark/count_trips.py", line 3, in <module>
    import pandas as pd
ModuleNotFoundError: No module named 'pandas'
log4j:WARN No appenders could be found for logger (org.apache.spark.util.ShutdownHookManager).
log4j:WARN Please initialize the log4j system properly.
log4j:WARN See http://logging.apache.org/log4j/1.2/faq.html#noconfig for more info.
(base) ➜  01-spark git:(main) ✗ pip install pandas         
Requirement already satisfied: pandas in /Users/sion/opt/anaconda3/lib/python3.9/site-packages (1.3.4)
Requirement already satisfied: python-dateutil>=2.7.3 in /Users/sion/opt/anaconda3/lib/python3.9/site-packages (from pandas) (2.8.2)
Requirement already satisfied: pytz>=2017.3 in /Users/sion/opt/anaconda3/lib/python3.9/site-packages (from pandas) (2021.3)
Requirement already satisfied: numpy>=1.17.3 in /Users/sion/opt/anaconda3/lib/python3.9/site-packages (from pandas) (1.20.3)
Requirement already satisfied: six>=1.5 in /Users/sion/opt/anaconda3/lib/python3.9/site-packages (from python-dateutil>=2.7.3->pandas) (1.16.0)
```
- 관련 내용
  - https://discuss.cloudxlab.com/t/importerror-no-module-named-pandas-pyspark/6527/4
- 해결 방법 #1 - 실패
  ```bash
  # 기존 local python의 pandas와는 다른 패키지로 설치 필요
  pip install pyspark-pandas
  ```
- 해결 방법 #2 - pip과 python의 위치가 다를 경우
  - https://bladewalker.tistory.com/713
  ```log
  base) ➜  01-spark git:(main) ✗ which pip
  /Users/sion/opt/anaconda3/bin/pip
  (base) ➜  01-spark git:(main) ✗ which python
  /usr/bin/python
  ```
  - 실제 현재 위치가 다른 상황
- 신규 가상 환경 추가
  ```bash
  conda create --name py3 python=3.9
  conda activate py3
  # numpy 없이 pandas를 설치하게 되면, 맥북상에서 설치가 상당히 지연됨
  pip install numpy
  pip install pandas
  pip install pyspark
  ```
- spark-submit
  ```bash
  cd 01-spark
  spark-submit count_trips.py
  ```
- interactive window에서 `visualize_trips_date.py` 수행 결과
  - ![image](https://user-images.githubusercontent.com/10006290/145673418-3ba01258-e1dd-4a37-8e81-8cc57d853abf.png)


## CH01_05. Spark에 대해 알아보자
- HDFS: 파일 시스템
- Map Reduce: 연산 엔진
  - **Spark**
- Yarn: 리소스 관리
- 고속 = 빅데이터의 In-memory 연산
- Cluster Manager
  - Hadoop - Yarn
  - AWS - Elastic MapReduce
- Spark의 성능
  - Hadoop MR보다 빠름
    - 메모리상 100배
    - 디스크상 10배
  - Lazy Evaluation
    - 실행이 필요할때까지 기다림

## CH01_06. Spark는 어떻게 진화하고 있을까
- spark 1,2,3동안 어떻게 변했는지
- Spark 1.x
  - Dataframe(v1.3)
- Spark 2.x
  - Structured Streaming
  - Catalyst Optimizer Project: 언어에 상관없이 동일한 성능
- Spark 3.x
  - Spark SQL 기능 추가
  - Spark 2.4보다 2배 빠른 성능
    - Adaptive execution
    - Dynamic partition pruning
  - DL
    - GPU 노드 지원
    - ML Framework 연계 가능
  - GraphX
  - python2 deprecated
  - k8s 지원 강화
- Spark의 현재 구성
  - Spark Core, Spark SQL, Spark Streaming, MLlib, GraphX

## CH01_07. RDD
- Resilient Distributed DataSet(RDD)

### RDD의 특징
- 데이터는 클러스터에 흩어져있으나, 하나의 파일인것처럼 사용 가능
  - `lines = sc.textFile(...)`
- 탄력적이고 불변
  - 네트워크 장애, HW/MEM 장애, 여러가지 이유..
  - 데이터가 Immutable하다면 동적 대응 가능
  - RDD1이 변환되면 RDD2가 새로 생성
    - 변환을 거치면서 연산을 기록할 수 있음
  - **RDD의 변환과정**은 **Acyclic Graph**로 그릴 수 있음
    - 문제가 발생했을 경우, 쉽게 전 RDD로 돌아갈 수 있음
  - 이를 탄력적이라고 함
- Type-Safe
  - Compile time에 검증 가능
- Unstructured/Structured
  - Unstructured: 텍스트 데이터, 로그, 자연어, ...
  - Structured: RDB, DataFrame, ...
- Lazy
  - 결과가 필요할때까지 연산을 하지 않음
  - T(Transformation), A(Action)
    - Action까지 T를 실행하지 않음

### RDD를 쓰는 이유
- 유연, 짧은 코드
- 개발시, **무엇**보다는 **어떻게**(how-to)에 초점

## CH01_08. 코드 한줄씩 파헤치기
```bash
pip install jupyter
```