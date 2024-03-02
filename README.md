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
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/06b6b1ab-c0c2-46ef-8c40-eae431e4dca1)  <br>
Once I confirmed that these locations were missing the leading zero, I used PySpark’s left-pad function to add the leading zero to all zip codes that were only 4 digits long. <br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/c94b301a-1882-47d2-b585-64764d83d2b1) <br>
I also noticed that the street addresses do not contain street numbers, and city names that are more than one word do not have a space between words. These are minor issues, however, that are beyond the scope of the project and not a priority for our stakeholders. I am making note to revisit this at a later time. Other changes were made as needed to satisfy the requirements specified in the mapping document.   <br>
<br>
Customer Data Observations <br>
<br>
During exploratory data analysis of the customers data, I confirmed that there were no duplicate social security numbers or credit card numbers. I also confirmed that all zip codes were 5 digits in length. Phone numbers, however, were only 7 digits long. The only way to accurately enter area codes would be to confirm them with each customer, as location is not an accurate way of determining one’s area code. In order to satisfy the formatting requirement without inserting inaccurate data, I chose to use “(XXX)” as the area code to indicate that those values are missing. I used the following code to format the customers’ phone numbers: <br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/35a3a7a1-210e-447e-b913-4f5c89136b4a) <br>
Similar to the Branch data, customer street addresses did not have street numbers, and city names longer than one word did not have spaces between words. I made other changes as needed to satisfy the requirements specified in the mapping document. <br>
<br>
Credit Card Data Observations <br>
<br>
During exploratory analysis of the credit card data, I confirmed that there were no duplicate transaction IDs, and I noticed that branch codes and social security numbers related to the branch and customers data, respectively. I also noticed that there were 7 distinct transaction types, which I used as user options in the front-end application program during the transaction search. <br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/a9612c07-368d-48b1-bb57-afe6c7115908) <br>
The transaction data also indicated that one branch does not have any transactions listed: Branch number 192. There were 952 distinct social security numbers, which matched the total number of customers in the customers table. After exploring the data, I made changes as needed, to meet the requirements of the mapping document. <br>
<br>
Creating the Database
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
During exploratory analysis, I observed the count of transaction types. To visualize this, I used a column chart and arranged the types in descending order by count. Bills had the highest transaction count, although all types were closely clustered. Please note: the visual is zoomed in, magnifying the differences between the type counts. In reality, the differences are minimal, but stakeholders requested a closer examination.<br>
<br>
![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/d94d8c1f-016e-41d3-86a2-27c0d61017eb) <br>
<br>


![image](https://github.com/missydupreast/PerScholasDACapstone/assets/98125097/5794c117-df12-4737-bb10-33dd13e09e92)
**4. Functional Requirements - LOAN Application Dataset**<br>


**5. More Data Analysis and Visualizations** <br>

**CONCLUSION**<br>

**APPENDIX**<br>
