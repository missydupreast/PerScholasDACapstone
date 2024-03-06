import mysql.connector
from display_mainmenu import *
from tabulate import tabulate

print("Welcome to the Imagine I.M.A. Credit Card Bank!")
print("To continue, please log in.")

cursor = None
connection = None

username = input("Username: ")
password = input("Password: ") # each bank employee should have their own username and password to access the database. This db contains sensitive information.

try:
    connection = mysql.connector.connect(
        host="localhost",          
        user= username,
        password= password,
        database="creditcard_capstone"
    )
    if connection.is_connected():
        print(f"Welcome, {username}! You are connected to the database!")
    else:
        print("Failed to connect.")

except mysql.connector.Error as err:
    print("Login failed. Error:", err)
    exit(1)  # Exit with a non-zero exit status to indicate failure

# create cursor object
cursor = connection.cursor()

##############################################################################################
def logout_exit():
    global cursor
    # Close the cursor if it's not None
    if cursor is not None:
        cursor.close()
    # Close the connection if it's not None
    if connection is not None:
        connection.close()
    print("Goodbye")
    exit()
##############################################################################################
def validate_zip():
    user_zip = input("Please enter the 5-digit zip code of the transactions you are searching for: \n(Type 0 to go back to the main menu) ") 
    
    if user_zip =="0":
        return
    
    if not user_zip.isdigit():
        print("Not a valid zip code. Please try again.")                
        return validate_zip()
        
    if user_zip.isdigit() and len(user_zip) == 5:
        # check to see if zip code is in the customers table
        cursor.execute("SELECT CUST_ZIP FROM CDW_SAPP_CUSTOMER WHERE CUST_ZIP = %s", (user_zip,))
        result = cursor.fetchall()

        if result:
            print("Thank you for entering the zip code.")
            return user_zip
        else:
            print("Zip code not found.")                       
            return validate_zip()
    else:
        print("Not a valid zip code. Please try again.")                
        return validate_zip()


def validate_month_year():
    user_date = input("Please enter the transactions' year and month (YYYYMM) \n(Type 0 to go back to the main menu): ") #TIMEID format without the day

    if user_date =="0":
        return

    if not user_date.isdigit() and not 1 <= int(user_date[-2:]) <= 12:
        print("Not a valid date input. Please try again.")        
        return validate_month_year()
    
    if user_date.isdigit() and len(user_date) == 6 and 1 <= int(user_date[-2:]) <= 12: # Check if the month is within the valid range (01 to 12)
        # check to see if the date exists in the credit card table
        userdate_wildcard = user_date + "%" 
        cursor.execute("SELECT TIMEID FROM CDW_SAPP_CREDIT_CARD WHERE TIMEID LIKE %s", (userdate_wildcard,))
        result = cursor.fetchall()

        if result:
            print("Thank you for entering the date.")
            print("")
            return user_date
        else:
            print("Date not found.")                        
            return validate_month_year()
        
    else:
        print("Not a valid date. Please make sure you are using YYYYMM format.")       
        
        return validate_month_year()


# 1) Create a function that accomplishes the following tasks:
# 2.1.1 - Prompt the user for a zip code, provide contextual cues for valid input, and verify it is in the correct format.
# 2.1.2- Ask for a month and year,  and provide contextual cues for valid input and verify it is in the correct format.
# 2.1.3- Use the provided inputs to query the database and retrieve a list of transactions made by customers in the specified zip code for the given month and year.
# 2.1.4 - Sort the transactions by day in descending order.

