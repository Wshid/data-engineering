# CH01. Apache Flink & Kafka와 실시간 빅데이터 처리

## CH01_01. Kafka에 대해 알아보자
- Kafka: 분산 데이터 스트리밍 플랫폼
- Source: Kafka로 메세지를 보냄
- Destination: Kafka로부터 메세지를 받음
- 확장성이 있고, 장애 허용(fault tolerant)하며 성능이 좋음

### Kafka를 도입했을 때의 장점
- 시스템간 의존성을 간접적으로 만듦
- 확장성: 새 시스템을 더할때마다 복잡도가 선형적으로 올라감
- Kafka를 이용해 통신 프로토콜 통합이 쉬움
- **확장성**: 하루에 1조개 메세지 처리 가능, Petabyte의 데이터 처리 가능
- **메세지 처리속도**: 2ms
- *가용성*: 클러스터 환경에서 작동
- **데이터 저장 성능**: 분산 처리, 내구성, 장애 허용

### Kafka의 활용처
- 시스템간 메세지 큐
- 로그 수집
- 스트림 프로세싱
- 이벤트 드리븐 기능들

### 유명 기업의 Kafka 사용
- Netflix: 실시간 모니터링
- Expedia: 이벤트 드리븐 아키텍처
- Uber: 실시간 가격 조정, 실시간 수요 예측

## CH01_02. Kafka의 구조
- Topic: 채널, 폴더와 같은 개념, Producer, consumer가 공유하는 채널
- Broker: 서버
- Producer
- Consumer
- Partition
- Message
- Offset
- Consumer Group
- Cluster
- Zookeeper

## CH01_03. Topics, Partitions, 그리고 Messages
- **Kafka Topic**
  - 데이터 스트림이 어디에 Publish될지 정하는데 쓰임
  - 파일 시스템의 폴더 개념과 유사
- **Producer**
  - 토픽을 지정하고 메세지를 게시(post)
- **Consumer**
  - 토픽으로부터 메세지를 받음
- 카프카의 메세지는 **디스크에 정렬**되어 저장 되며,
  - 새로운 메세지가 도착하면 지속적으로 로그에 기록

### Partitions
- 토픽 = 파티션의 그룹
- 디스크에는 **파티션**단위로 저장
- 파티션마다 `commit log`가 쌓임
- 파티션에 쌓이는 기록들은 **정렬**되어 있으며, `immutable`함
- 파티션의 모든 기록들은 `Offset`이라는 `id`를 부여 받음

### Message
- Byte의 배열
- 단순 String, JSON이나 Avro 사용
  - Avro: 타입이 있는 JSON
- 메세지 크기에는 제한이 없음
- **성능을 위해 작게 유지하는 것을 추천**(KB ~ MB)
- 데이터는 사용자가 지정한 시간만큼 저장(**Retention Period**)
- **Topic별**로 지정도 가능
- Consumer가 데이터를 받아가고 나서도 데이터는 저장됨
- Retention Period가 지나면, 데이터는 자동으로 삭제됨

## CH01_04. Cluster & Replication
### Cluster
- 카프카 클러스터는 여러개의 **카프카 브로커**(서버)를 가질 수 있음
- 카프카 토픽을 생성하면, 모든 카프카 브로커에 생성
- 카프카 파티션은 **여러 브로커에 걸쳐서 생성**
- Producer가 메세지를 게시하면 **Round-Robin**방식으로 파티션에 분배
- 같은 Key를 가진 메세지들은 같은 Partition에게 보내짐

### Replication Factor
- 파티션이 n개의 브로커에 복제되어 담긴다는 개념
- 각 브로커는 복제된 파티션 중 대표를 하는 **파티션 리더**를 가짐
- 모든 Read/Write는 파티션 리더를 통해 이루어짐
- 다른 파티션들은 **파티션 리더**를 복제

## CH01_05. Producer
- Message -> Topic
- 카프카 토픽으로 메세지를 게시(post)하는 클라이언트 어플리케이션
- 메세지를 어느 파티션에 넣을지 결정(key)
- Client Application
- 메세지를 어느 파티션으로 보낼지 결정
- **Partition Key**를 지정하지 않으면 **Round Robin 방식**으로 각 파티션에 메세지를 분배
- Partition Key를 지정하면, 같은 키를 가진 메세지가 같은 파티션에 들어감

## CH01_06. Consumer
- 각 Consumer group은 모든 파티션으로부터 데이터를 받을 수 있음
- Consumer는 지정된 파티션으로부터 데이터를 받을 수 있음
- Consumer Rebalancing
- Client Application
- **Consumer**와 **Consumer Group**이 존재
- Consumer Group을 지정하지 않으면 새로운 **Consumer Group**에 배정
- Consuemr Group안의 두 Consumer는 **같은 파티션으로부터 동시에 메세지를 받을 수 없음**
- Consumer가 제거되거나 추가될 때 rebalancing이 이루어짐

## CH01_07. Zookeeper
- Consumer와 통신
- 메타 데이터 정보 저장
- 카프카 상태관리
- 분산 시스템간의 정보 공유, 상태 체크, 서버들간의 동기화
- 분산 시스템의 일부이기 때문에 동작을 멈춘다면 분산 시스템에 영향
- 주키퍼 역시 클러스터로 구성
- 클러스터는 **홀수**로 구성되어
  - 문제가 생겼을 경우
  - **과반수**가 가진 데이터를 기준으로 **일관성** 유지
  
### 주키퍼의 역할
- **클러스터 관리**
  - 클러스터에 존재하는 브로커를 관리하고 모니터링
- **Topic 관리**
  - 토픽 리스트를 관리
  - 토픽에 할당된 파티션과 Replication 관리
- **파티션 리더 관리**
  - 파티션의 리더가 될 브로커를 선택하고
  - 리더가 다운될 경우, 다음 리더를 선택
- **브로커들끼리 서로를 발견할 수 있도록 정보 전달**

## CH01_08. 카프카 설치
```bash
wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz
tar -xzvf https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz
mv kafka_2.13-3.1.0 /Users/sion/apps/.
cd /Users/sion/apps
ln -s kafka_2.13-3.1.0 kafka
```