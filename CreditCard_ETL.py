from my_secrets import *
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.functions import *

# define the structure of the json data - I am defining the schema to make sure the data will be the type that I want it to be
schema = StructType([
    StructField("TRANSACTION_ID", IntegerType(), False), # this is a primary key, so False means null values are not allowed
    StructField("YEAR", StringType()),
    StructField("MONTH", StringType()),
    StructField("DAY", StringType()),
    StructField("CREDIT_CARD_NO", StringType()),
    StructField("CUST_SSN", IntegerType()),
    StructField("BRANCH_CODE", IntegerType()),
    StructField("TRANSACTION_TYPE", StringType()),
    StructField("TRANSACTION_VALUE", DoubleType()),   
])

spark = SparkSession.builder.appName("CCD_Extraction").getOrCreate()

ccd_df = spark.read.schema(schema).json(r"C:\Users\Learner_9ZH3Z104\Desktop\PerScholasDACapstone\CreditCardDataset_jsons\cdw_sapp_credit.json") # specify to read the json according to the above schema

# Add leading '0' if length of 'day' is 1 - do the same for 'month'
# lpad means left pad; takes 3 arguments: column to be padded, the target length, and the character used for the padding
ccd_df = ccd_df.withColumn("DAY", lpad(col("DAY"), 2, "0"))
ccd_df = ccd_df.withColumn("MONTH", lpad(col("MONTH"), 2, "0"))

# concatenate the year, month, amd day columns - (creates the new TIMEID column at the end)
ccd_df = ccd_df.withColumn("TIMEID", concat(col("YEAR"), col("MONTH"), col("DAY")))

# drop the year, month, day columns
ccd_df = ccd_df.drop('YEAR', 'MONTH', 'DAY')

# I need to rename the customer credit card column
ccd_df = ccd_df.withColumnRenamed("CREDIT_CARD_NO", "CUST_CC_NO")

# put the columns in the proper order
ccd_df = ccd_df.select(["TRANSACTION_ID", "CUST_CC_NO", "TIMEID", "CUST_SSN", "BRANCH_CODE", "TRANSACTION_TYPE", "TRANSACTION_VALUE"])

ccd_df.show(1000,0) # show first 1000 rows

# save the dataframe to the MySQL table
ccd_df.write.format("jdbc") \
  .mode("append") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "CDW_SAPP_CREDIT_CARD") \
  .option("user", mysql_username) \
  .option("password", mysql_password) \
  .save()