import sqlite3
conn = sqlite3.connect('credentials.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS
(NAME TEXT PRIMARY KEY NOT NULL, 
 PASSWORD TEXT NOT NULL, 
 PHONE INT NOT NULL, 
 EMAIL TEXT NOT NULL)''')
if fetch.fetchone != None:
    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL)\
        VALUES('ADMIN', 'ADMINPWD', 0199999999, 'admin@email.com') ");
    conn.commit()

def signUp():   
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

def adminFeature():
    print("adminFeature")

def book_func():
    
    c.execute('''CREATE TABLE IF NOT EXISTS TEST 
                (BOOK_ID INT PRIMARY KEY NOT NULL, 
                BOOK_NAME TEXT NOT NULL, 
                BOOK_AMOUNT INT NOT NULL, 
                BOOK_STATUS TEXT NOT NULL)''')
        
    book_id = int(input('Enter Book ID: '))
    fetch  = c.execute('SELECT BOOK_ID from TEST WHERE BOOK_ID=?', (book_id,))
    while book_id == '':
        print('Book_ID cannot be empty.')
        book_id = int(input('Enter Book ID: '))
    while book_id == '' or fetch.fetchone() != None:
        print('ID has already excisted.')
        book_id = int(input('Enter Book ID: '))

    book_name = str(input('Enter Book Name: '))
    while book_name == '':
        print('Book Name cannot be empty.')
        book_name = str(input('Enter Book Name: '))
    
    book_amount = int(input('Enter Book Amount: '))
    while book_amount == '':
        print('Please enter an value.')
        book_amount = int(input('Enter Book Amount: '))
    
    book_status = str(input('Enter book status(T/F): '))
    
    c.execute('INSERT INTO TEST (BOOK_ID,BOOK_NAME,BOOK_AMOUNT,BOOK_STATUS) VALUES(?,?,?,?)',(book_id,book_name,book_amount,book_status))
    print('Added succesfully.')
    conn.commit()    

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
    for data in loginData:
        user = data[0]
    if user == 'ADMIN':
        adminFeature()
    else:
        studentFeature()

#Update amount
def update_amount(book_amount,book_id):
    new_amount = """UPDATE BOOKS SET BOOK_AMOUNT = ? WHERE BOOK_ID = ?"""
    data = (book_amount,book_id)
    c.execute(new_amount,data)
    conn.commit()
    print('Update successfully.')
    c.close()

#Minus amount
def minus_amount():
    book_id = input('Enter book id: ')
    minus_amount = int(input('Enter amount minus: ')) 
    amount = c.execute('SELECT BOOK_AMOUNT from BOOKS WHERE BOOK_ID=?', (book_id,))
    for x in amount:
        final_amount = x[0] - minus_amount
    total = final_amount
    update_amount(total,book_id)      
      
#main
menu()
