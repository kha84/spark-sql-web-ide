from pyspark.sql import SparkSession

# Initialize PySpark
spark = SparkSession.builder \
    .appName("PySpark SQL App") \
    .getOrCreate()

# Function to execute SQL query
def execute_sql_query(query):
    try:
        result = spark.sql(query)
        return result.toPandas()
    except Exception as e:
        return str(e)

query = "select 1 as col1, 'a' as col2"
result_df = execute_sql_query(query)
print(result_df)
