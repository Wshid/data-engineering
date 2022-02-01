# CH01. Apache Airflow 알아보기

## CH01_01. 워크플로우 관리를 위한 에어플로우
- Airflow
  - 에엉비엔비에서 개발한
  - **워크플로우 스케줄링**, **모니터링 플랫폼**
  - 실제 데이터의 처리가 이루어지는 곳은 아님
- 예시: 매일 10시에 주기적으로 돌아가는 데이터 파이프라인 만들려면?
  - Download -> Process -> Store
  - 외부 API -> SparkJob -> DB

#### 기존 방식의 문제점
- **실패 복구**
  - 언제 어떻게 다시 실행할 것인가? Backfill?
- **모니터링**
  - 잘 돌아가고 있는지 어떻게 확인하기 힘듦
- **의존성 관리**
  - 데이터 파이프라인간 의존성이 있는 경우
  - 상위 데이터 파이프라인이 잘 돌아가고 있는지 파악이 어려움
- **확장성**
  - 중앙화해서 관리하는 툴이 없기 때문에
  - 분산된 환경에서 파이프라인들을 관리하기 어려움
- **배포**
  - 새로운 워크플로우를 배포하기 어려움

#### Airflow란?
- **워크플로우**를 작성하고, **스케줄링**하고
- **모니터링**하는 작업을 **프로그래밍**할 수 있게 해주는 플랫폼

#### Airflow의 특징
- 파이썬 사용
- 분산된 환경에서의 **확장성**
- 웹 대시보드 (UI)
- 커스터마이징 가능

#### 워크플로우
- 의존성으로 연결된 task들의 집합
- 의존성으로 연결된 것을 `DAG`라고 함

#### Airflow의 컴포넌트
- **웹 서버**
  - 웹 대시보드 UI
- **스케줄러**
  - 워크플로우가 **언제** 실행되는지 관리
- **Metastore**
  - 메타데이터 관리
- **Executor**
  - task가 **어떻게** 실행되는지 정의
- **Worker**
  - task를 **실행**하는 프로세스

#### Operator
- Task를 정의하는데 사용
- **Action Operators**
  - 실제 연산 수행
- **Transfer Operators**
  - 데이터를 옮김
- **Sensor Operators**
  - task를 언제 실행시킬 **트리거**를 기다림

#### Task
- `Operator`를 실행시키면 `Task`가 됨
- `Task = Operator Instance`

#### Airflow의 활용처
- 데이터 웨어하우스
- 머신러닝
- 분석
- 실험
- 데이터 인프라 관리

## CH01_02. AirFlow의 구조

### One-node Architecture
- Web Server
- Scheduler
- Metastore
- Executor
  - Queue가 존재
- 구동 순서
  - Web Server와 Scheduler가 Metastore에서 정보를 읽어옴
  - Executor로 해당 정보를 보내어 task 실행
  - DAG의 task의 상태는 Metastore로 업데이트
  - 업데이트된 상태를 Web Server와 Scheduler가 읽어들임
    - task가 잘 완료되었는지 확인

### Multi-node Architecture
- Queue가 Executor 바깥에 존재
  - Queue = Celery Broker

### 정리
- DAG를 작성하여 **Workflow**를 만듦
  - DAG는 **Task**로 구성됨
- Task는 Operator가 인스턴스화 된 것
- DAG를 실행시킬 때, Scheduler는 **DagRun** 오브젝트 생성
  - `Dag의 인스턴스 = Dag 오브젝트`
- DagRun 오브젝트는 Task Instance를 만듦
- Worker가 Task를 수행 후 DagRun의 상태를 **완료**로 바꿈

## CH01_03. Airflow 설치

### airflow 설치
```bash
pip --version
pip install apache-airflow
# airflow는 내부 웹서버를 Flask 사용
```
- 설치 완료시 `~`에 `airflow`가 생성됨

### airflow 초기화 및 admin 생성
```bash
# airflow 초기화 과정
airflow db init
airflow webserver -p 8080

# 신규 사용자 생성
airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
```

### 구동 완료 화면
- ![image](https://user-images.githubusercontent.com/10006290/151902642-99ebdb3e-9223-4151-abb8-0d8358a8cba0.png)
