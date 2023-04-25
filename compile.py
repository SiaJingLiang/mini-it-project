import sqlite3
import time
from datetime import datetime, timedelta
from tabulate import tabulate
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS
            (NAME     TEXT PRIMARY KEY NOT NULL, 
             PASSWORD TEXT NOT NULL, 
             PHONE    INT  NOT NULL, 
             EMAIL    TEXT NOT NULL,
             PENALTY  REAL )''')
fetch = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?',('ADMIN',))
if fetch.fetchone() == None:
    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL, PENALTY)\
        VALUES('ADMIN', 'ADMINPWD', 0199999999, 'admin@email.com', 0) ")
    conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS BOOKS 
                (ID INT PRIMARY KEY NOT NULL,
                TITLE TEXT NOT NULL,
                AUTHOR TEXT,
                CATEGORY TEXT NOT NULL,
                LANGUAGE TEXT NOT NULL,
                FICTION TEXT NOT NULL, 
                AMOUNT INT NOT NULL,
                PRICE REAL NOT NULL, 
                PUBLISHER TEXT NOT NULL,
                YEAR INT );''')

c.execute('''CREATE TABLE IF NOT EXISTS LIST
         (ID           INT       NOT NULL, 
          TITLE        TEXT      NOT NULL,
          BORROWEDBY   TEXT      NOT NULL,  
          BORROWEDDATE TIMESTAMP NOT NULL,
          EXPIREDDATE  TIMESTAMP NOT NULL, 
          COLLECT      INT       NOT NULL)''')

def signUp():   
    name = str(input("Enter name: "))
    fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
    while name == '':
        print("Username cannot be empty. ")
        name = str(input("Enter name: "))
    while name == '' or fetch.fetchone() != None:
        print("Username has been taken")
        name = str(input("Enter name: "))
        fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (name,))
    
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

    c.execute("INSERT INTO CREDENTIALS (NAME, PASSWORD, PHONE, EMAIL, PENALTY) VALUES(?, ?, ?, ?, ?)",(name, pwd, phone, email, 0))
    print("Signed up successfully. ")
    conn.commit()
    main()
    quit()

def checklogin(name,pwd):
    check = c.execute('SELECT * from CREDENTIALS WHERE NAME=? AND PASSWORD=?', (name, pwd))
    for row in check:
        if row != None:
            return True
        else:
            return False

def titlef():
    global title
    title = str(input("Title: "))
    while title == '':
        print("Invalid")
        title = str(input("Title: "))

def categoryf():
    global category, catChoice, ficChoice, langChoice
    categoryList =['Literature', 'Encyclopedia', 'Guidlines', 'Motivations', 'Dictionary', 'History', 'News', 'Others']
    catChoice = int(input("[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
    while catChoice < 1 or catChoice >9:
        print("Input invalid. ")
        catChoice = int(input("[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
    category = categoryList[catChoice-1]
    fictionf()
    languagef()

def amountf():
    global amount
    amount = input("Enter amount: ")
    while amount == '' or int(amount) <= 0 or amount.isdigit() == False:
        print("Invalid")
        amount = input("Enter amount: ")

def pricef():
    global price
    price = input("Enter price: RM")
    while price == '':
        print("Invalid")
        price = input("Enter price: RM")
    price = format(float(price), ".2f")

def authorf():
    global author
    author = str(input("Enter author: "))
    while author == '':
        print("Invalid")
        author = str(input("Enter author: "))

def languagef():
    global langChoice, language
    languageList = ["English", "Malay", "Chinese", "Tamil", "Others"]
    langChoice = int(input("[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: "))
    while langChoice == '':
        print("Invalid")
        langChoice = input("[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: ")
    language = str(languageList[langChoice-1])

def fictionf():
    global ficChoice, fiction
    ficChoice = input("[1]Fiction\n[2]Non-fiction\nEnter choice: ")
    while ficChoice not in ('1', '2'):
        print("Invalid")
        ficChoice = input("[1]Fiction\n[2]Non-fiction\nEnter choice: ")
    if ficChoice == '1':
        fiction = str("Fiction")
    else:
        fiction = str("Non-fiction")

def commitf(index, title, author, category, language, fiction, amount, price, publisher, year,):
    amountl = int(1)
    if int(amount) > 1:
        for i in range (1, int(amount) + 1):
            c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, title, author, category, language, fiction, amountl, price, publisher, year,))
            index = int(index) + 1
    else:
        c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, title, author, category, language, fiction, amountl, price, publisher, year,))
    conn.commit()
    print("Book has been added. ")
    
