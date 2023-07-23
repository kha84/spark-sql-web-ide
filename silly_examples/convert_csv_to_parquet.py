from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql import Window, functions as F
sys.path.append('../')
from spark_sql_app_config import * 
import pandas as pd

# Check if input CSV file exists
if len(sys.argv) < 3 or sys.argv[1] == '--help':
    print('Usage: python read_csv_to_pyspark.py <filename.csv> <filename.parquet>')
else:
    try:
        
        # Create a Spark Session
        spark = SparkSession.builder.appName("MinioTest") \
            .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
            .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint) \
            .config("spark.hadoop.fs.s3a.access.key", minio_access_key) \
            .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key ) \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .getOrCreate()
            
        # Read DataFrame from csv and save it as parquet
        csv_filename = sys.argv[1]
        parquet_filename = sys.argv[2] 
        print(f"Reading file {csv_filename}")
        spark_df = spark.read.option("inferSchema",True).option("delimiter",",").option("header",True).csv(csv_filename)
        print("Spark DataFrame Created from CSV file: ")
        spark_df.show()
        print(f"Saving file to S3 as '{parquet_filename}' to '{minio_bucket_name}' bucket")
        spark_df.write.mode('overwrite').parquet(f"./{parquet_filename}")
        print("All done!")
        # TODO: make it also to upload that parquet file
        # as I hit this bug - https://github.com/aws/aws-sdk-java/issues/2510
        #spark_df.write.mode('overwrite').parquet(f"s3a://{minio_bucket_name}/{parquet_filename}")
    except Exception as e:
        print("Exception while processing data file ", str(e))
        pass
