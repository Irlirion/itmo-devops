import random
import json
import os
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

conf = SparkConf().setAppName("DataPipeline").setMaster("spark://spark-master:7077")
spark = SparkSession.builder.config(conf=conf).getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# Generate 50 random numbers
data = [(float(random.randint(1, 100)),) for _ in range(50)]
df = spark.createDataFrame(data, ["value"])

# Calculate statistics
stats_row = df.agg(
    F.sum("value").alias("total"),
    F.avg("value").alias("average"),
    F.min("value").alias("min"),
    F.max("value").alias("max"),
    F.count("value").alias("count"),
).collect()[0]

stats = {
    "total": float(stats_row["total"]),
    "average": round(float(stats_row["average"]), 2),
    "min": float(stats_row["min"]),
    "max": float(stats_row["max"]),
    "count": int(stats_row["count"]),
}
print(f"Statistics: {stats}")

# Transform: multiply by 2, filter values above doubled average
df_transformed = df.withColumn("value", F.col("value") * 2)
df_above_avg = df_transformed.filter(F.col("value") > stats["average"] * 2)

transformation = {
    "transformed_count": df_transformed.count(),
    "above_average_count": df_above_avg.count(),
    "original_avg": stats["average"],
    "transformed_avg": round(float(df_transformed.agg(F.avg("value")).collect()[0][0]), 2),
}
print(f"Transformation: {transformation}")

os.makedirs("/opt/airflow/output", exist_ok=True)
result = {"statistics": stats, "transformation": transformation}
with open("/opt/airflow/output/spark_result.json", "w") as f:
    json.dump(result, f, indent=2)

print("Results saved to /opt/airflow/output/spark_result.json")
spark.stop()
