import pandas as pd
import sqlite3
from datetime import datetime
from sqlite3 import Error
import csv


# import matplotlib.pyplot as plt


# import plotly.express as px

# Subject   : PROG-8420
# Student_ID: 8715911 ,8758098, 8714965, 8804665
# Student   : Deep Bhatt, Monark Bhatt, Helly Darji, Utkarshkumar Patel


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
        conn = sqlite3.connect(db_file, timeout=3)
        # print(sqlite3.version)
    except Error as er:
        print(er)
    finally:
        if conn:
            return conn
            conn.close()


if __name__ == '__main__':
    create_connection(r"final_project_database.db")


class EcommerceClass(object):

    def __init__(self):
        self.login_count = 1

    def custlogin(self):
        try:
            ecom_obj.product_price()
            conn = create_connection(r"final_project_database.db")
            cur = conn.cursor()
            try:
                create_cust_query = '''CREATE TABLE IF NOT EXISTS "customers" (cid INTEGER NOT NULL UNIQUE, cust_name TEXT NOT NULL,
                        cust_phone	NUMERIC NOT NULL UNIQUE, cryptographic_password TEXT, "access_count" INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(cid AUTOINCREMENT));'''
                conn.execute(create_cust_query)
                # commit to save query result
                conn.commit()
            except Exception as e:
                print("The", e)
                pass

            # Taking user input
            user_name = input("User Name:- ")
            pw = input("Password:-  ")
            encrypted_password = cipher_conv(pw)
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
                    access_count = cur.fetchone()
                    if access_count:
                        access_count = access_count[0]
                    conn.commit()
                    ecom_obj.to_cart_options(cid)
                    cur.close()
                    conn.close()

                # If User is new user then create user and register
                else:
                    # query to insert new USER
                    print("You are a new customer: ")
                    cust_phone = input("Please enter phone number")
                    cur.execute(
                        "INSERT INTO customers (cust_name,cust_phone, cryptographic_password) VALUES('{}','{}','{}');".format(
                            user_name, cust_phone,
                            encrypted_password))
                    # commit to save the changes occurred in the table
                    print("New Customer created successfully.")
                    conn.commit()
                # cur.close()
                # conn.close()
            except Exception as e:
                print('')
        except Exception as e:
            print(e)

    def stafflogin(self):
        try:
            conn = create_connection(r"final_project_database.db")
            cur = conn.cursor()
            ecom_obj.product_price()
            try:
                que = '''CREATE TABLE IF NOT EXISTS StaffMember (smid INTEGER NOT NULL UNIQUE, staffm_name TEXT NOT NULL,
                        staffm_phone	NUMERIC NOT NULL UNIQUE, cryptographic_password TEXT, "access_count" INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(smid AUTOINCREMENT));'''
                conn.execute(que)
                # commit to save query result

            except Exception as e:
                print("The", e)
                pass

            # Taking user input
            user_name = input("Staff Member Name:- ")
            pw = input("Password:-  ")
            encrypted_password = cipher_conv(pw)
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

                    cur.execute("COMMIT;")
                    # concatenation
                    if access_count:
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print("Current Time =", current_time)
                    # Let's see the rows in table customers
                    que_table = "SELECT * FROM StaffMember"
                    cur.execute(que_table)
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
                        print("Logged out successfully")
                        pass

                # If User is new user then create user and register
                else:
                    # query to insert new USER
                    print("New Staff Member: ")
                    staff_phone = input("Please enter phone number")
                    cur.execute(
                        "INSERT INTO StaffMember (staffm_name,staffm_phone, cryptographic_password) VALUES('{}','{}','{}');".format(
                            user_name, staff_phone,
                            encrypted_password))
                    # commit to save the changes occurred in the table
                    cur.execute("COMMIT;")
                    print("New staff Member created. To use features/functions, login again")
                    cur.close()
                    conn.close()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    def product_price(self):
        try:
            conn = create_connection(r"final_project_database.db")
            cur = conn.cursor()
            try:
                cur.execute('SELECT * FROM products;')
                productprice_csv = cur.fetchall()
                if productprice_csv:
                    with open('productprice.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Product_ID', 'Product_Name', 'Unit_Price'])
                        writer.writerows(productprice_csv)
                cur.close()
                conn.close()

            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    def create_product(self):
        try:

            conn = create_connection(r"final_project_database.db")
            cur = conn.cursor()
            prod_name = input("Enter product name:")
            prod_price = int(input("Enter product price:"))
            try:
                if prod_name == "" or prod_price == "":
                    print("product_name OR price can not be empty")
                elif not prod_name == "" and not prod_price == "":
                    if prod_price < 0:
                        print("product price can not be less than zero")
                    else:
                        cur.execute(
                            "CREATE TABLE IF NOT EXISTS products (pid INTEGER NOT NULL UNIQUE, prod_name	TEXT NOT NULL,"
                            "unit_price	INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(pid AUTOINCREMENT));")

                        cur.execute("INSERT INTO products (prod_name, unit_price) VALUES (?, ?);",
                                    (prod_name, prod_price))
                        cur.execute("COMMIT;")
                        print("Product has been created successfully...")
                        cur.close()
                        conn.close()
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

    def show_products(self):
        df = pd.read_csv(r'productprice.csv', sep=',')

        print(df.to_string(index=False))
        return df

    def add_prod_to_cart(self, custid):
        try:
            conn = create_connection(r"final_project_database.db")
            cur = conn.cursor()
            pid = input("enter pid:")
            que_exi_prod = "SELECT prod_name, unit_price FROM products WHERE pid = '{}'".format(pid)

            # executing the query
            cur.execute(que_exi_prod)
            que_exi_use_find = cur.fetchone()
            prod_name = "SELECT prod_name FROM products WHERE pid = '{}'".format(pid)
            prod_price = "SELECT unit_price FROM products WHERE pid = '{}'".format(pid)
            # if there is any response, this 'if' part will run
            cur.execute(prod_name)
            prod_name_find = cur.fetchone()
            cur.execute(prod_price)
            prod_price_find = cur.fetchone()
            if que_exi_use_find:
                pname = prod_name_find[0]
                pprice = int(prod_price_find[0])
                print("Product is: ", pname)
                print("Unit price is:", pprice)
                qnt = int(input("Enter product quantity:"))
                total_price = qnt * pprice
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS cart (cartid INTEGER NOT NULL UNIQUE,pid INTEGER, prod_name	TEXT NOT NULL,"
                    "unit_price	INTEGER NOT NULL DEFAULT 0, qnt	INTEGER NOT NULL DEFAULT 1, "
                    "final_price INTEGER NOT NULL DEFAULT 0, cid	INTEGER ,PRIMARY KEY(cartid AUTOINCREMENT),"
                    "FOREIGN KEY(cid) REFERENCES customers(cid));")

                cur.execute(
                    "INSERT INTO cart (pid, prod_name,unit_price, qnt, final_price, cid) VALUES('{}','{}','{}','{}','{}','{}');".format(
                        pid, pname, pprice, qnt, total_price, custid))
                print("Product added into Cart")
                cur.execute("COMMIT;")

                cur.close()

            else:
                print("Product does not exist.")
        except Exception as e:
            print("error", e)

    def to_cart_options(self, custid):
        conn = create_connection(r"final_project_database.db")
        cur = conn.cursor()
        cur1 = conn.cursor()
        cur2 = conn.cursor()
        vchoice = 0
        while vchoice != '0':
            print('''
            1. View cart
            2. Add product to existing cart
            3. Place order
            4. Go back to previous menu
            0. Exit  
                            ''')
            vchoice = input("Enter choice: ")
            if vchoice == '1':
                try:

                    cur = conn.cursor()
                    cur.execute(
                        "select pid, prod_name, qnt, unit_price, final_price from cart where cid = '{}'".format(custid))
                    testcart = cur.fetchall()
                    cur1 = conn.cursor()
                    cur1.execute("select sum(final_price) from cart where cid = '{}'".format(custid))
                    finalprice = cur1.fetchone()
                    if testcart:
                        with open('testcart.csv', 'w+') as file:
                            writer = csv.writer(file)
                            writer.writerow(['Product_Id', 'Product_Name', 'Quantity', 'Unit_Price', 'Line_Item_Total'])
                            writer.writerows(testcart)
                            writer.writerow([''])
                            writer.writerow(['Grand_Total', finalprice[0]])

                        prodcart = pd.read_csv('testcart.csv', sep=',').fillna(' ')
                        print(prodcart.to_string(index=False, justify='center'))
                        cur.close()
                        cur1.close()
                    else:
                        print("The cart is empty")
                        pass

                except Exception as e:
                    print(e)
            if vchoice == '3':
                now = datetime.now()
                current_time = now.strftime("%d-%m-%y %H:%M:%S")

                try:

                    oid = cur2.execute("select oid from cart where cid = '{}'".format(custid))
                    oid = cur2.fetchone()
                    pid = cur2.execute("select pid from cart where cid = '{}'".format(custid))
                    pid = cur2.fetchone()
                    prod_qty = cur2.execute("select qnt from cart where cid = '{}'".format(custid))
                    prod_qty = cur2.fetchone()
                    lineitem_total = cur2.execute("select final_price from cart where cid = '{}'".format(custid))
                    lineitem_total = cur2.fetchone()

                    cur2.execute('''CREATE TABLE IF NOT EXISTS "order_details" (	"odid"	INTEGER NOT NULL DEFAULT 0 UNIQUE,	"oid"	INTEGER NOT NULL,	"pid"	INTEGER NOT NULL,
                    "prod_qty"	NUMERIC NOT NULL,	"lineitem_total"	NUMERIC NOT NULL,	"OrderDateTime"	INTEGER NOT NULL,	PRIMARY KEY("odid" AUTOINCREMENT)); ''')


                    cur2.execute("insert into order_details( oid, pid,prod_qty ,lineitem_total,OrderDateTime) select distinct cart.oid , cart.pid, cart.qnt, cart.final_price, '{}' from cart WHERE cart.cid ='{}'".format(current_time, custid))
                    cur2.execute("delete from cart where cid = '{}'".format(custid))

                    cur2.execute('commit;')
                    print("Thanks for placing an order")

                        #cur2.close()
                except Exception as e:
                    print(e)

            if vchoice == '2':
                print("Welcome to Cart")
                conn = create_connection(r"final_project_database.db")

                print('''Select from following option
                    1. Add to Cart
                    2. Remove all products from cart
                    0. exit
                    ''')
                choice = '0'
                choice = input("enter choice: ")
                if choice == '1':
                    cur = conn.cursor()
                    ecom_obj.show_products()
                    ecom_obj.add_prod_to_cart(custid)
                    cur.close()
                elif choice == '2':
                    try:
                        flush_table = "DELETE FROM cart where cid = '{}'".format(custid)
                        conn.execute(flush_table)
                        conn.execute("COMMIT;")
                        print("Your cart is now empty")
                    except Exception as e:
                        print(e)
                elif choice == "0":
                    print("Thanks for using our site")
                    exit()
                else:
                    print("Invalid option")
            if vchoice == '0':
                print('Thank You!!')
                exit()


