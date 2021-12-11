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