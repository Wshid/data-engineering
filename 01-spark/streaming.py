from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# 소켓으로부터 데이터를 받아 처리하는 예시
spark = SparkSession.builder.appName("stream-word-count").getOrCreate()

lines_df = spark.readStream.format("socket").option("host", "localhost").option("port", "9999").load()

# explode: 배열 타입을 여러개의 row로 변환
words_df = lines_df.select(expr("explode(split(value, ' ')) as word"))
counts_df = words_df.groupBy("word").count()

word_count_query = counts_df.writeStream.format("console")\
                            .outputMode("complete")\
                            .option("checkpointLocation", ".checkpoint")\
                            .start()
word_count_query.awaitTermination()

# nc -lk 9999 // 소켓을 열어주는 명령어
# 이후, `spark-submit streaming.py`로 실행
# 구동시 초기에 enter(return)을 해주어야 outboundException이 발생하지 않음

# 다음과 같이, 소켓에 입력한 단어별로 aggregation
# socket이 끊기더라도, checkpoint directory를 통해 단어가 누적 될 수 있음
"""
22/01/29 15:07:38 INFO WriteToDataSourceV2Exec: Data source write support org.apache.spark.sql.execution.streaming.sources.MicroBatchWrite@3e3f2429 is committing.
-------------------------------------------
Batch: 8
-------------------------------------------
+---------+-----+
|     word|count|
+---------+-----+
|  session|    1|
|   stream|    1|
|   graphx|    2|
|streaming|    1|
|      sql|    1|
|    batch|    1|
|    spark|    4|
|  pyspark|    2|
|    abcde|    1|
|  builder|    1|
|        b|    1|
|        a|    2|
|         |    2|
+---------+-----+

22/01/29 15:07:39 INFO WriteToDataSourceV2Exec: Data source write support org.apache.spark.sql.execution.streaming.sources.MicroBatchWrite@3e3f2429 committed.
22/01/29 15:07:39 INFO CheckpointFileManager: Writing atomically to file:/Users/sion/Workspace/data-engineering/01-spark/.checkpoint/commits/8 using temp file file:/Users/sion/Workspace/data-engineering/01-spark/.checkpoint/commits/.8.a3da482b-45a4-4006-99d9-04bcb08b1c0c.tmp
22/01/29 15:07:39 INFO CheckpointFileManager: Renamed temp file file:/Users/sion/Workspace/data-engineering/01-spark/.checkpoint/commits/.8.a3da482b-45a4-4006-99d9-04bcb08b1c0c.tmp to file:/Users/sion/Workspace/data-engineering/01-spark/.checkpoint/commits/8
"""