ecom_obj = EcommerceClass()
user_choice = '1'

while user_choice != '0':
    print("\n@@@@@ -----E-commerce Final Project----- @@@@@ ")
    print(''' Select Account type
    1. Staff
    2. Customer ''')
    print("Type '0' to EXIT ")
    print("============================")

    user_choice = input("Enter your choice:")
    if user_choice == "1":
        staff_choice = 0
        while staff_choice != '0':
            print("=======================")
            print('''Staff login. ⬇Select appropriate option from following options️
            1. Staff Login/sign up to access staff functions
            2. Back to main menu
            0. Exit ''')
            print("=======================")
            staff_choice = input("Enter staff choice: ")
            if staff_choice == "1":
                ecom_obj.stafflogin()
            elif staff_choice == "2":
                print("Exit from staff ")
                break
            elif staff_choice == "0":
                print("Thanks for using our site")
                exit()
            else:
                print("\nInvalid option...Please enter a proper option...!!!")
    elif user_choice == "2":
        customer_choice = 0
        while customer_choice != '0':
            print("=======================")
            print('''   Customer section. Select appropriate option from following options
            1. Customer sign in/sign up 
            2. Back to main menu        
            0. Exit''')
            print("=======================")
            customer_choice = input(" Enter customer option: ")
            if customer_choice == "1":
                ecom_obj.custlogin()
            elif customer_choice == "2":
                break
            elif customer_choice == "0":
                print("Thanks for using our site")
                exit()
            else:
                print("\nInvalid option...Please enter a proper option...!!!")
    elif user_choice == "0":
        print("********************...Thanks...Good bye...Enjoy...******************")
        break
    else:
        print("\nInvalid option...Please enter a proper option...!!!")
