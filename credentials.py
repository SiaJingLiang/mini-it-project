import sqlite3, sys
conn = sqlite3.connect('credentials.db')
c = conn.cursor()

def signUp():
    c.execute('CREATE TABLE IF NOT EXISTS CREDENTIALS (NAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL, PHONE INT NOT NULL, EMAIL TEXT NOT NULL)')
    name = username()
    pwd = password()
    phone = telephone()
    email = mail()
    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL) VALUES(?, ?, ?, ?)",(name, pwd, phone, email,))
    conn.commit()

def username():
    name = str(input("Enter Username: "))
    fetch = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
    if fetch.fetchone() != None:
        print("Username taken. ")
        username()
    else:
        return name
    
def password():
    pwd = str(input("Enter password (at least 10 characters): "))
    if len(pwd) < 10:
        print("Too short. ")
        password()
    else:
        return pwd

def telephone():
    phone = input("Enter phone: ")
    if len(phone) < 10 or len(phone) > 11 or phone.isdigit() == False:
        print("Phone number invalid. ")
        telephone()
    else:
        return phone

def mail():
    email = str(input("Enter email: "))
    if '@' not in email:
        print("Email invalid. ")
        mail()
    else:
        return email

signUp()
table = c.execute('SELECT * from CREDENTIALS')
for x in table:
    print(x)
    
