# CH03. Airflow로 Spark 파이프라인 관리하기

## CH03_01. Airflow로 Spark 파이프라인 관리하기 - Airflow와 Spark 같이 쓰기
```bash
pip install apache-airflow-providers-apache-spark
```
- spark-submit의 conn_id 등록
  - ![image](https://user-images.githubusercontent.com/10006290/152629132-966a484a-6d4a-4878-9f62-4b3462947364.png)
```bash
airflow tasks test spark-example submit_job 2021-01-01
```

## CH03_02. 택시비 예측 파이프라인 만들기 1
- X

## CH03_03. 택시비 예측 파이프라인 만들기 2
- X