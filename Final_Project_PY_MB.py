# Subject   : PROG-8420
# Student_ID: 8758098, 8804665
# Student   : Monark Bhatt, Utkarshkumar Patel


# importing library
import sqlite3
from datetime import datetime
from sqlite3 import Error
import csv
#import pandas as pd
#import plotly.express as px


def cipher_conv(password):
    # key to convert user input
    original = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"
    key = "TIMEODANSFRBCGHJKLPQUVWXYZ9876543210timeodansfrbcghjklpquvwxyz"
    txt = password
    # First declare an empty string
    # for every original letter, it will find the cipher letter from 'key' and store it into the 'ciphered'
    ciphered = ""
    for letter in txt:
        if letter in original:
            ciphered += key[original.find(letter)]
        else:
            ciphered += letter

    return ciphered


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file,timeout=10)
        #print(sqlite3.version)
    except Error as er:
        print(er)
    finally:
        if conn:
            return conn
            conn.close()


if __name__ == '__main__':
    create_connection(r"final_project_database.db")



class EcommerceClass(object):
    #connection = create_connection(r"final_project_database.db")
    #cursor = connection.cursor()

    def __init__(self):
        self.login_count = 1

    def custlogin(self):
        try:
            conn = create_connection(r"final_project_database.db")

            try:
                cur = conn.cursor()

                que = '''CREATE TABLE "customers" (cid INTEGER NOT NULL UNIQUE, cust_name TEXT NOT NULL,
                        cust_phone	NUMERIC NOT NULL UNIQUE, cryptographic_password TEXT, "access_count" INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(cid AUTOINCREMENT));'''
                conn.execute(que)
                print("Table created ")
                # commit to save query result
                conn.commit()
            except Exception as e:
                print("The", e)
                pass

            # Taking user input
            user_name = input("User Name:- ")
            pw = input("Password:-  ")
            encrypted_password = cipher_conv(pw)
            print("after pw")
            print("Cipher password is ", encrypted_password)
            try:
                # .format let us insert and do data formatting in the query
                # Since the USER_ID is unique, there will be only one USER_ID assigned to each user
                que_exi_user = "SELECT cid FROM customers WHERE cust_name = '{}'".format(user_name)
                # executing the query
                cur.execute(que_exi_user)
                que_exi_use_find = cur.fetchone()
                # if there is any response, this 'if' part will run
                if que_exi_use_find:
                    cid = que_exi_use_find[0]
                    print("Customer ID is found and is: ", cid)
                    # Increase the login access_count by 1
                    cur.execute(
                        "UPDATE customers SET access_count = access_count + 1 WHERE cid = {};".format(cid))

                    # let's display the access_count column
                    cur.execute('select access_count from  customers where cid ={};'.format(cid))
                    print("find")
                    access_count = cur.fetchone()
                    if access_count:
                        access_count = access_count[0]
                    conn.commit()
                    # concatenation
                    if access_count:
                        print("User ID '" + user_name + "' has accessed " + str(access_count) + " times")
                    # Let's see the rows in table customers
                    que_table = "SELECT * FROM customers"
                    cur.execute(que_table)
                    # print("Updated Table")
                    # print(cur.fetchall())

                # If User is new user then create user and register
                else:
                    # query to insert new USER
                    print("new customer: ")
                    cust_phone = input("Please enter phone number")
                    cur.execute(
                        "INSERT INTO customers (cust_name,cust_phone, cryptographic_password) VALUES('{}','{}','{}');".format(user_name, cust_phone,
                                                                                                       encrypted_password))
                    # commit to save the changes occurred in the table
                    print("inserted")
                    conn.commit()
                    print("new user")

                # Exporting table customers into CSV file by fetching all the results we get from query
                # make sure you have set the csv path
                # cur.execute('SELECT * FROM customers;')
                # customers_csv = cur.fetchall()
                # if customers_csv:
                    #     with open(csv_path, 'w') as file:
                    #     writer = csv.writer(file)
                        # select columns names to write rows in that sequence
                    #     writer.writerow(['USER_ID', 'LOGIN', 'PASSWORD', 'access_count'])
                        # writer.writerows(customers_csv)

            except Exception as e:
                # remove curser
                cur.close()
            cur.close()
        except Exception as e:
            # close the connection
            conn.close()

    def stafflogin(self):
        try:
            conn = create_connection(r"final_project_database.db")

            try:
                cur = conn.cursor()

                que = '''CREATE TABLE "StaffMember" (smid INTEGER NOT NULL UNIQUE, staffm_name TEXT NOT NULL,
                        staffm_phone	NUMERIC NOT NULL UNIQUE, cryptographic_password TEXT, "access_count" INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(smid AUTOINCREMENT));'''
                conn.execute(que)
                print("Table created ")
                # commit to save query result
                cur.execute("COMMIT;")
                #conn.commit()
            except Exception as e:
                print("The", e)
                pass

            # Taking user input
            user_name = input("Staff Member Name:- ")
            pw = input("Password:-  ")
            encrypted_password = cipher_conv(pw)
            print("after pw")
            print("Cipher password is ", encrypted_password)
            try:
                # .format let us insert and do data formatting in the query
                # Since the USER_ID is unique, there will be only one USER_ID assigned to each user
                que_exi_user = "SELECT smid FROM StaffMember WHERE staffm_name = '{}'".format(user_name)
                # executing the query
                cur.execute(que_exi_user)
                que_exi_use_find = cur.fetchone()
                # if there is any response, this 'if' part will run
                if que_exi_use_find:
                    smid = que_exi_use_find[0]
                    print("Staff ID is found and is: ", smid)
                    # Increase the login access_count by 1
                    cur.execute(
                        "UPDATE StaffMember SET access_count = access_count + 1 WHERE smid = {};".format(smid))

                    # let's display the access_count column
                    cur.execute('select access_count from  StaffMember where smid ={};'.format(smid))
                    print("find")
                    access_count = cur.fetchone()
                    if access_count:
                        access_count = access_count[0]
                    #conn.commit()
                    cur.execute("COMMIT;")
                    # concatenation
                    if access_count:
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print("Current Time =", current_time)
                        print("Staff Member ID '" + user_name + "' has accessed " + str(access_count) + " times")
                    # Let's see the rows in table customers
                    que_table = "SELECT * FROM StaffMember"
                    cur.execute(que_table)
                    # print("Updated Table")
                    # print(cur.fetchall())

                    print('''Select from available choices
                    1. Create product
                    2. Generate product-price info report
                    0. Log out and back to main menu''')
                    func_choice = input("Enter choice: ")
                    if func_choice == "1":
                        conn.close()
                        ecom_obj.create_product()
                    elif func_choice == "2":
                        ecom_obj.product_price()
                    elif func_choice == "0":
                        print("Log out successful")
                        pass

                # If User is new user then create user and register
                else:
                    # query to insert new USER
                    print("New Staff Member: ")
                    staff_phone = input("Please enter phone number")
                    cur.execute(
                        "INSERT INTO StaffMember (staffm_name,staffm_phone, cryptographic_password) VALUES('{}','{}','{}');".format(user_name, staff_phone,
                                                                                                       encrypted_password))
                    # commit to save the changes occurred in the table
                    print("inserted")
                    #conn.commit()
                    cur.execute("COMMIT;")
                    print("New staff Member created. To use features/functions, login again")



            except Exception as e:
                # remove curser
                cur.close()
            cur.close()
        except Exception as e:
            # close the connection
            conn.close()

    def product_price(self):

        try:
            conn = create_connection(r"final_project_database.db")
            print("Connection established")
            try:
                cur = conn.cursor()
                cur.execute('SELECT * FROM products;')
                productprice_csv = cur.fetchall()
                csv_path = r"productprice.csv"
                if productprice_csv:
                    with open(csv_path, 'w') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Product ID', 'Product Name', 'Unit Price'])
                        writer.writerows(productprice_csv)
                        print("report generated")

                #df = pd.read_csv('productprice.csv.csv')

               # fig = px.line(df, x='Product Name', y='Unit Price', title='Apple Share Prices over time (2014)')
                #fig.show()
            except Exception as e:
                    # remove curser
                    cur.close()
            cur.close()
        except Exception as e:
                # close the connection
                conn.close()


    def create_product(self):
        try:
            prod_name = input("Enter product name:")
            prod_price = int(input("Enter product price:"))

            try:
                if prod_name == "" or prod_price == "":
                    print("product_name OR price can not be empty")
                elif not prod_name == "" and not prod_price == "":
                    if prod_price < 0:
                        print("product price can not be less than zero")
                    else:
                        connection = create_connection(r"final_project_database.db")
                        cursor = connection.cursor()

                        cursor.execute(
                            "CREATE TABLE IF NOT EXISTS products (pid INTEGER NOT NULL UNIQUE, prod_name	TEXT NOT NULL,"
                            "unit_price	INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(pid AUTOINCREMENT));")

                        cursor.execute("INSERT INTO products (prod_name, unit_price) VALUES (?, ?);", (prod_name, prod_price))
                        cursor.execute("COMMIT;")
                        print("Product has been created successfully...")
                        cursor.close()
                        connection.close()
                        return True
            except TypeError:
                print("Entered data format incorrect")
            except ValueError:
                print("Entered value is not proper")
            except Exception as e:
                print("error: ", e)
            else:
                print("Error came...1")
        except Exception:
            print("Error came...2")