def idf(catChoice, langChoice, ficChoice):
    #id = category, language, fiction, index
    global index
    catChoice = str(catChoice)
    langChoice = str(langChoice)
    ficChoice = str(ficChoice)
    x = (catChoice + langChoice + ficChoice + "0001")
    row = c.execute("SELECT * FROM BOOKS")
    existance = row.fetchone()
    rows = c.execute("SELECT * FROM BOOKS")
    quantity = len(rows.fetchall())
    x = int(x)
    if existance == None:
        index = int(x)
    elif quantity >= 1:
        result = c.execute("SELECT * FROM BOOKS")
        for y in result:
            if y[0] == x:
                x += 1
        index = x
    print(index)

def publisherf():
    global publisher
    publisher = str(input("Enter publisher: "))
    while publisher == "":
        print("Invalid")
        publisher = str(input("Enter publisher: "))

def yearf():
    global year
    year = input("Enter year: ")
    while year == '' or year.isdigit() == False:
        print("Invalid")
        year = input("Enter year: ")
    year = int(year)
   
def addBooks():
    titlef()
    categoryf()
    amountf()
    pricef()
    authorf()
    idf(catChoice, langChoice, ficChoice)
    publisherf()
    yearf()
    print(f"\nTitle: {title} \nCategory: {category} \nFiction: {fiction} \nLanguage: {language} \nAmount: {amount} \nPrice: {price} \nAuthor: {author} \nIndex: {index} \nPublisher: {publisher}")
    commitf(index, title, author, category, language, fiction, amount, price, publisher, year)
    print("Back to menu to make any changes. ")
    
#def menu():
def searchBook():
    choice = int(input("[1]Search Book \n[2]View All Books \n[3]Back to menu \nEnter your choice: "))
    while choice == '' or choice < 1 or choice > 3: 
        print("Input Invalid")
        choice = int(input("[1]Search Book \n[2]View All Books \n[3]Back to menu \nEnter your choice: "))
    if choice == 1:
        search_menu()
    elif choice == 2:
        view_all_books()
    else:
        studentFeature()

