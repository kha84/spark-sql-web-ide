# Silly, simple Web SQL IDE for Spark

A very simple streamlit web UI which allows you to run Spark SQL against parquet files stored in MinIO S3 bucket.
You can define your own aliases for the files you need. 

If you need something more useful, consider to look at HUE (https://github.com/cloudera/hue).


# Installation


1. Install all the needed requirements

```
pip install pyspark streamlit boto3
```

2. Download jars we need for MinIO and place them together to all pyspark jars. Have a look on this URL to see more details:
https://abdullahdurrani.com/posts/how-to-use-minio-with-spark/

```
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar
mv hadoop-aws-3.2.0.jar ~/.local/lib/python3.10/site-packages/pyspark/jars/
wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.511/aws-java-sdk-bundle-1.12.511.jar
mv aws-java-sdk-bundle-1.12.511.jar ~/.local/lib/python3.10/site-packages/pyspark/jars/
```

3. Download, run and configure minio. 

```
wget https://dl.minio.io/server/minio/release/linux-amd64/minio
chmod 755 minio
mkdir data
./minio server ./data 
```

Open MinIO web console and create bucket. Also create API key and update all the details to spark_sql_app.py

4. Run the app 

```
streamlit run spark_sql_app.py 
```

# Screenshots

![](https://github.com/kha84/spark-sql-web-ide/blob/main/screenshot1.png?raw=true)

![](https://github.com/kha84/spark-sql-web-ide/blob/main/screenshot2.png?raw=true)

![](https://github.com/kha84/spark-sql-web-ide/blob/main/screenshot3.png?raw=true)
