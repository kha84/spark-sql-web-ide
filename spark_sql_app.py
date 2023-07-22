import streamlit as st
import boto3
from pyspark.sql import SparkSession

# Configure S3 MinIO access
minio_access_key = "g3sB5A0PkrpDJ1iuzxhw"
minio_secret_key = "FcodVGJaEhZdX88zyB9safLSdIMc1vNcCUwyAqSM"
minio_bucket_name = "test"
minio_endpoint = "http://localhost:9000"  # Replace with your MinIO server endpoint


# Initialize PySpark
spark = SparkSession.builder.appName("MinioTest") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint) \
        .config("spark.hadoop.fs.s3a.access.key", minio_access_key) \
        .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key ) \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()

# Function to execute SQL query
def execute_sql_query(query):
    try:
        result = spark.sql(query)
        return result.toPandas()
    except Exception as e:
        return str(e)

# Function to get the execution plan for the query
def get_execution_plan(query):
    try:
        df = spark.sql(query)
        return df._jdf.queryExecution().toString()
    except Exception as e:
        st.error(f"Error executing the query: {e}")

def main():
    st.title("PySpark SQL Query Runner")
    
    # Initialize query variable
    query = st.text_area("Enter your SQL query:")
    
    # Execute the query and display the result
    def execute_query(query):
        if query.strip():
            try:
                result_df = execute_sql_query(query)
                st.dataframe(result_df)
            except Exception as e:
                st.error(f"Error executing the query: {e}")

    #execute_query(query)
    
    # Show Parquet files in S3 MinIO bucket in the sidebar
    st.sidebar.title("Parquet Files in S3 MinIO Bucket")
    
    # Initialize S3 MinIO client
    s3_client = boto3.client("s3",
                             aws_access_key_id=minio_access_key,
                             aws_secret_access_key=minio_secret_key,
                             endpoint_url=minio_endpoint,
                             region_name="us-east-1"  # Replace with your desired region
                             )

    # List objects in the MinIO bucket with .parquet extension
    response = s3_client.list_objects_v2(Bucket=minio_bucket_name)
    parquet_files = [file["Key"] for file in response["Contents"] if file["Key"].endswith(".parquet")]
    
    # Display the list of Parquet files and input fields for aliases
    selected_files = st.sidebar.multiselect("Select Parquet Files", parquet_files)
    
    # Input fields for aliases
    aliases = {}
    for file in selected_files:
        alias = st.sidebar.text_input(f"Alias for {file}", file.split("/")[-1].split(".")[0])
        aliases[file] = alias
    
    # TODO: delete all spark views before creating new ones
    
    # Button to show PySpark execution plan
    if st.button("Show Execution Plan"):
        st.text(get_execution_plan(query))
    
    # Execute the selected files with aliases
    if st.button("Run SQL with Selected Files"):
        try:
            for file, alias in aliases.items():
                spark.read.parquet(f"s3a://{minio_bucket_name}/{file}").createOrReplaceTempView(alias)
            
            result_df = execute_sql_query(query)
            st.dataframe(result_df)
        except Exception as e:
            st.error(f"Error executing the query with selected files: {e}")

if __name__ == "__main__":
    main()

