from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, sum as _sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def get_user_selection():
    print("Seçiminizi yapın:")
    print("1 - Show login_fail_count greater than 0")
    print("2 - Show src2dst_bytes data in descending order")
    print("3 - Show request_types data")
    selection = input("Enter your choice: ")
    return selection

spark = SparkSession.builder \
    .appName("BruteForce") \
    .config("spark.jars", "pulsar-spark-connector_2.12-3.4.0.1.jar") \
    .getOrCreate()

schema = StructType([
    StructField("login_fail_count", StringType(), True),
    StructField("source_address", StringType(), True),
    StructField("destination_address", StringType(), True),
    StructField("src2dst_bytes", StringType(), True),
    StructField("src2dst_packets", StringType(), True),
    StructField("request_type", StringType(), True)
])

pulsar_service_url = "pulsar://localhost:6650"
topic = "persistent://public/default/login_fail_countTopic"

df = spark.readStream \
    .format("pulsar") \
    .option("service.url", pulsar_service_url) \
    .option("admin.url", "http://localhost:8080") \
    .option("topic", topic) \
    .option("subscription.name", "sub1") \
    .load()

parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data"))

final_df = parsed_df.select(
    col("data.login_fail_count").cast("integer").alias("login_fail_count"),
    col("data.source_address").alias("source_address"),
    col("data.destination_address").alias("destination_address"),
    col("data.src2dst_bytes").cast("integer").alias("src2dst_bytes"),
    col("data.src2dst_packets").cast("integer").alias("src2dst_packets"),
    col("data.request_type").alias("request_type")
)

user_selection = get_user_selection()

def process_batch(batch_df, batch_id):
    if user_selection == "1":
        filtered_df = batch_df.filter(col("login_fail_count") > 0)
        grouped_df = filtered_df.groupBy("source_address", "destination_address").agg(_sum("login_fail_count").alias("total_login_fail_count"))
        sorted_df = grouped_df.orderBy(col("total_login_fail_count").desc())
    elif user_selection == "2":
        grouped_df = batch_df.groupBy("source_address").agg(_sum("src2dst_bytes").alias("total_bytes"))
        sorted_df = grouped_df.orderBy(col("total_bytes").desc())
    elif user_selection == "3":
        sorted_df = batch_df.filter((col("request_type") == "GET") | (col("request_type") == "POST"))
    else:
        print("Invalid selection!")
        return

    sorted_df.show(truncate=False)

query = final_df.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("update") \
    .start()

query.awaitTermination()