def search_menu():
    choices = ["title", "author", "year", "category", "language", "amount", "publisher"]
    choice_input = int(input("Search with: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Availability \n[7]Publisher \n[8]Back to menu \nEnter your choice: "))
    while choice_input < 1 or choice_input > 8:
        choice_input = int(input("Search with: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Availability \n[7]Publisher \n[8]Back to menu \nEnter your choice: "))
    if choice_input == 8:
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()
    else:
        choice = choices[choice_input-1]
        if choice_input == 6:
            user_input = str(input(f"Enter {choice} (0 or 1): "))
        else:
            user_input = str(input(f"Enter {choice}: "))
    #print(library)
    data = []
    c.execute(f"SELECT ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PUBLISHER, YEAR FROM books WHERE {choice} LIKE ?", ("%" + user_input + "%",))
    books = c.fetchall()
    if len(books) == 0:
        print("No books found.")
    else:
        print("Search results:")
        for book in books:
            data.append(book)
        listing(data)

    while True:
        if user != "ADMIN":
            choice = int(input("[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >4:
                choice = input("Invalid input. \n[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                BorrowBook(0)
            elif choice == 3:
                print("we will proceed back to menu")
                studentFeature()

        elif user == "ADMIN":
            choice = int(input("[1]Another search \n[2]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >3:
                choice = input("Invalid input. \n[1]Another search \n[2]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                print("we will proceed back to menu")
                adminFeature()

def view_all_books():
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    data = []
    if len(books) == 0:
       print("No books found.")
    else:
        print("Books:")
        for book in books:
            data.append(book)
        listing(data)
    
    while True:
        if user != "ADMIN":
            choice = int(input("[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >4:
                choice = input("Invalid input. \n[1]Another search \n[2]Borrow Book \n[3]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                BorrowBook(0)
            elif choice == 3:
                print("we will proceed back to menu")
                studentFeature()

        elif user == "ADMIN":
            choice = int(input("[1]Another search \n[2]Back to menu \nEnter your choice: "))
            while choice < 1 or choice >3:
                choice = input("Invalid input. \n[1]Another search \n[2]Back to menu \nEnter your choice: ")
            if choice == 1:
                search_menu()
            elif choice == 2:
                print("we will proceed back to menu")
                adminFeature()

def listing(data):
    headers = ["ID", "TITLE", "AUTHOR", "CATEGORY", "LANGUAGE", "FICTION", "AVAILABILITY", "PRICE", "PUBLISHER", "YEAR"]
    print(tabulate(data, headers=headers, tablefmt="outline"))

def check_expiry(expiry):
    if str(expiry[0]) == 0:
        month = str(expiry[1])
    else:
        month = str(expiry[0]+expiry[1])
    year = str(expiry.split("/")[1])
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%Y", named_tuple)
    month1 = str(time_string.split("/")[0])
    year1 = str(time_string.split("/")[1])
    if int(year) < int(year1):
        print("Credit card is expired. ")
        return False
    elif int(year) == int(year1):
        if int(month) < int(month1):
            print("Credit card is expired. ")
            return False
        else:
            return True
    elif int(year) > int(year1):
        return True

def Card(penalty,user,username):
    card_number = int(input("Enter card number (without dash): "))
    while len(str(card_number)) != 12:
        card_number = int(input("Invalid number, please enter again (without dash): "))
    expiry = str(input("Enter expiry date (MM/YYYY): "))
    expDate = check_expiry(expiry)
    if expDate == False:
        choose = input("Do you want to continue? y/n: ")
        while choose not in ["n", "y"]:
            choose = str(input("continue? y/n: "))
        if choose == "y":
            Card(penalty,user,username)
        if choose == "n":
            if user == "ADMIN":
                adminFeature()
            else:
                studentFeature()
    elif expDate == True:
        cvv = str(input("Enter CVV: "))
        while len(cvv) != 3:
            cvv = int(input("Invalid CVV, please enter again: "))
        pin = int(input("Enter pin: "))
        choose = str(input("Confim payment? y/n: "))
        while choose not in ["n", "y"]:
            choose = str(input("continue? y/n: "))
        if choose == "n":
            if user == "ADMIN":
                adminFeature()
            else:
                studentFeature()
        elif choose == "y":
            print("Connecting...")
            time.sleep(3.0)
            print("Authenticating...")
            time.sleep(2.0)
            print("Payment success. ")  
        
            c.execute('UPDATE CREDENTIALS SET PENALTY=0 WHERE NAME=?',(username,))
            conn.commit()
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()

import webbrowser
def eWallet(penalty, user, username):
    print(f"Amount u need to pay is {penalty}")
    tbc = str(input("Confim payment? y/n: "))
    while tbc not in ["n", "y"]:
        tbc = str(input("Continue? y/n: "))
    if tbc == "n":
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()
    elif tbc == "y":
        url = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fen.m.wikipedia.org%2Fwiki%2FFile%3ATotally_not_a_Rickroll_QR_code.png&psig=AOvVaw0vhkuaQBY9qyqhmJnNaE4L&ust=1682066763179000&source=images&cd=vfe&ved=0CBEQjRxqFwoTCIjV7pCJuP4CFQAAAAAdAAAAABAJ"
        webbrowser.open(url)
        print('Payment success')

        c.execute('UPDATE CREDENTIALS SET PENALTY=0 WHERE NAME=?',(username,))
        conn.commit()
    if user == "ADMIN":
        adminFeature()
    else:
        studentFeature()

def Cash(penalty, user, username):
    print(f"Amount u need to pay is {penalty}")
    tbc = str(input("Confim payment? y/n: "))
    while tbc not in ["n", "y"]:
        tbc = str(input("Continue? y/n: "))
    if tbc == "n":
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()
    elif tbc == "y":
        balance = 0
        while balance < penalty:
            print(f"Need {penalty - balance} more")
            payment = float(input("Enter paid amount: $"))
            balance += payment
        print(f"Payment success. Your change is ${balance - penalty:.2f}")

        c.execute('UPDATE CREDENTIALS SET PENALTY=0 WHERE NAME=?',(username,))
        conn.commit()
    if user == "ADMIN":
        adminFeature()
    else:
        studentFeature()

def selcpaymtd(penalty, user, username):
    process = int(input("[1]Pay your penalty \n[2]Exit \nEnter your choice: "))
    while process not in [1, 2]:
        process = int(input("Input invalid, enter again \n[1]Pay your penalty \n[2]Exit \nEnter your choice: "))
    if process == 1:
        print("Select your payment method")
        if user == "ADMIN":
            select = int(input("[1]Card \n[2]Ewallet \n[3]Cash \nEnter your choice: "))
            while select not in [1,2,3]:
                select = int(input("Input invalid, enter again \n[1]Card \n[2]Ewallet \n[3]Cash \nEnter your choice: "))
        else:
            select = int(input("[1]Card \n[2]Ewallet \nEnter your choice: "))
            while select not in [1,2]:
                select = int(input("Input invalid, enter again \n[1]Card \n[2]Ewallet \nEnter your choice: "))
        if select == 1:
            Card(penalty, user, username)
        elif select == 2:
            eWallet(penalty, user, username)
        elif select == 3:
            Cash(penalty,user,username)
            
    elif process == 2:
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()

def BorrowBook(x):
    if x == 1:
        username = input("Enter username:")
        c.execute('SELECT NAME FROM CREDENTIALS WHERE NAME=?',(username,))
        result = c.fetchone()
        #print(username)
        while result == None:
            print("Username not found in database.")
            username = input("Enter username:")
            c.execute('SELECT NAME FROM CREDENTIALS WHERE NAME=?',(username,))
            result = c.fetchone()

        c.execute('SELECT PENALTY from CREDENTIALS WHERE NAME=?',(result[0],))
        penalty = c.fetchone()[0]

    elif x == 0:
        c.execute('SELECT PENALTY from CREDENTIALS WHERE NAME=?',(user,))
        penalty = c.fetchone()[0]

    if penalty != 0 :
        print(f"Currrently your status is not available, pay your penalty first to borrow books. \nThe amount you need to pay is: RM{penalty}")
        selcpaymtd(penalty, user, username)
    else:
        qty = 0
        count = 0
        amt = 0
        data = []
        while qty <= 0 or qty >= 4:
            qty = int(input("Input amount of book u want to borrow maximum 3: "))

        while count < qty:
            #select the book u want
            bookMau = input("Input book ID that u want to borrow: ")
            c.execute('SELECT ID FROM BOOKS where ID=?',(bookMau,))
            id = c.fetchone()
            num = c.execute('SELECT AMOUNT FROM BOOKS WHERE ID=?',(bookMau,))
            for row in num:
                amt = int(row[0])
            while id==None or amt<=0:
                print("Book is not available. Please enter a valid book ID ")
                bookMau = input("Input book ID that u want to borrow or press 'n' back to menu: ")
                if bookMau == 'n':
                    if user == "ADMIN":
                        adminFeature()
                    else:
                        studentFeature()
                else:
                    bookMau = int(bookMau)
                    c.execute('SELECT TITLE FROM BOOKS where ID=?',(bookMau,))
                    id = c.fetchone()
                    num = c.execute('SELECT AMOUNT FROM BOOKS WHERE ID=?',(bookMau,))
                    for row in num:
                        amt = int(row[0])

            #get book title
            book = c.execute('SELECT * from BOOKS WHERE ID=?', (bookMau,))
            for row in book:
                title = row[1]
                data.append(row)
            listing(data)

            decn=input("comfirm? press any key to continue, press 'n' back to menu: ")
            if decn=='n' :
                if user == "ADMIN":
                    adminFeature()
                else:
                    studentFeature()
            else:
                #create borrow datetime
                now = datetime.now().strftime("%Y-%m-%d")
            
                #create expried datetime
                expDate = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

                #update amount left into BOOKS.db & insert data into LIST.db
                c.execute('UPDATE BOOKS SET AMOUNT=AMOUNT-? WHERE ID=?',(1,bookMau,))

                if x==0:
                    c.execute('INSERT INTO LIST (ID, TITLE, BORROWEDBY, BORROWEDDATE, EXPIREDDATE, COLLECT) VALUES(?, ?, ?, ?, ?, ?)', (bookMau, title, user, now, expDate, x,))
                elif x==1:
                    c.execute('INSERT INTO LIST (ID, TITLE, BORROWEDBY, BORROWEDDATE, EXPIREDDATE, COLLECT) VALUES(?, ?, ?, ?, ?, ?)', (bookMau, title, username, now, expDate, x,))
                    
                conn.commit()
                count += 1
        print('borrow successful')
        if user == "ADMIN":
            adminFeature()
        else:
            studentFeature()

def ReturnListing(list):
    headers = ["ID","Title","Borrowed by","Borrowed date","Return date","Collect"]
    print(tabulate(list, headers = headers, tablefmt = "outline"))

def CollectBook():
    # Read table where collect = 0
    list = []
    c.execute("SELECT * from LIST WHERE COLLECT = ?",(0,))
    record = c.fetchall()
    #USE tabulate
    for row in record:
        list.append(row)
    ReturnListing(list)

    book = c.execute("SELECT ID from LIST WHERE COLLECT = ?",(0,))
    books = book.fetchall()
    if books == []:
        print('No books to be collected')
        adminFeature()

    else:
        user_input = int(input('Press [1] to proceed; Press [2] to cancel: '))
        while user_input not in [1,2]:
            print('Invalid input, please try again.')
            user_input = int(input('Press [1] to proceed; Press [2] to cancel: '))
        if user_input == 2:
            #Back to admin menu (X)
            adminFeature()
        elif user_input == 1:
            # Change collect into 1
            book_id = int(input('Enter book ID: '))
            book = c.execute("SELECT ID from LIST WHERE COLLECT = ?",(0,))
            books = book.fetchall()
            while (book_id,) not in books:
                print("Invalid")
                book_id = int(input('Enter book ID: '))
        c.execute('UPDATE LIST SET COLLECT = ? WHERE ID = ?',(1,book_id,))
        conn.commit()
        print('Update completed.')
    cnt = str(input("continue? y/n: "))
    while cnt not in ['y', 'n']:
        cnt = str(input("Input invalid, input again \ncontinue? y/n: "))
    if cnt == 'y':
        CollectBook()
    elif cnt == 'n':
        adminFeature()

def ReturnBook(): 
    penalty = 0
    count = 0
    data = c.execute('SELECT * FROM LIST')
    for x in data:
        count = count + 1
    rtnAmt = int(input('Enter how many books u want to return: '))
    while rtnAmt > count:
        print("the amount u input is not valid")
        rtnAmt = int(input('Enter how many books u want to return: '))
    for count in range (1, rtnAmt+1, 1):
        rtnBookID = int(input('Enter book ID that u want to return: '))
        c.execute('SELECT ID FROM LIST WHERE ID=?',(rtnBookID,))
        id = c.fetchone()
        while id == None:
            print("input invalid, input again")
            rtnBookID = int(input('Enter book ID that u want to return: '))
            c.execute('SELECT ID FROM LIST WHERE ID=?',(rtnBookID,))
            id = c.fetchone()

        c.execute('SELECT BORROWEDBY FROM LIST WHERE ID=?',(rtnBookID,))
        brwer = c.fetchone()[0]

        c.execute("SELECT EXPIREDDATE from LIST WHERE ID=?",(rtnBookID,))
        ExpriredDate = c.fetchone()[0]
    
        now = datetime.now()
        #convert to object
        Exprired_date = datetime.strptime(ExpriredDate, "%Y-%m-%d")

        #date diff
        dateDiff = (now - Exprired_date).days
        if dateDiff > 0:
            penalty = penalty + (dateDiff*1)

        #AMOUNT + 1
        c.execute('UPDATE BOOKS SET AMOUNT=AMOUNT+? WHERE ID=?',(1,rtnBookID,))
        conn.commit()

        #delete data in LIST after the people return the book
        c.execute('DELETE from LIST WHERE ID=?;',(rtnBookID,))
        conn.commit()

        print("return successful")
    #update credentials penalty database
    c.execute('UPDATE CREDENTIALS SET PENALTY=PENALTY+? WHERE NAME=?',(penalty, brwer))
    conn.commit()

def edit_credential(): 
    choices = int(input("Edit: \n[1]Name \n[2]Password \n[3]Phone \n[4]Email \nEnter choice: "))
    while choices not in [1,2,3,4]:
        print('Invalid input.')
        choices = int(input("Edit: \n[1]Name \n[2]Password \n[3]Phone \n[4]Email \nEnter choice: "))
    if choices == 1:
        choice = "NAME"  
        value = str(input("Enter name: "))
        fetch  = c.execute('SELECT NAME from CREDENTIALS WHERE NAME=?', (value,))
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

    c.execute(f"UPDATE CREDENTIALS set {choice}=? WHERE NAME=?", (value, user))
    print("Edit successfully. ")
    conn.commit()
    studentFeature()
            
def edit_book():
    books = c.execute(f"SELECT * FROM BOOKS")
    everything = []
    for x in books:
        everything.append(x)
    listing(everything)
    id = int(input("Enter id of the book to be edited: "))
    ids = c.execute(f"SELECT ID FROM BOOKS")
    idss = ids.fetchall()
    while (id,) not in idss:
        print("Invalid")
        listing(everything)
        id = int(input("Enter id of the book to be edited: "))
    ori_id = id
    books = c.execute(f"SELECT * FROM books WHERE ID={id}")
    data = []
    for x in books:
        data.append(x)
    listing(data)
    old_title = data[0][1]
    choice_input = int(input("\nEdit: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Fiction \n[7]Amount \n[8]Publisher \n[9]Back to menu \nEnter your choice: "))
    while choice_input < 1 or choice_input > 8:
        choice_input = int(input("\nEdit: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Fiction \n[7]Amount \n[8]Publisher \n[9]Back to menu \nEnter your choice: "))
    if choice_input == 1:
        title = str(input("Edit title: "))
        c.execute(f"UPDATE BOOKS SET TITLE = '{title}' WHERE TITLE = ?", (old_title,))
    elif choice_input == 2:
        author = str(input("Edit author: "))
        c.execute(f"UPDATE BOOKS SET AUTHOR = '{author}' WHERE TITLE = ?", (old_title,))
    elif choice_input == 3:
        year = int(input("Edit year: "))
        c.execute(f"UPDATE BOOKS SET YEAR = {year} WHERE TITLE = ?", (old_title,))
    elif choice_input == 8:
        publisher = str(input("Edit publisher: "))
        c.execute(f"UPDATE BOOKS SET PUBLISHER = '{publisher}' WHERE TITLE = ?", (old_title,))
    elif choice_input == 9:
        adminFeature()
    elif choice_input == 4:
        catlist = ['Literature', 'Encyclopedia', 'Guidlines', 'Motivations', 'Dictionary', 'History', 'News', 'Others']
        category = int(input("Edit category: \n[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
        categ = catlist[category-1]
        index = int(0)
        id_editor(id, ori_id, old_title, index, category)
        c.execute(f"UPDATE BOOKS SET CATEGORY = '{categ}' WHERE TITLE = ?", (old_title,))
    elif choice_input == 5:
        langlist = ['English', 'Malay', 'Chinese', 'Tamil', 'Others']
        langChoice = int(input("Edit language: \n[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: "))
        while langChoice == '':
            print("Invalid")
            langChoice = int(input("Edit language: \n[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: "))
        lang = langlist[langChoice-1]
        index = int(1)
        id_editor(id, ori_id, old_title, index, langChoice)
        c.execute(f"UPDATE BOOKS SET LANGUAGE = '{lang}' WHERE TITLE = ?", (old_title,))
    elif choice_input == 6:
        ficChoice = input("Edit fiction: \n[1]Fiction\n[2]Non-fiction\nEnter choice: ")
        while ficChoice not in ('1', '2'):
            print("Invalid")
            ficChoice = input("Edit fiction \n[1]Fiction\n[2]Non-fiction\nEnter choice: ")
        index = int(2)
        id_editor(id, ori_id, old_title, index, ficChoice)
        if ficChoice == '1':
            fict = str("Fiction")
        else:
            fict = str("Non-fiction")
        c.execute(f"UPDATE BOOKS SET FICTION = '{fict}' WHERE TITLE = ?", (old_title,))
    elif choice_input == 7:
        ids = []
        select_title = c.execute(f"SELECT TITLE FROM BOOKS WHERE ID={id}")
        seltitle = select_title.fetchone()
        for x in seltitle:
            y = x
        find_amount = c.execute(f"SELECT ID FROM BOOKS WHERE TITLE='{y}'")
        for x in find_amount:
            ids.append(x)
        amount = len(ids)
        print(f"The amount is {amount}")
        new_amount = int(input("Change to: "))
        if new_amount < amount:
            minus_amount = amount - new_amount
            i = 1
            while i <= minus_amount:
                largest = max(ids)
                largest = int(largest[0])
                ids.pop(len(ids)-1)
                c.execute(f"DELETE FROM BOOKS WHERE ID={largest}")
                i += 1
            conn.commit()
        else:
            add_amount = new_amount - amount
            get_details(id, add_amount)
    conn.commit()

def get_details(id, add_amount):
    details = []
    book = c.execute(f"SELECT * FROM BOOKS WHERE ID={id}")
    for x in book:
        details.append(x)
    id = str(id)
    splited = [*id]
    catChoice = splited[0]
    langChoice = splited[1]
    ficChoice = splited[2]
    idf(catChoice, langChoice, ficChoice)
    title = details[0][1]
    author = details[0][2]
    category = details[0][3]
    language = details[0][4]
    fiction = details[0][5]
    amount = add_amount
    price = details[0][7]
    publisher = details[0][8]
    year = details[0][9]
    commitf(index, title, author, category, language, fiction, amount, price, publisher, year,)

def id_editor(id, ori_id, title, index, value):
    id = str(id)
    splited = [*id]
    splited[6] = '1'
    del splited[index]
    splited.insert(index, str(value))
    new_id = "".join(splited)
    new_id = int(new_id)
    result = c.execute("SELECT ID FROM BOOKS")
    for y in result:
        if y[0] == new_id:
            new_id += 1
        else:
            new_id = new_id
    find_title = c.execute("SELECT TITLE FROM BOOKS")
    amount = 1
    for x in find_title:
        if x[0] == title:
            amount += 1
    id = new_id
    print(id)
    print(amount)
    if int(amount) > 1:
        for i in range (1, int(amount) + 1):
            c.execute(f"UPDATE BOOKS SET ID={id} WHERE ID ={ori_id}")
            conn.commit()
            id = int(id)
            id += 1
            ori_id += 1
            print(id)
            print(ori_id)   
    else:
        c.execute(f"UPDATE BOOKS SET ID={id} WHERE ID ={ori_id}")
        conn.commit()

    print("ID has been updated. ")

def main():
    global user
    login = False
    choice = input("[1]Login \n[2]Sign Up \n[3]End \nEnter your choice: ")
    if choice == '1':
        name = str(input("Enter username: "))
        pwd = str(input("Enter password: "))
        login  = checklogin(name, pwd)
        if login == True:
            print("Login successful. ")
            print("Welcome", name)
            user = name
        else:
            print("Username or password incorrect. ")
            main()
            quit()
    elif choice == '2':
        signUp()
    elif choice == '3':
        quit()
    else:
        main()
        quit()

    if user == 'ADMIN':
        adminFeature()
    else:
        studentFeature()

def studentFeature():
    print("[1]Search Book \n[2]View status \n[3]Edit user Details \n[4]Log Out")
    choice = int(input("Enter your choice:"))
    if choice == 1:
        searchBook()
    elif choice == 2:
        status = c.execute("SELECT * from CREDENTIALS WHERE NAME=?",(user,))
        for row in status:
            print('Name: ',row[0])
            print('Phone: ',row[2])
            print('Email: ',row[3])
            print('Penalty: ',row[4])
            penalty = row[4]
            print('-----------')
            if penalty != 0:
                selcpaymtd(penalty,user, user)
            else:
                studentFeature()
    elif choice == 3:
        edit_credential()
    else:
        main()
        quit()

def adminFeature():
    print("[1]Add book \n[2]Search book \n[3]Borrow Books \n[4]View Books To collect \n[5]Return Books \n[6]Edit books \n[7]Log out")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        addBooks()
    elif choice == 2:
        searchBook()
    elif choice == 3:
        BorrowBook(1)
    elif choice == 4:
        CollectBook()
    elif choice == 5:
        ReturnBook()
    elif choice == 6:
        edit_book()                
    else:
        main()
        quit()
    adminFeature()

#main
main()
conn.close()