def zip_date_transactions():
    user_zip = validate_zip()

    if user_zip is None:
        return
    
    user_date = validate_month_year()
    
    if user_date is None:
        return
  
    userdate_wildcard = user_date + "%"
            
    zip_date_query = """SELECT ccd.*, c.CUST_ZIP FROM CDW_SAPP_CREDIT_CARD ccd 
                        JOIN CDW_SAPP_CUSTOMER c ON ccd.CUST_CC_NO = c.Credit_card_no
                        WHERE c.CUST_ZIP = %s AND TIMEID LIKE %s
                    """ 
    cursor.execute(zip_date_query, (user_zip, userdate_wildcard))
    results = cursor.fetchall()
            
    if not results:
        print("No results found.")
        user_input = input("To return to the main menu, enter 0; enter any key to search for another zip code and date. \n")
        if user_input != "0":
            zip_date_transactions()
            return
    else:
        # Process the results
        header_row = [i[0] for i in cursor.description]
        print(tabulate(results, headers=header_row))

        user_input = input("To return to the main menu, enter 0; enter any key to search for another zip code and date. \n")
        if user_input != "0":
            zip_date_transactions()

#################################################################################################

# 2) Used to display the number and total values of transactions for a given type.
def trans_by_type():
    trans_type = input("What type of transaction are you searching for? \n    1 - Bills \n    2 - Education \n    3 - Entertainment \n    4 - Gas \n    5 - Grocery \n    6 - Healthcare \n    7 - Test \n    0 - Return to the Main Menu \n    Enter the number that corresponds to your choice: ")

    if trans_type == "0":
        display_mainmenu()
        return
    elif trans_type == "1":
        trans_type = "Bills"
    elif trans_type == "2":
        trans_type = "Education" 
    elif trans_type == "3":
        trans_type = "Entertainment"
    elif trans_type == "4":
        trans_type = "Gas"
    elif trans_type == "5":
        trans_type = "Grocery"
    elif trans_type == "6":
        trans_type = "Healthcare"
    elif trans_type == "7":
        trans_type = "Test"
    else:
        print("Not a valid choice. Please try again.")
        print("")
        trans_by_type()


    # search for the type in the credit card table
    cursor.execute("SELECT TRANSACTION_TYPE FROM CDW_SAPP_CREDIT_CARD WHERE TRANSACTION_TYPE = %s", (trans_type,))
    result = cursor.fetchall()

    if result:
        type_total_query = ("""SELECT TRANSACTION_TYPE, COUNT(TRANSACTION_ID) AS COUNT, ROUND(SUM(TRANSACTION_VALUE),2) as TOTAL 
                            FROM CDW_SAPP_CREDIT_CARD 
                            WHERE TRANSACTION_TYPE = %s
                            GROUP BY TRANSACTION_TYPE""")
        cursor.execute(type_total_query, (trans_type,))
        type_totals = cursor.fetchall()
        
        header_row = [i[0] for i in cursor.description]
        print(tabulate(type_totals, headers=header_row))
        print("")
    else:
        print("Type not found")
            
    user_input = input("To return to the main menu, enter 0; enter any key to search for another type. ")
    if user_input != "0":
        trans_by_type()
        

#################################################################################################

# 3) Used to display the total number and total values of transactions for branches in a given state.

def trans_by_branchstate():

    br_state = input("Which state would you like to view branch transactions for? (use state abbreviation) \n(Type 0 to go back to the main menu) \n")
    if br_state == "0":
        return

    if not len(br_state) == 2 or not br_state.isalpha():
        print("Not a valid state abbreviation. Please try again.")
        trans_by_branchstate()
        return

    else:
        # search for the state in the branch table
        cursor.execute("SELECT BRANCH_STATE FROM CDW_SAPP_BRANCH WHERE BRANCH_STATE = %s", (br_state,))
        result = cursor.fetchall()
        
        if result:
            branchstate_query = """SELECT b.BRANCH_STATE, COUNT(ccd.TRANSACTION_ID) AS COUNT, ROUND(SUM(ccd.TRANSACTION_VALUE),2) AS TOTAL
                                FROM CDW_SAPP_BRANCH b JOIN CDW_SAPP_CREDIT_CARD ccd ON b.BRANCH_CODE = ccd.BRANCH_CODE
                                WHERE BRANCH_STATE = %s
                                GROUP BY b.BRANCH_STATE
                                """
            cursor.execute(branchstate_query, (br_state,))
            br_state_totals = cursor.fetchall() 
            
            header_row = [i[0] for i in cursor.description]
            print(tabulate(br_state_totals, headers=header_row, floatfmt=".2f"))
            print("")
        else:
            print("Branch state not found. Please try again.")
            print("")
            trans_by_branchstate()
            return

    user_input = input("To return to the main menu, enter 0; enter any key to search for another branch state. \n")
    if user_input != "0":
        trans_by_branchstate()

