import requests
import json
from my_secrets import *
import pyspark
from pyspark.sql import SparkSession

# Make a GET request to the /books endpoint.
response = requests.get("https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json")

# Check the status code.
if response.status_code == 200:
   print(f"Successful! Status code = {response.status_code}.")
   loan_app_data = response.json()
else:
   # The request failed.
   print(response.status_code)



# create a spark session
spark = SparkSession.builder.appName("loan_app_API").getOrCreate()

# Convert loan_app_data into a DataFrame
# loan_data_df = spark.createDataFrame(data = loan_app_data, schema = columns)
loan_data_df = spark.createDataFrame(loan_app_data)

# Display the DataFrame schema
# loan_data_df.printSchema()

# Show the first few rows of the DataFrame
# loan_data_df.show()

# save the dataframe to the MySQL table
loan_data_df.write.format("jdbc") \
  .mode("append") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "creditcard_capstone.CDW_SAPP_loan_application") \
  .option("user", mysql_username) \
  .option("password", mysql_password) \
  .save()
