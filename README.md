# PerScholasDACapstone
Per Scholas Data Analytics Capstone Project <br>
by Missy Dupreast

<br>
Completed March 2024
<br>
<br>
<br>
<br>

**OVERVIEW**<br>

In partial fulfillment of the requirements for the Per Scholas Data Analytics certificate, this capstone project marks the apex of proficiency gained throughout the course and showcases the culmination of acquired knowledge and skills. This project begins with a series of primer activities for the Data Detective Capstone Project and concludes with a larger, more in-depth Data Analytics Capstone Project where I apply the skills learned in a practical setting involving a Credit Card Bank. In this scenario, I have been assigned a series of tasks including extracting credit-card system data from json files, transforming and cleaning the data, creating a MySQL database, loading the transformed data into the database, creating a front-end application for bank employees to be able to interact with and modify the data, importing the data into Power BI for analysis and building of visualizations, connecting to a REST API to extract loan application data, loading that data into the credit-card database, providing visualizations and answering questions for the hypothetical business analysis team at the Credit Card Bank. For these tasks I am utilizing Python, Jira, Apache Spark (pyspark), MySQL, and Power BI, and I am sharing my work via github. 
<br>
<br>
<br>
**PRIMER ACTIVITIES: The Data Detective**<br>

**Summary of Jira Sprints**<br>
<br>
<br>
<br>
**CORE CAPSTONE COMPONENTS** <br>

**1. Load Credit Card Database (SQL)** <br>
<br>
Credit Card System data was provided in the form of three json files. The data included transaction information, customer data, and branch data. Also provided was a mapping document, which included stakeholder requests as to how some of the data should be formatted for the database. Utilizing Python and PySpark, I extracted the data from the json files, I explored and transformed the data.<br>
<br>
Branch Data Observations <br>
<br>
During exploratory data analysis, I confirmed that there were no duplicate branches listed in the data. I also confirmed that all the phone numbers were 10 digits long, and there were no leading or trailing spaces. One issue I discovered, however, was that several branches’ zip codes were only four digits long. <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/06b6b1ab-c0c2-46ef-8c40-eae431e4dca1)  <br>
<br>
Once I confirmed that these locations were missing the leading zero, I used PySpark’s left-pad function to add the leading zero to all zip codes that were only 4 digits long. <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/c94b301a-1882-47d2-b585-64764d83d2b1) <br>
<br>
I also noticed that the street addresses do not contain street numbers, and city names that are more than one word do not have a space between words. These are minor issues, however, that are beyond the scope of the project and not a priority for our stakeholders. I am making note to revisit this at a later time. Other changes were made as needed to satisfy the requirements specified in the mapping document.   <br>
<br>
Customer Data Observations <br>
<br>
During exploratory data analysis of the customers data, I confirmed that there were no duplicate social security numbers or credit card numbers. I also confirmed that all zip codes were 5 digits in length. Phone numbers, however, were only 7 digits long. The only way to accurately enter area codes would be to confirm them with each customer, as location is not an accurate way of determining one’s area code. In order to satisfy the formatting requirement without inserting inaccurate data, I chose to use “(XXX)” as the area code to indicate that those values are missing. I used the following code to format the customers’ phone numbers: <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/35a3a7a1-210e-447e-b913-4f5c89136b4a) <br>
<br>
Similar to the Branch data, customer street addresses did not have street numbers, and city names longer than one word did not have spaces between words. I made other changes as needed to satisfy the requirements specified in the mapping document. <br>
<br>
Credit Card Data Observations <br>
<br>
During exploratory analysis of the credit card data, I confirmed that there were no duplicate transaction IDs, and I noted that branch codes and social security numbers are related to the branch and customers data, respectively. I also noticed that there were 7 distinct transaction types, which I used as user options in the front-end application program during the transaction search. <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/a9612c07-368d-48b1-bb57-afe6c7115908) <br>
<br>
The transaction data also indicated that one branch does not have any transactions listed: Branch number 192. There were 952 distinct social security numbers, which matched the total number of customers in the customers table. After exploring the data, I made changes as needed, to meet the requirements of the mapping document. <br>
<br>
Creating the Database <br>
<br>
Before loading the data, I created the database framework in order to specify the schema, including primary and foreign keys. I utilized Python and mysql connector to create the database and tables schema, and I specified default values as needed. The Python program for creating the MySQL database is here:
INSERT LINK TO DB FILE <br>
<br>
Once I confirmed the creation of the database and made sure the schema was correct, I proceeded to load the branch, customers, and credit card data by running the below programs: <br>
INSERT LINK TO Branch ETL <br>
INSERT LINK TO Customers ETL <br>
INSERT LINK TO Credit Card ETL <br>
<br>

