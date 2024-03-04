from my_secrets import *
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.sql.functions import *

# define the structure of the json data
schema = StructType([
    StructField("BRANCH_CODE", IntegerType(), False), # this is a primary key, so False means null values are not allowed
    StructField("BRANCH_NAME", StringType()),
    StructField("BRANCH_STREET", StringType()),
    StructField("BRANCH_CITY", StringType()),
    StructField("BRANCH_STATE", StringType()),
    StructField("BRANCH_ZIP", StringType()),
    StructField("BRANCH_PHONE", StringType()),
    StructField("LAST_UPDATED", TimestampType()),
])

spark = SparkSession.builder.appName("Branch_Extraction").getOrCreate()

branch_df = spark.read.schema(schema).json(r"C:\Users\Learner_9ZH3Z104\Desktop\PerScholasDACapstone\CreditCardDataset_jsons\cdw_sapp_branch.json") # specify to read the json according to the avove schema

# we are being asked to enter "99999" if the zip code value is null; upon checking, we have no null zip code values - I will add this as a default value when creating the databse table - here is the code for if there were null values to modify
branch_df = branch_df.fillna({'BRANCH_ZIP': '99999'})

# Several zip codes are only 4 digits long, so I need to add the missing leading 0s
branch_df = branch_df.withColumn("BRANCH_ZIP", lpad(col("BRANCH_ZIP"), 5, "0"))

# reformat the phone number using concat of substrings and indexing
# lit() is used for literal values like (, ). and -

branch_df = branch_df.withColumn('formatted_phone_number',
                                 concat(lit('('),
                                        substring('BRANCH_PHONE', 1, 3),
                                        lit(')'),
                                        substring('BRANCH_PHONE', 4, 3),
                                        lit('-'),
                                        substring('BRANCH_PHONE', 7, 4)))

# drop the old formatted phone number column
branch_df = branch_df.drop("BRANCH_PHONE")

# rename the formatted phone number column and put the columns in the correct order
branch_df = branch_df.withColumnRenamed("formatted_phone_number", "BRANCH_PHONE")
branch_df = branch_df.select(["BRANCH_CODE", "BRANCH_NAME", "BRANCH_STREET", "BRANCH_CITY", "BRANCH_STATE", "BRANCH_ZIP", "BRANCH_PHONE", "LAST_UPDATED"])

branch_df.show(branch_df.count())

# save the dataframe to the MySQL table
branch_df.write.format("jdbc") \
  .mode("append") \
  .option("url", "jdbc:mysql://localhost:3306/creditcard_capstone") \
  .option("dbtable", "CDW_SAPP_BRANCH") \
  .option("user", mysql_username) \
  .option("password", mysql_password) \
  .save()