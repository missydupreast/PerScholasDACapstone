# ACT 401 - The Data Detective Agency (continued)

import mysql.connector
import my_secrets

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user=my_secrets.mysql_username,
    password=my_secrets.mysql_password,
    database="capstone"
)
cursor = conn.cursor()

# Execute the SQL query to retrieve all cases
cursor.execute('SELECT * FROM evidence')

# Fetch all the results
all_cases = cursor.fetchall()

# Print or process the retrieved cases
for case in all_cases:
    print(case)

# Close the database connection
conn.close()

