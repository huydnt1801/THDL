from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.2.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'
KAFKA_TOPIC_NAME = "muaban"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

spark = (
        SparkSession.builder.appName("Kafka Pyspark Streamin Learning")
        .master("local[*]")
        .getOrCreate()
    )
spark.sparkContext.setLogLevel("ERROR")

# STEP 2 : reading a data stream from a kafka topic

sampleDataframe = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", 'localhost:9092')
    .option("subscribe", KAFKA_TOPIC_NAME)
    .option("startingOffsets", "earliest")
    .load()
)
sampleDataframe.show(truncate = False)
base_df = sampleDataframe.selectExpr("CAST(key as STRING)", "CAST(value AS STRING)")
result_1 = base_df.selectExpr("CAST(key AS STRING)",).withColumn("value", to_json(struct("*")).cast("string"),)
# print(result_1)


# STEP 3 : Applying suitable schema

# sample_schema = (
#         StructType()
#         .add("col_a", StringType())
#         .add("col_b", StringType())
#         .add("col_c", StringType())
#         .add("col_d", StringType())
#     )

# info_dataframe = base_df.select(
#     from_json(col("value"), sample_schema).alias("info"), "value"
# )

# info_dataframe.printSchema()
# info_df_fin = info_dataframe.select("info.*", "value")
# info_df_fin.printSchema()

schema = (
    StructType()
    .add("name", StringType())
    .add("price", StringType())
    .add("address", StringType())
    .add("url", StringType())
)
df = base_df.select(from_json(base_df.value, schema).alias("data"))
# query = df.select("data.name", "data.price", "data.address", "data.url").writeStream.format("csv").option("checkpointLocation", "checkpoint/") \
#   .option("header", "true") \
#   .option("path", "/home/edkl/project/20222/THDL/BTL/THDL/spark/") \
#   .outputMode("append") \
#   .start()
df.printSchema()
df.select("data.name", "data.price", "data.address", "data.url").writeStream.format("console").outputMode("append").start()
query = df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# pandas_df = df.select("data.name", "data.price", "data.address", "data.url")\
#     .toPandas()
# print(pandas_df)
query.awaitTermination()
# df = df.select("data.id", "data.name")

# # STEP 4 : Creating query using structured streaming

# query = info_df_fin.groupBy("url").agg(
#     approx_count_distinct("col_b").alias("col_b_alias"),
#     count(col("col_c")).alias("col_c_alias"),
# )

# # query = query.withColumn("query", lit("QUERY3"))
# result_1 = query.selectExpr(
#     "CAST(col_a AS STRING)",
#     "CAST(col_b_alias AS STRING)",
#     "CAST(col_c_alias AS STRING)",
# ).withColumn("value", to_json(struct("*")).cast("string"),)