ecom_obj = EcommerceClass()
user_choice = '1'

while user_choice != '0':
    print("\n@@@@@ -----E-commerce Final Project----- @@@@@ ")
    print(''' Select Account type
    1. Staff
    2. Customer ''')
    print("Type '0' to EXIT ")
    print("================================================")

    user_choice = input("Enter your choice:")
    if user_choice == "1":
        print("=======================")
        print('''Staff login. ⬇Select appropriate option from following options⬇⬇️
        1. Staff Login/sign up to access staff functions
        2. Back to main menu
        0. Exit ''')
        print("=======================")
        staff_choice = input("Enter staff choice: ")
        if staff_choice == "1":
            ecom_obj.stafflogin()
        elif user_choice == "2":
            print("Exit from staff ")
            pass
        elif user_choice == "0":
            print("Thanks for using our site")
            break
    elif user_choice == "2":
        print("=======================")
        print('''   Customer section. ⬇Select appropriate option from following options⬇⬇️"
        1. Customer sign in/sign up 
        2. Back to main menu        
        0. Exit''')
        print("=======================")
        customer_choice = input(" Enter customer option: ")
        if customer_choice == "1":
            ecom_obj.custlogin()
        elif customer_choice == "2":
            pass
        elif customer_choice == "0":
            print("Thanks for using our site")
            break

    elif user_choice == "0":
        print("********************...Thanks...Good bye...Enjoy...******************")
        break
    else:
        print("\nInvalid option...Please enter a proper option...!!!")
