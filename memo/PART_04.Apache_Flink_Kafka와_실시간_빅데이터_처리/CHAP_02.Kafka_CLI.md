# CH02. Kafka CLI

## CH02_01. Zookeeper 콘솔에서 사용하기
```bash
/Users/sion/apps/kafka/bin/zookeeper-server-start.sh -daemon /Users/sion/apps/kafka/config/zookeeper.properties
```

## CH02_02. Broker 시작하기
```bash
/Users/sion/apps/kafka/bin/kafka-server-start.sh -daemon /Users/sion/apps/kafka/config/server.properties

# daemon이 정상적으로 구동되는지 확인
(base) ➜  bin netstat -an | grep 2181
tcp6       0      0  ::1.2181               ::1.49332              ESTABLISHED
tcp6       0      0  ::1.49332              ::1.2181               ESTABLISHED
tcp46      0      0  *.2181                 *.*                    LISTEN
(base) ➜  bin
```

## CH02_03. Topic 만들기
```bash
# create
/Users/sion/apps/kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic first-topic --partitions 1 --replication-factor 1

# list
/Users/sion/apps/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# describe
/Users/sion/apps/kafka/bin/kafka-topics.sh --describe --bootstrap-server localhost:9092
```

## CH02_04. Producer CLI
```bash
(base) ➜  bin /Users/sion/apps/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic first-topic
>kafka is fun
>spark is fun too
>third
>fourth
```