#################################################################################################

# this function chooses a customer SSN and returns it        
def choose_customerSSN():
    cust_SSN = input("Enter the SSN for the customer you would like to search: \n(Type 0 to go back to the main menu) \n")
    if cust_SSN == "0":
        return
    else:
        clean_cust_SSN = ''.join(num for num in cust_SSN if num.isdigit()) # this will remove any punctuation or spaces if the user inputs them
        if len(clean_cust_SSN) == 9:
            cursor.execute("SELECT SSN FROM CDW_SAPP_CUSTOMER WHERE SSN = %s", (clean_cust_SSN,))
            result = cursor.fetchall()
            if result:
                return clean_cust_SSN
            else:
                print("SSN not found.")
                print("")                
                return choose_customerSSN()
        else:
            print("Not a valid SSN. Please try again")
            print("")            
            return choose_customerSSN()

# 2.2 Customer Details Module
# 1) Used to check the existing account details of a customer.

def cust_acct_deets():
    cust_SSN = choose_customerSSN() # this function will validate the SSN and make sure it exists in the customers table
    
    if cust_SSN is not None:
        cust_acct_query = "SELECT * FROM CDW_SAPP_CUSTOMER WHERE SSN = %s"
        cursor.execute(cust_acct_query, (cust_SSN,))
        cust_acct_results = cursor.fetchall()
    
        header_row = [i[0] for i in cursor.description]
        print(tabulate(cust_acct_results, headers=header_row))
        print("") 
        user_input = input("To return to the main menu, enter 0; enter any key to search for another customer's details. \n")
        if user_input != "0":
            cust_acct_deets()

#################################################################################################
def update_timestamp(cust):
    new_timestamp = """UPDATE CDW_SAPP_CUSTOMER
                        SET LAST_UPDATED = NOW()
                        WHERE SSN = %s
                        """
    cursor.execute(new_timestamp, (cust, ))
    connection.commit()
    return
#######################################################
def mod_cust_first_name(cust):
    new_firstname = input("What would you like to change the first name to? \n(Type 0 to go back to the previous menu) \n")
    if new_firstname == "0":
        return
    else:
        mod_firstname = """UPDATE CDW_SAPP_CUSTOMER
                        SET FIRST_NAME = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_firstname, (new_firstname, cust))
        connection.commit()
        update_timestamp(cust)
        print("First name updated successfully!")

########################################################
def mod_cust_mid_name(cust):
    new_midname = input("What would you like to change the middle name to? \n(Type 0 to go back to the previous menu) \n")
    if new_midname == "0":
        return
    else:
        mod_firstname = """UPDATE CDW_SAPP_CUSTOMER
                        SET MIDDLE_NAME = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_firstname, (new_midname, cust))
        connection.commit()
        update_timestamp(cust)
        print("Middle name updated successfully!")

