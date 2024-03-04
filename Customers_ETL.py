from my_secrets import *
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.functions import *

# define the structure of the json data
schema = StructType([
    StructField("SSN", IntegerType()),
    StructField("FIRST_NAME", StringType()),
    StructField("MIDDLE_NAME", StringType()),
    StructField("LAST_NAME", StringType()),
    StructField("CREDIT_CARD_NO", StringType()),
    StructField("STREET_NAME", StringType()),
    StructField("APT_NO", StringType()),
    StructField("CUST_CITY", StringType()),
    StructField("CUST_STATE", StringType()),
    StructField("CUST_COUNTRY", StringType()),
    StructField("CUST_ZIP", StringType()),
    StructField("CUST_PHONE", StringType()),
    StructField("CUST_EMAIL", StringType()),
    StructField("LAST_UPDATED", TimestampType()),
])

spark = SparkSession.builder.appName("Customer_Extraction").getOrCreate()

customer_df = spark.read.schema(schema).json(r"C:\Users\Learner_9ZH3Z104\Desktop\PerScholasDACapstone\CreditCardDataset_jsons\cdw_sapp_custmer.json")

# make first and last name columns title case
customer_df = customer_df.withColumn("FIRST_NAME", initcap(col("FIRST_NAME")))
customer_df = customer_df.withColumn("LAST_NAME", initcap(col("LAST_NAME")))

# convert the middle name column to lowercase
customer_df = customer_df.withColumn("MIDDLE_NAME", lower(col('MIDDLE_NAME')))

# reformat the phone number; since area codes are missing, I am using (XXX) in place of area codes to signify that they are unknown/missing 
# actual area codes will need to be verified with each customer
customer_df = customer_df.withColumn('formatted_phone_number',
                                     concat(lit('(XXX)'),
                                            substring('CUST_PHONE', 1, 3),
                                            lit('-'),
                                            substring('CUST_PHONE', 4, 4)))

# drop the customer phone column and rename formatted phone number
customer_df = customer_df.drop("CUST_PHONE")
customer_df = customer_df.withColumnRenamed("formatted_phone_number", "CUST_PHONE")

# concat street name and Apt number if Apt number is not null
customer_df = customer_df.withColumn('FULL_STREET_ADDRESS',
                                     when(col("APT_NO").isNotNull(),
                                          concat(col("STREET_NAME"), lit(", Apt "), col("APT_NO")))
                                     .otherwise(col("STREET_NAME")))

# drop old address and apt columns
customer_df = customer_df.drop("STREET_NAME", "APT_NO")

# put all the columns in the proper order
customer_df = customer_df.select("SSN", "FIRST_NAME", "MIDDLE_NAME", "LAST_NAME", "CREDIT_CARD_NO", "FULL_STREET_ADDRESS", "CUST_CITY", "CUST_STATE", "CUST_COUNTRY","CUST_ZIP", "CUST_PHONE", "CUST_EMAIL", "LAST_UPDATED")

customer_df.show(customer_df.count()) # this will show all results, not just the first 20

# save the dataframe to the MySQL table
customer_df.write.format("jdbc") \
  .mode("append") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "CDW_SAPP_CUSTOMER") \
  .option("user", mysql_username) \
  .option("password", mysql_password) \
  .save()