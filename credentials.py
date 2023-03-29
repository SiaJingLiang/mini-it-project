import sqlite3, sys
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
    while fetch.fetchone() != None:
        print("Username has been taken")
        name = str(input("Enter name: "))
    
    pwd = str(input("Enter password (at least 10 characters): "))
    while pwd == '':
        print("Password cannot be empty. ")
        pwd = str(input("Enter password: "))
    while len(pwd) < 10:
        print("Too short. ")
        pwd = str(input("Enter password (at least 10 characters): "))

    phone = input("Enter phone: ")
    while phone == '':
        print("Phone no. cannot be empty: ")
    while len(phone) < 10 or len(phone) > 11 or phone.isdigit() == False:
        print("Phone number invalid. ")
        phone = int(input("Enter phone: "))

    email = str(input("Enter email: "))
    while email == '':
        print("Email cannot be empty. ")
        email = str(input("Enter email: "))
    while '@' not in email:
        print("Email invalid. ")
        email = str(input("Enter email: "))

    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL) VALUES(?, ?, ?, ?)",(name, pwd, phone, email))
    print("Signed up successfully. ")
    conn.commit()
    print("Go to menu")

signUp()
table = c.execute('SELECT * from CREDENTIALS')
for x in table:
    print(x)
    
