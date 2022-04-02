# Subject   : PROG-8420
# Student_ID: 8758098
# Student   : Monark Bhatt


# importing library
import sqlite3
from sqlite3 import Error
import csv


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
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
    connection = create_connection(r"final_project_database.db")
    cursor = connection.cursor()

    def __init__(self):
        self.login_count = 1

    def create_product(self):
        try:
            prod_name = input("Enter product name:")
            prod_price = int(input("Enter product price:"))
            try:
                if prod_name == "" or prod_price == "":
                    print("product_name OR price can not be empty")
                elif not prod_name == "" and not prod_price == "":
                    if prod_price < 0:
                        print("product price can not be less than zero.")
                    else:
                        connection = create_connection(r"final_project_database.db")
                        cursor = connection.cursor()

                        cursor.execute(
                            "CREATE TABLE IF NOT EXISTS products (pid INTEGER NOT NULL UNIQUE, prod_name	TEXT NOT NULL,"
                            "unit_price	INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(pid AUTOINCREMENT));")

                        cursor.execute("INSERT INTO products (prod_name, unit_price) VALUES (?, ?);",(prod_name,prod_price))
                        cursor = connection.cursor()
                        print("Product has been created successfully...")
                        cursor.execute("COMMIT;")
                        cursor.close()
                        connection.close()
                        return True
            except TypeError:
                print("Entered data format incorrect")
            except ValueError:
                print("Entered value is not proper")
            else:
                print("Error came...")
        except Exception:
            print("Error came...")


ecom_obj = EcommerceClass()
user_choice = '1'

while user_choice != '0':
    print("\n@@@@@ -----E-commerce Final Project----- @@@@@ ")
    print("1. Create a Product")
    print("Type '0' to EXIT")
    print("================================================")

    user_choice = input("Enter you choice:")
    if user_choice == "1":
        print("=======================")
        print("To Create a Product")
        print("=======================")
        ecom_obj.create_product()
    elif user_choice == "0":
        print("********************...Thanks...Good bye...Enjoy...******************")
        break
    else:
        print("\nInvalid option...Please enter a proper option...!!!")
