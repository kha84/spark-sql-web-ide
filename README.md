# Silly, simple Web SQL IDE for Spark

A very simple streamlit web UI which allows you to run Spark SQL against parquet files stored in MinIO S3 bucket.
You can define your own aliases for the files you need. 

If you need something more useful, consider to look at HUE (https://github.com/cloudera/hue).


# Quick setup guide 


1. Install all the needed requirements

```
pip install pyspark streamlit boto3
```

2. Download jars we need for MinIO and place them together to all pyspark jars. Have a look on this URL to see more details:
https://abdullahdurrani.com/posts/how-to-use-minio-with-spark/

```
SPARK_JARS_DIR=`find / -type d -iname "jars" | grep "dist-packages/pyspark/jars"`
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar
mv hadoop-aws-3.2.0.jar $SPARK_JARS_DIR
wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.511/aws-java-sdk-bundle-1.12.511.jar
mv aws-java-sdk-bundle-1.12.511.jar $SPARK_JARS_DIR
```

3. Download, run and configure MinIO S3 server.

This repo already comes with minio binary, "test" bucket created and API key preconfigured, so you can skip this step. 

```
wget https://dl.minio.io/server/minio/release/linux-amd64/minio
chmod 755 minio
mkdir data
./minio server ./data 
```

Open MinIO web console (minioadmin/minioadmin) and:
* create bucket
* put some parquet files in there
* create API key for our application

Update all the details to spark_sql_app_config.py


4. Run the app 

```
streamlit run spark_sql_app.py 
```

# Screenshots

![](https://github.com/kha84/spark-sql-web-ide/blob/main/screenshot1.png?raw=true)

![](https://github.com/kha84/spark-sql-web-ide/blob/main/screenshot2.png?raw=true)

![](https://github.com/kha84/spark-sql-web-ide/blob/main/screenshot3.png?raw=true)

# More detailed guide

I used to run this in docker, just for the sake of not littering my machine with all the extra libs
```
docker run -it --name test --expose 1000 --expose 1001 ubuntu
```

Install required packages
```
apt update
apt install -y git python3-pip wget default-jdk iproute2 nmap
pip install pyspark streamlit boto3
```

Clone project code
```
git clone https://github.com/kha84/spark-sql-web-ide.git
cd spark-sql-web-ide/
```

With using a simple example provided in repo, make sure pySpark (barebones) is operating  
```
python3 silly_examples/sql.py
```
You should see a simple table as a result of running this script:  
```
    col1 col2  
 0     1    a
```


Make sure a simple standalone streamlit app is operating.
Streamlit will give you "Network URL" like this: http://172.17.0.2:1001
Open it with your web browser and make sure the test app works fine.
```
streamlit run silly_examples/test_app.py --server.port 1001
```

We are getting closer. Run the next simple test to make sure you can run Streamlit app which sets up local Spark.
Spark doesn't have any connectivity yet, so once you open this test app, use only simple SQLs like 
`select 1 as col union all select 2` and then press CTRL+Enter to make sure you see results returned.
```
streamlit run silly_examples/sql_app.py  --server.port 1001
```

Startup MinIO S3 server to listen all the interfaces on ports:
*  9000 - it is used for S3 protocol it's default for MinIO so we don't change it
*  1000 - for Web UI

```
./minio server ./data --console-address 0.0.0.0:1000 &
```

Using the IP address from streamlit "Network URL" we seen before, open it with your WebBrowser while changing port to 1000 - to make sure you can access Minio Web UI.
Username and password is "minioadmin"
```
http://172.17.0.2:1000
```

Before we move on and run our app, there're two important JARs we need to sideload to pySpark other jars.
For that we first need to figure it out, where these jars are.
```
SPARK_JARS_DIR=`find / -type d -iname "jars" | grep "dist-packages/pyspark/jars"`
```

Now download two jars and put them in place:
```
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.2.0/hadoop-aws-3.2.0.jar
mv hadoop-aws-3.2.0.jar $SPARK_JARS_DIR
wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.511/aws-java-sdk-bundle-1.12.511.jar
mv aws-java-sdk-bundle-1.12.511.jar $SPARK_JARS_DIR
```

And finally, let's run the app itself:
```
streamlit run spark_sql_app.py --server.port 1001
```

If you ever shutdown this test container and want to start it up, terminal back to it and run everything again, use these commands:
```
docker start test
docker exec --user root -it test bash
cd spark-sql-web-ide/
./minio server ./data --console-address 0.0.0.0:1000 &
streamlit run spark_sql_app.py --server.port 1001
```
