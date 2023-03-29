import sqlite3
conn = sqlite3.connect('credentials.db')
c = conn.cursor()

def signUp():
    c.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS 
                (NAME TEXT PRIMARY KEY NOT NULL, 
                 PASSWORD TEXT NOT NULL, 
                 PHONE INT NOT NULL, 
                 EMAIL TEXT NOT NULL)''')
    
    name = str(input("Enter name: "))
    fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
    while name == '':
        print("Username cannot be empty. ")
        name = str(input("Enter name: "))
    while name == '' or fetch.fetchone() != None:
        print("Username has been taken")
        name = str(input("Enter name: "))
    
    pwd = str(input("Enter password (at least 10 characters): "))
    while pwd == '' or len(pwd) < 10:
        print("Password invalid. ")
        pwd = str(input("Enter password (at least 10 characters): "))

    phone = input("Enter phone: ")
    while  phone == '' or len(phone) < 10 or len(phone) > 11 or phone.isdigit() == False:
        print("Phone number invalid. ")
        phone = input("Enter phone: ")

    email = str(input("Enter email: "))
    while email == '' or '@' not in email:
        print("Email invalid. ")
        email = str(input("Enter email: "))

    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL) VALUES(?, ?, ?, ?)",(name, pwd, phone, email))
    print("Signed up successfully. ")
    conn.commit()
    menu()

def checklogin(name,pwd):
    check = c.execute('SELECT * from CREDENTIALS WHERE NAME=? AND PASSWORD=?', (name, pwd))
    for row in check:
        if row != None:
            return True
        else:
            return False

def studentFeature():
    print("studentFeature")

def managerFeature():
    print("managerFeature")

def menu():
    login = False
    choice = int(input("[1]Login \n[2]Sign Up \n[3]End \nEnter your choice: "))
    if choice == 1:
        name = str(input("Enter username: "))
        pwd = str(input("Enter password: "))
        login  = checklogin(name, pwd)
        if login == True:
            loginData = c.execute('SELECT * from CREDENTIALS WHERE NAME=? AND PASSWORD=?', (name, pwd))
            print("Login successful. ")
            print("Welcome", name)
        else:
            print("Username or password incorrect. ")
            menu()
            quit()
    elif choice == 2:
        signUp()
    elif choice == 3:
        quit()
    else:
        menu()
        quit()

    #all the feature after done the login
    studentFeature()
    print("After login feature")


#main
menu()
