import sqlite3
conn = sqlite3.connect('books.db')
c = conn.cursor()

    #id:done
    #title:done
    #author:done
    #category:done
    #amount:done
    #amountleft:done
    #price:done
    #dateadded:done

def title():
    title = input("Title: ")
    fetch = c.execute('SELECT TITLE from BOOKS WHERE TITLE=?', (title,))
    if fetch.fetchone() != None:
        choice = str(input("Book exists, do you want to increase amount only? y/n "))
        while choice not in ('y', 'n'):
            print("Input invalid. ")
            choice = str(input("Book exists, do you want to increase amount only? y/n ")) 
        if choice == "y":
            find = c.execute('SELECT * from BOOKS WHERE TITLE=?', (title))
            for row in find:
                amount = row[3]
                print("Amount is", amount)
                newAmount = input("Enter amount to be added: ")
                confirmation = input("Enter again: ")
                while newAmount != confirmation:
                    print("Invalid")
                    newAmount = input("Enter amount to be added: ")
                    confirmation = input("Enter again: ")
                amount += newAmount
            c.execute("UPDATE BOOKS set AMOUNT = ? WHERE TITLE = ?", (amount, title))
            conn.commit()
            print("Amount is now " + amount)
            quit()
        elif choice == "n":
            print("Menu")
            quit()
    else:
        return title

def category():
    categoryList =['literature', 'encyclopedia', 'guidlines', 'motivations', 'dictionary', 'history', 'news', 'others']
    catChoice = int(input("[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
    while catChoice < 1 or catChoice >9:
        print("Input invalid. ")
        catChoice = int(input("[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
    category = categoryList[catChoice-1]
    ficChoice = fiction()
    langChoice = language()
    return category, catChoice, ficChoice, langChoice

def amount():
    amount = input("Enter amount: ")
    while amount == '' or int(amount) <= 0 or amount.isdigit() == False:
        print("Invalid")
        amountleft = amount
    return amount, amountleft

def price():
    price = input("Enter price: RM")
    while price == '' or price.isdigit() == False:
        print("Invalid")
        price = input("Enter price: RM")
    return price

def author():
    author = str(input("Enter author: "))
    return author

def language():
    langChoice = input("[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: ")
    while langChoice == '' or langChoice.isdigit() == False or langChoice < 1 or langChoice > 5:
        print("Invalid")
        langChoice = input("[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: ")
    return langChoice

def fiction():
    ficChoice = input("[1]Fiction\n[2]Non-fiction\nEnter choice: ")
    while ficChoice not in ('1', '2'):
        print("Invalid")
        ficChoice = input("[1]Fiction\n[2]Non-fiction\nEnter choice: ")
    ficChoice = int(ficChoice)
    return ficChoice
    

def date():
    today = c.execute("SELECT DATE ('now')")
    for x in today:
        date = x[0]
    return date

def confirmation(title, category, catChoice, ficChoice, langChoice, amount, amountleft, price, author, date, id):
    c.execute('''CREATE TABLE IF NOT EXISTS BOOKS 
                (ID INT NOT NULL,
                TITLE TEXT PRIMARY KEY NOT NULL,
                AUTHOR TEXT,
                CATEGORY TEXT NOT NULL, 
                AMOUNT INT NOT NULL,
                AMOUNTLEFT INT NOT NULL,
                PRICE REAL NOT NULL,
                DATEADDED TEXT NOT NULL, 
                BORROWEDBY TEXT,
                BORROWEDDATE TEXT,
                RETURNDATE TEXT);''')
    title = title()
    category, catChoice, ficChoice, langChoice = category()
    amount, amountleft = amount()
    price = price()
    author = author()
    confirmation = str(input("Do you want to make any changes? y/n "))
    while confirmation not in ('y', 'n') or confirmation == '':
        print("Invalid")
        confirmation = str(input("Do you want to make any changes? y/n "))
    if confirmation == 'y':
        selection = input("[1]Title\n[2]Author\n[3]Category\n[4]Amount\n[5]Price\n[6]Cancel adding\nEnter choice: ")
        while selection.isdigit() == False or int(selection) < 1 or int(selection) > 6:
            selection = input("[1]Title\n[2]Author\n[3]Category\n[4]Amount\n[5]Price\n[6]Cancel adding\nEnter choice: ")
        if selection == 1:
            title = title()
        elif selection == 2:
            author = author()
        elif selection == 3:
            category, catChoice, ficChoice, langChoice = category()
        elif selection == 4:
            amount, amountleft = amount()
        elif selection == 5:
            price = price()
        elif selection == 6:
            print("Menu")
            quit()
    date = date()
    id = id(catChoice, langChoice, ficChoice)
    c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, AMOUNT, AMOUNTLEFT, PRICE, DATEADDED) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (id, title, author, category, amount, amountleft,price, date,))
    conn.commit()
    
def id(catChoice, langChoice, ficChoice):
    #id = category, language, fiction, index
    catChoice = str(catChoice)
    langChoice = str(langChoice)
    ficChoice = str(ficChoice)
    index = int(c.execute("SELECT COUNT(*) FROM BOOKS"))
    if index == 0:
        index = 1
    index = str(index)
    index = str(index.zfill(4))
    id = (catChoice + langChoice + ficChoice + index)
    return id

def addBooks():
    title = title()
    category, catChoice, ficChoice, langChoice = category()
    amount, amountleft = amount()
    price = price()
    author = author()
    title, category, catChoice, ficChoice, langChoice, amount, amountleft, price, author, date, id = confirmation(title, category, catChoice, ficChoice, langChoice, amount, amountleft, price, author, date, id)
   
addBooks()
conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('SELECT * FROM BOOKS')
print(len(c.fetchall()))
table = c.execute('SELECT * from BOOKS')
for x in table:
    print(x)
