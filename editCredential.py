from tabulate import tabulate
import sqlite3
conn = sqlite3.connect('credentials.db')
c = conn.cursor()

def edit_credential(): 
    choices = int(input("Edit: \n[1]Name \n[2]Password \n[3]Phone \n[4]Email \nEnter choice: "))
    if choices == 1:
        choice = "name"  
        value = str(input("Enter name: "))
        fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
        while value == '':
            print("Username cannot be empty. ")
            value = str(input("Enter name: "))
        while value == '' or fetch.fetchone() != None:
            print("Username has been taken")
            value = str(input("Enter name: "))
            
    elif choices == 2:
        choice = "password"
        value = str(input("Enter password (at least 10 characters): "))
        while value == '' or len(value) < 10:
            print("Password invalid. ")
            value = str(input("Enter password (at least 10 characters): "))

    elif choices == 3:
        choice = "phone"
        value = input("Enter phone: ")
        while  value == '' or len(value) < 10 or len(value) > 11 or value.isdigit() == False:
            print("Phone number invalid. ")
            value = input("Enter phone: ")

    elif choices == 4:
        choice = "email"
        value = str(input("Enter email: "))
        while value == '' or '@' not in value:
            print("Email invalid. ")
            value = str(input("Enter email: "))

    #need get name from global
    c.execute(f"UPDATE CREDENTIALS set {choice} = {value} WHERE NAME={name}")
    print("Signed up successfully. ")
    conn.commit()