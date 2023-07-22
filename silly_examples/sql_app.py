import streamlit as st
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

    execute_query(query)
    
    # Button to show PySpark execution plan
    if st.button("Show Execution Plan"):
        st.text(get_execution_plan(query))

if __name__ == "__main__":
    main()