########################################################
def mod_cust_last_name(cust):
    new_lastname = input("What would you like to change the last name to? \n(Type 0 to go back to the previous menu) \n")
    if new_lastname == "0":
        return
    else:
        mod_lastname = """UPDATE CDW_SAPP_CUSTOMER
                        SET LAST_NAME = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_lastname, (new_lastname, cust))
        connection.commit()
        update_timestamp(cust)
        print("Last name updated successfully!")

########################################################
def mod_cust_ccd(cust):
    new_ccd = input("What would you like to change the credit card number to? \n(Type 0 to go back to the previous menu) \n")
    if new_ccd == "0":
        return
    else:       
        clean_new_ccd = ''.join(num for num in new_ccd if num.isdigit()) # this will remove any punctuation or spaces if the user inputs them, and it will not join letters
        if len(clean_new_ccd) == 16:
        
            mod_ccd = """UPDATE CDW_SAPP_CUSTOMER
                            SET Credit_card_no = %s
                            WHERE SSN = %s
                            """
            cursor.execute(mod_ccd, (clean_new_ccd, cust))
            connection.commit()
            update_timestamp(cust)
            print("Credit card number updated successfully!")
            return
        else:
            print("Not a valid credit card number. Please try again.")
            return mod_cust_ccd(cust)
########################################################
def mod_cust_ssn(cust):
    new_ssn = input("What would you like to change the SSN to? \n(Type 0 to go back to the previous menu) \n")
    if new_ssn == "0":
        return
    else:       
        clean_new_SSN = ''.join(num for num in new_ssn if num.isdigit()) # this will remove any punctuation or spaces if the user inputs them, and it will not join letters
        if len(clean_new_SSN) == 9:
            mod_ssn = """UPDATE CDW_SAPP_CUSTOMER
                            SET SSN = %s
                            WHERE SSN = %s
                            """
            try:
                cursor.execute(mod_ssn, (clean_new_SSN, cust))
                connection.commit()
                update_timestamp(cust)
                print("SSN updated successfully!")
            except Exception as e:
                print("Sorry, cannot edit a parent row. A foreign key constraint fails. ")
            return
        else:
            print("Not a valid SSN. Please try again.")
            return mod_cust_ssn(cust)
########################################################
def mod_cust_street(cust):
    new_street = input("What would you like to change the street address to? \n(Type 0 to go back to the previous menu) \n")
    if new_street == "0":
        return
    else:
        mod_street = """UPDATE CDW_SAPP_CUSTOMER
                        SET FULL_STREET_ADDRESS = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_street, (new_street, cust))
        connection.commit()
        update_timestamp(cust)
        print("Street address updated successfully!")

########################################################    
def mod_cust_city(cust):
    new_city = input("What would you like to change the city to? \n(Type 0 to go back to the previous menu) \n")
    if new_city == "0":
        return
    else:
        mod_city = """UPDATE CDW_SAPP_CUSTOMER
                        SET CUST_CITY = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_city, (new_city, cust))
        connection.commit()
        update_timestamp(cust)
        print("City updated successfully!")

######################################################## 
def mod_cust_state(cust):
    new_state = input("What would you like to change the state to? \n(Type 0 to go back to the previous menu) \n").upper()
    if new_state == "0":
        return
    
    if not len(new_state) == 2 or not new_state.isalpha():
        print("Not a valid state abbreviation. Please try again.")
        mod_cust_state(cust)
        return 
    
    else:
        mod_state = """UPDATE CDW_SAPP_CUSTOMER
                        SET CUST_STATE = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_state, (new_state, cust))
        connection.commit()
        update_timestamp(cust)
        print("State updated successfully!")

######################################################## 
def mod_cust_cntry(cust):
    new_cntry = input("What would you like to change the country to? \n(Type 0 to go back to the previous menu) \n")
    if new_cntry == "0":
        return
    else:
        mod_cntry = """UPDATE CDW_SAPP_CUSTOMER
                        SET CUST_COUNTRY = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_cntry, (new_cntry, cust))
        connection.commit()
        update_timestamp(cust)
        print("Country updated successfully!")

######################################################## 
def mod_cust_zip(cust):
    new_zip = input("What would you like to change the zip code to? \n(Type 0 to go back to the previous menu) \n")
    
    if new_zip == "0":
        return
    
    if not new_zip.isdigit() or not len(new_zip) == 5:
        print("Not a valid zip code. Please try again.")
        return mod_cust_zip(cust)

    else:
        mod_zip = """UPDATE CDW_SAPP_CUSTOMER
                        SET CUST_ZIP = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_zip, (new_zip, cust))
        connection.commit()
        update_timestamp(cust)
        print("Zip code updated successfully!")

