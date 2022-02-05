from datetime import datetime
import json
from airflow import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
# 내장이기때문에 providers 하위에 있지 않음
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from pandas import json_normalize

default_args = {
    'start_date': datetime(2021, 1, 1),
}

def _processing_nft(ti):
    # ti = task instance
    assets = ti.xcom_pull(task_ids=['extract_nft'])
    if not len(assets):
        raise ValueError("assets is empty")
    nft = assets[0]['assets'][0]

    processed_nft = {
        'token_id': nft['token_id'],
        'name': nft['name'],
        'image_url': nft['image_url'],
    }
    processed_nft.to_csv('/tmp/processed_nft.csv', index=None, header=False)

with DAG(dag_id='nft-pipeline', 
        schedule_interval='@daily', 
        default_args=default_args, 
        tags=['nft'], 
        catchup=False) as dag:
    
    # 새로운 테이블 만들기
    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        # connection id는 ui에서 생성
        # Admin - connection 탭 
        sql='''
            CREATE TABLE IF NOT EXISTS nfts (
                token_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                image_url TEXT NOT NULL
            )
        '''
    )

    # CloudFlare 403 에러 우회하기 위해 extra_options 사용
    ## https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/sensors/http/index.html
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='opensea_api',
        endpoint='api/v1/assets?collection=doodles-official&limit=1',
        extra_options={'check_response': False}
    )

    # 디버깅 용도로 log_response 사용
    # extra_option을 사용해도 정상적으로 작동하지 않음
    ## extra_options 다른 옵션들, 의미는 없음: https://stackoverflow.com/questions/57807560/documentation-for-airflow-http-operator-sensor-extra-options
    extract_nft = SimpleHttpOperator(
        task_id='extract_nft',
        http_conn_id='opensea_api',
        endpoint='api/v1/assets?collection=doodles-official&limit=1',
        method='GET',
        response_filter=lambda res: json.loads(res.text),
        log_response=True,
        extra_options={'check_response': False},
        headers={'Content-Type': 'application/json'}
    )

    process_nft = PythonOperator(
        task_id='process_nft',
        python_callable=_processing_nft
    )

    store_nft = BashOperator(
        task_id='store_nft',
        bash_command='echo -e ".separator ","\n.import /tmp/processed_nft.csv nfts" | sqlite3 /Users/sion/airflow/airflow.db'
    )

    # task간 의존성을 갖게 하는 과정
    creating_table >> is_api_available >> extract_nft >> process_nft >> store_nft