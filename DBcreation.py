import mysql.connector
import my_secrets

cursor = None
connection = None

try:
    # Establish a connection to the MySQL server
    connection = mysql.connector.connect(
        host="localhost",          
        user=my_secrets.mysql_username,
        password=my_secrets.mysql_password,
    )

    # check to see if we are connected:
    if connection.is_connected():
        print("Connected to MySQL database!")
    else:
        print("Failed to connect to MySQL database.")

    # create cursor object
    cursor = connection.cursor() 

    cursor.execute("DROP DATABASE IF EXISTS creditcard_capstone;")

    cursor.execute("CREATE DATABASE IF NOT EXISTS creditcard_capstone;")
    cursor.execute("USE creditcard_capstone;")

    # create BRANCH table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CDW_SAPP_BRANCH (
            `BRANCH_CODE` int NOT NULL, 
            `BRANCH_NAME` varchar(50),   
            `BRANCH_STREET` varchar(50),
            `BRANCH_CITY` varchar(50),
            `BRANCH_STATE` varchar(10), 
            `BRANCH_ZIP` varchar(10) DEFAULT '99999', 
            `BRANCH_PHONE`  varchar(25),
            `LAST_UPDATED` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            PRIMARY KEY (`BRANCH_CODE`)
        );   
    """)

    # create CUSTOMER table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CDW_SAPP_CUSTOMER (
            `SSN` int NOT NULL,
            `FIRST_NAME` varchar(50),
            `MIDDLE_NAME` varchar(50),
            `LAST_NAME` varchar(50),
            `Credit_card_no` varchar(50),
            `FULL_STREET_ADDRESS` varchar(50),
            `CUST_CITY` varchar(50),
            `CUST_STATE` varchar(50),
            `CUST_COUNTRY` varchar(50),
            `CUST_ZIP` varchar(50),
            `CUST_PHONE` varchar(50),
            `CUST_EMAIL` varchar(50),
            `LAST_UPDATED` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
            PRIMARY KEY (`SSN`)
        );   
    """)

    # create CREDIT CARD table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CDW_SAPP_CREDIT_CARD (
            `TRANSACTION_ID` int NOT NULL,
            `CUST_CC_NO` varchar(50),
            `TIMEID` varchar(10),
            `CUST_SSN` int,
            `BRANCH_CODE` int,
            `TRANSACTION_TYPE` varchar(50),
            `TRANSACTION_VALUE` float,
            PRIMARY KEY (`TRANSACTION_ID`),
            CONSTRAINT `br_code_fk` FOREIGN KEY (`BRANCH_CODE`) REFERENCES `CDW_SAPP_BRANCH` (`BRANCH_CODE`),
            CONSTRAINT `ssn_fk` FOREIGN KEY (`CUST_SSN`) REFERENCES `CDW_SAPP_CUSTOMER` (`SSN`)
        );   
    """)

    # commit changes
    connection.commit()

    #print confirmation
    print("Databse creation complete!")

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    # Close the cursor if it's not None
    if cursor is not None:
        cursor.close()

    # Close the connection if it's not None
    if connection is not None:
        connection.close()