########################################################
def mod_cust_phone(cust):
    new_phone = input("What would you like to change the phone number to? \n(Type 0 to go back to the previous menu) \n")
    if new_phone == "0":
        return
    else:               
        # this will remove any punctuation or spaces if the user inputs them, and it will not join letters
        clean_new_phone = ''.join(num for num in new_phone if num.isdigit()) 
        if len(clean_new_phone) == 10:
            area_code = clean_new_phone[:3]
            first_three = clean_new_phone[3:6]
            last_four = clean_new_phone[6:]
            new_phone = (f"({area_code}){first_three}-{last_four}")

            mod_phone = """UPDATE CDW_SAPP_CUSTOMER
                            SET CUST_PHONE = %s
                            WHERE SSN = %s
                            """
            cursor.execute(mod_phone, (new_phone, cust))
            connection.commit()
            update_timestamp(cust)
            print("Phone number updated successfully!")
            return 
        else:
            print("Not a valid phone number. Please try again.")
            return mod_cust_phone(cust)

########################################################
def mod_cust_email(cust):
    new_email = input("What would you like to change the email to? \n(Type 0 to go back to the previous menu) \n")
    if new_email == "0":
        return
    
    if "@" not in new_email or not new_email.endswith('.com'):
        print("Not a valid email address. Please try again.")
        return mod_cust_email(cust)
    
    else:      
        mod_email = """UPDATE CDW_SAPP_CUSTOMER
                        SET CUST_EMAIL = %s
                        WHERE SSN = %s
                        """
        cursor.execute(mod_email, (new_email, cust))
        connection.commit()
        update_timestamp(cust)
        print("Email updated successfully!")

########################################################

# 2) Used to modify the existing account details of a customer.
def modify_cust_acct():
    
    cust = choose_customerSSN()
    
    #show acct details for customer
    if cust is not None:
        cust_acct_query = "SELECT * FROM CDW_SAPP_CUSTOMER WHERE SSN = %s"
        cursor.execute(cust_acct_query, (cust,))
        cust_acct_results = cursor.fetchall()
    
        header_row = [i[0] for i in cursor.description]
        print(tabulate(cust_acct_results, headers=header_row))
        print("")
    
    while True:
        print("Which customer field would you like to modify?") # the last_updated column is updated to current timestamp each time a change is made
        print("    1 - Customer First Name")
        print("    2 - Customer Middle Name")
        print("    3 - Customer Last Name")
        print("    4 - Customer Credit Card Number")
        print("    5 - Customer SSN")
        print("    6 - Customer Street Address")
        print("    7 - Customer City")
        print("    8 - Customer State")
        print("    9 - Customer Country")
        print("    10 - Customer Zip Code")
        print("    11 - Customer Phone Number")
        print("    12 - Customer Email")
        print("    0 - Return to Main Menu")

        field = input("Enter the number that corresponds to your choice: ") 

        if field == "1":
            mod_cust_first_name(cust)
        elif field == "2":
            mod_cust_mid_name(cust)
        elif field == "3":
            mod_cust_last_name(cust)
        elif field == "4":
            mod_cust_ccd(cust)
        elif field == "5":
            mod_cust_ssn(cust)
        elif field == "6":
            mod_cust_street(cust)
        elif field == "7":
            mod_cust_city(cust)
        elif field == "8":
            mod_cust_state(cust)
        elif field == "9":
            mod_cust_cntry(cust)    
        elif field == "10":
            mod_cust_zip(cust)
        elif field == "11":
            mod_cust_phone(cust)
        elif field == "12":
            mod_cust_email(cust)
        elif field == "0":
            return
        else:
            print("Invalid choice. Please try again.")
#################################################################################################
# 3) Used to generate a monthly bill for a credit card number for a given month and year. 
# Hint: What does YOUR monthly credit card bill look like?  What structural components does it have?  Not just a total $ for the month, right?

def validate_ccd():
    ccd_no = input("Enter the 16-digit credit card number: \n(Type 0 to go back to the main menu) \n")
    
    clean_ccd = ''.join(num for num in ccd_no if num.isdigit()) # this will remove any punctuation or spaces if the user inputs them, and it will not join letters
    
    if ccd_no == "0":
        return

    if len(clean_ccd) == 16:
        cursor.execute("SELECT CUST_CC_NO FROM CDW_SAPP_CREDIT_CARD WHERE CUST_CC_NO = %s", (clean_ccd,))
        result = cursor.fetchall()

        if result:
            print("Thank you for entering the credit card number.")
            return clean_ccd
        else:
            print("Credit card number not found. Please try again.")                       
            return validate_ccd()
    else:
        print("Not a valid credit card number. Please try again.")                
        return validate_ccd()