**2. Application Front-End**<br>
<br>
INSERT LINK TO Front-end Application <br>
<br>

**3. Data Analysis and Visualizations** <br>
<br>
Now that the database has been constructed and bank employees are able to view and interact with the data, the business analyst team is seeking detailed data insights and visual representations to fulfill their information requests as listed below: <br>
<br>
*Which transaction type has the highest transaction count?* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/d94d8c1f-016e-41d3-86a2-27c0d61017eb)
<br>
During exploratory analysis, I observed the count of transaction types. To visualize this, I used a column chart and arranged the types in descending order by count. Bills had the highest transaction count, although all types were closely clustered. Please note: the visual is zoomed in, magnifying the differences between the type counts. In reality, the differences are minimal, but stakeholders requested a closer examination.<br>
<br>
<br>
*What are the top 10 states with the highest number of customers?* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/63cec576-8a76-42a4-a7a4-d53fcf7c95d2)
<br>
For this visualization, I used a bar chart and arranged the states by count of customer social security numbers in descending order. I filtered to display only the top 10. <br>
<br>
<br>
*Identify the top 10 customers with the highest total transaction amounts.* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/a8fa4923-0395-40f8-bbe9-2f95bed3c9bf) 
<br>
To identify the top 10 biggest spenders, I used a column chart with the customers’ social security numbers on the x-axis, and the sum of their transactions on the y-axis. I sorted by descending and filtered to show only the top 10. Please note: the visual is zoomed in, which magnifies the differences between the transaction amounts. <br>
<br>
<br>
**4. Functional Requirements - LOAN Application Dataset**<br>
<br>
The next task of the capstone project involved connecting to a REST API to access loan application data. I created a Python program and imported the request module to “get” the data from the following URL: https://raw.githubusercontent.com/platformps/LoanDataset/main/loan_data.json. <br>
<br>
I instructed the program to print the status code, which was 200, indicating that the request was successful. I then used response.json() to parse the response content as a json and assigned it to a variable. Next, I created a Spark Session and used PySpark to create a dataframe with the loan application data and loaded it as a new table into the creditcard_capstone database in MySQL. <br>
<br>
<br>

**5. More Data Analysis and Visualizations** <br>
<br>
Once the loan application table was complete and had been loaded into the MySQL database, I exported it as a csv file and imported it into Power BI in order to showcase the requested visualizations below: <br>
<br>
*What percentage of applications were approved for self-employed applicants?* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/3a2987d4-2851-4cb6-89af-9ff5013f5b1f)
<br>
I created new measures to calculate the total of approved and rejected self-employed applicants and added those measures to the pie chart. In our dataset, there are 70 self-employed applicants, 46 were approved for loans, and 24 were rejected. The percentage of self-employed applicants who were approved for loans is 65.71%.
<br>
<br>
<br>
*What is the percentage of rejection for married male applicants?* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/72e0f667-e1c8-43e1-b2d2-78ba5b84d127)
<br>
I created new measures to calculate the total of approved and rejected married male applicants and added those measures to the pie chart. In our dataset, there are 306 married male applicants, 219 were approved for loans, and 87 were rejected. The percentage of married male applicants who were rejected is 28.43%. <br>
<br>
<br>
*What are the top three months with the largest volume of transaction data?* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/5263e69d-5c9c-4274-8148-f2fd25041402)
<br>
For this analysis, I had to create a new column in order to extract the month name from the TIMEID column. Then I used a column chart, with month on the x-axis and count of transaction IDs on the y-axis. I filtered to show the three months with the highest counts of transactions. Please note that this visual is zoomed in, which magnifies the differences between the months. The actual difference between the months is minimal; February has the most transactions by 13 transactions. May and October have the same count of transactions. <br>
<br>
<br>
*Which branch processed the highest total dollar value of healthcare transactions?* <br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/b5a3b1a5-f756-42aa-b4a7-c212330a717c)
<br>
I added a new column to the credit card table in order to add the state name that corresponds to the branch code. I put the branch code and state abbreviation on the x-axis of this column chart, and the y-axis is the sum of transactions, filtered to show only healthcare. I also filtered to show only the top five and sorted in descending order by transaction value. <br>
<br>


**CONCLUSION**<br>

**APPENDIX**<br>
