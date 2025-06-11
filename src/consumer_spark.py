from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Initialize Spark session
spark = SparkSession.builder.appName("KafkaConsumer").getOrCreate()

# Kafka configuration
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "your-msk-bootstrap-servers") \
    .option("subscribe", "transactions") \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.sasl.jaas.config", "org.apache.kafka.common.security.plain.PlainLoginModule required username='your-username' password='your-password';") \
    .load()

# Define schema
schema = StructType([
    StructField("transaction_id", StringType()),
    StructField("amount", DoubleType()),
    StructField("timestamp", StringType()),
    StructField("customer_id", StringType())
])

# Parse JSON data
parsed_df = kafka_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Aggregate data (e.g., total amount per customer)
agg_df = parsed_df.groupBy("customer_id").sum("amount").alias("total_amount")

# Write to S3
query = agg_df.writeStream \
    .format("parquet") \
    .option("path", "s3://your-bucket/processed-data/") \
    .option("checkpointLocation", "s3://your-bucket/checkpoints/") \
    .start()

query.awaitTermination()