def gen_mo_bill():
    ccd_no = validate_ccd()
    
    if ccd_no is None:
        return

    bill_date =  validate_month_year()

    if bill_date is None:
        return  
    
    billdate_wildcard = bill_date + "%"

    gen_bill_query = """SELECT TRANSACTION_ID, TRANSACTION_TYPE, TIMEID, TRANSACTION_VALUE  
                        FROM CDW_SAPP_CREDIT_CARD
                        WHERE CUST_CC_NO = %s AND TIMEID LIKE %s
                        ORDER BY TIMEID
                    """ 
    cursor.execute(gen_bill_query, (ccd_no, billdate_wildcard))
    results = cursor.fetchall()

    if not results:
        print("No results found.")
        user_input = input("To return to the main menu, enter 0; enter any key to search for another credit card number and date. ")
        if user_input != "0":
            gen_mo_bill()
            return
        
    else:
        # Process the results
        year = bill_date[:4]
        month = bill_date[4:]
        print(f"Bill for credit card number {ccd_no} for {month}/{year}:")
        print("")
        header_row = [i[0] for i in cursor.description]
        print(tabulate(results, headers=header_row))
        print("")

        total_amt_due = """SELECT ROUND(SUM(TRANSACTION_VALUE),2) AS TOTAL  
                        FROM CDW_SAPP_CREDIT_CARD
                        WHERE CUST_CC_NO = %s AND TIMEID LIKE %s                        
                    """ 
        cursor.execute(total_amt_due, (ccd_no, billdate_wildcard))
        total = cursor.fetchone()[0]
        print(f"Total amount due: ${total}")
        print("")

        user_input = input("To return to the main menu, enter 0; enter any key to generate another bill. \n")
        if user_input != "0":
            gen_mo_bill()
#################################################################################################
# 4) Used to display the transactions made by a customer between two dates. Order by year, month, and day in descending order.

def cust_trans_btwn_dates():
    custSSN = choose_customerSSN()

    if custSSN is None:
        return

    while True:
        start_date = input("Enter the start date: (YYYYMMDD) ") 
        end_date = input("Enter the end date: (YYYYMMDD) ")

        get_trans_query = """SELECT TRANSACTION_ID, TIMEID, TRANSACTION_TYPE, TRANSACTION_VALUE
                            FROM CDW_SAPP_CREDIT_CARD
                            WHERE CUST_SSN = %s AND TIMEID BETWEEN %s AND %s
                            ORDER BY TIMEID DESC
                            """
        cursor.execute(get_trans_query, (custSSN, start_date, end_date))
        results = cursor.fetchall()

        if results:
            print(f"Transactions for customer SSN {custSSN} between {start_date} and {end_date}:")
            print("")
            header_row = [i[0] for i in cursor.description]
            print(tabulate(results, headers=header_row))
            print("")
            break

        else:
            print("Date range not found. Please try again")
            print("")
        
    user_input = input("To return to the main menu, enter 0; enter any key to view more transactions. ")
    if user_input != "0":
        cust_trans_btwn_dates()

#################################################################################################
#################################################################################################
# Main program loop 
while True:
    display_mainmenu()
    choice = input("Enter the number that corresponds to your choice: ")

    if choice == "1":
        zip_date_transactions()
    elif choice == "2":
        trans_by_type()
    elif choice == "3":
        trans_by_branchstate()
    elif choice == "4":
        cust_acct_deets()
    elif choice == "5":
        modify_cust_acct()
    elif choice == "6":
        gen_mo_bill()
    elif choice == "7":
        cust_trans_btwn_dates()
    elif choice == "0":
        logout_exit()
    else:
        print("Invalid choice. Please try again.")
