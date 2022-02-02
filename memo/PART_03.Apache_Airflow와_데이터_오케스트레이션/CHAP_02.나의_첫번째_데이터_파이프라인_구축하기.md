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