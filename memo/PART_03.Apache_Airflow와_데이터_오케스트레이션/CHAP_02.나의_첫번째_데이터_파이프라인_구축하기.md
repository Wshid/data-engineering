# CH02. 나의 첫번째 데이터 파이프라인 구축하기

## CH02_01. NFT 파이프라인 프로젝트 소개
- OpenSea 사이트의 NFT데이터를 추출해 테이블에 저장하기
  - NFT: 인터넷 상 소유권, 블록체인으로 증명할 수 있는 프로덕트
  - OpenSea: 이 소유권을 사고 팔 수 있는 사이트
- 작업 절차
  - 테이블 생성 -> API 확인 -> NFT 정보 추출 -> NFT 정보 가공 -> NFT 정보 저장
- `api.opensea.io`에서 해당 정보 제공

## 02.02. DAG Skeleton
```bash
airflow webserver
airflow scheduler

cd ~/airflow
drwxr-xr-x   7 sion  staff     224  2  2 20:30 .
drwxr-xr-x+ 51 sion  staff    1632  2  2 20:30 ..
-rw-r--r--   1 sion  staff       5  2  2 20:27 airflow-webserver.pid
-rw-r--r--   1 sion  staff   43973  2  1 10:59 airflow.cfg
-rw-r--r--   1 sion  staff  647168  2  2 20:30 airflow.db
drwxr-xr-x   5 sion  staff     160  2  1 15:39 logs
-rw-r--r--   1 sion  staff    4695  2  1 10:59 webserver_config.py

# dag가 담길 코드
mkdir dags
ln -s ~/airflow/dags /Users/sion/Workspace/data-engineering/02-airflow/dags
vi nft-pipeline
```
- 이후 파이프라인을 작성
- 계속 새로고침을 해주어야 함(web page)
  - 실제 dag 파일이 web-server에 적용되는데 30초 이상의 시간이 걸리기 때문
- dag 에러 발생시 다음과 같이 출력
  - ![image](https://user-images.githubusercontent.com/10006290/152146912-e3aaa798-5a69-4eed-92d8-69c0b7d24c6a.png)
- 정상적인 파이프라인 생성
  - ![image](https://user-images.githubusercontent.com/10006290/152147233-ad41f161-dd86-4b1f-82c2-526e209e3088.png)

## 02.03. Operators
- 내부 Operator
  - **BashOperator**
  - **PythonOperator**
  - **EmailOperator**
- 외부 Operator
  - **Action Operator**: 액션을 실행
    - e.g. 어떤 데이터 추출한다던가, 프로세싱한다던가
  - **Transfer Operator**: 데이터를 옮길때 사용
  - **Sensors**: 조건이 맞을때까지 기다림
- 외부 Provider
  - 다양하게 존재
  - 각 Provider가 Operator를 만들어줌

## 02.04. Table 만들기
- Admin - connection(sqlite connection id 추가)
  - ![image](https://user-images.githubusercontent.com/10006290/152151139-fa843075-f967-4fad-a067-525f22a21536.png)
- DAG 테스트 방법
  ```bash
  airflow tasks test nft-pipeline creating_table 2021-01-01
  ```
- sqlite
  ```bash
  sqlite3 airflow.db
  .table # 전체 테이블 목록 확인
  .schema nfts # 스키마 확인
  ```

## 02.05. Sensor로 API 확인하기
- 코드상에 HttpSensor 추가
- connection_id 설정
  - DAG에 맞게 connection id를 동일하게 하여 아래와 같이 설정
    - ![image](https://user-images.githubusercontent.com/10006290/152152338-96f5b1cd-eff8-4759-b410-b575ea6af583.png)
- 테스트 방법
  ```bash
  airflow tasks test nft-pipeline is_api_available 2021-01-01
  ```

## 02.06. HttpOperator로 데이터 불러오기
```bash
airflow tasks test nft-pipeline extract_nft 2021-01-01
```

## 02.07. PythonOperator로 데이터 처리하기
```bash
airflow tasks test nft-pipeline process_nft 2021-01-01
```

## 02.08. BashOperator로 데이터 저장하기
```bash
airflow tasks test nft-pipeline store_nft 2021-01-01
``` 

## 02.09. 테스크간 의존성 만들기
```bash
creating_table >> is_api_available
```
- ![image](https://user-images.githubusercontent.com/10006290/152346110-57295282-3e84-4337-9679-22d15a9e4c67.png)
```bash
creating_table >> is_api_available >> extract_nft >> process_nft >> store_nft
```
- ![image](https://user-images.githubusercontent.com/10006290/152346482-632c0daf-48e4-471b-add1-d094fe9fc3e2.png)
- Failed task 발생시, modal내에서 log를 확인할 수 있음
  - ![image](https://user-images.githubusercontent.com/10006290/152346558-b23bfaab-b9bd-40c1-85ba-68a478d1e33e.png)

## 02.10. Backfill
- 어떤 파이프라인이 망가졌을때,
  - 망가지기 전 시점으로 돌아가 처음부터 다시 구동
- 매일 주기적으로 돌아가는 파이프라인을 멈췄다가 몇일 뒤 실행시키면 어떻게 될까?
  - 1/1, 1/2(중단), 1/3, 1/4(재구동)
- `catchup`
  - 1/4에 수행하더라도, 1/2, 1/3에 중단된 내용도 같이 실행
  ```python
  with DAG(dag_id='nft-pipeline', 
        schedule_interval='@daily', 
        default_args=default_args, 
        tags=['nft'], 
        # 특정 과거 시점부터 동작할 수 있도록 catchup=True로 변경
        catchup=True) as dag:
  ```
  - 단, `catchup=True`라도, 이전에 구동된 DAG가 있다면, 그 지점부터 수행하게 됨
- UI를 통해 단순히 컨트롤 가능