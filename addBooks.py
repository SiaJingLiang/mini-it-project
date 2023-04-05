import sqlite3
conn = sqlite3.connect('books.db')
c = conn.cursor()

    #id:done
    #title:done
    #author:done
    #category:done
    #amount:done
    #amountleft:deleted
    #price:done
    #dateadded:deleted

def titlef():
    global title
    title = str(input("Title: "))
    while title == '':
        print("Invalid")
        title = str(input("Title: "))

def categoryf():
    global category, catChoice, ficChoice, langChoice
    categoryList =['literature', 'encyclopedia', 'guidlines', 'motivations', 'dictionary', 'history', 'news', 'others']
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
    while price == '' or price.isdigit() == False:
        print("Invalid")
        price = input("Enter price: RM")

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
    if ficChoice == 1:
        fiction = str("Fiction")
    else:
        fiction = str("Non-fiction")

def commitf(id, title, author, category, language, fiction, amount, price, publisher,):
    if int(amount) > 1:
        for i in range (1, int(amount) + 1):
            c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, title, author, category, language, fiction, amount, price, publisher,))
            id = int(id) + 1
    else:
        c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, title, author, category, language, fiction, amount, price, publisher,))
    conn.commit()
    
def idf(catChoice, langChoice, ficChoice):
    #id = category, language, fiction, index
    global id
    catChoice = str(catChoice)
    langChoice = str(langChoice)
    ficChoice = str(ficChoice)
    x = (catChoice + langChoice + ficChoice + "0001")
    row = c.execute("SELECT * FROM BOOKS")
    if row.fetchone() == None:
        id = str(x)
    elif len(row.fetchall()) >= 1:
        h = (catChoice + langChoice + ficChoice + "0001")
        h = int(h)
        result = c.execute("SELECT ID FROM BOOKS")
        for y in result:
            if y[0] == h:
                h += 1
        id = (catChoice + langChoice + ficChoice + str(h.zfill(4)))

def publisherf():
    global publisher
    publisher = str(input("Enter publisher: "))
    while publisher == "":
        print("Invalid")
        publisher = str(input("Enter publisher: "))

c.execute('''CREATE TABLE IF NOT EXISTS BOOKS 
                (ID INT NOT NULL,
                TITLE TEXT PRIMARY KEY NOT NULL,
                AUTHOR TEXT,
                CATEGORY TEXT NOT NULL,
                LANGUAGE TEXT NOT NULL,
                FICTION TEXT NOT NULL, 
                AMOUNT INT NOT NULL,
                PRICE REAL NOT NULL, 
                PUBLISHER TEXT NOT NULL);''')
   
def addBooks():
    titlef()
    categoryf()
    amountf()
    pricef()
    authorf()
    idf(catChoice, langChoice, ficChoice)
    publisherf()
    print(title, category, fiction, language, amount, price, author, id, publisher)
    commitf(id, title, author, category, language, fiction, amount, price, publisher)

#addBooks()
conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('SELECT * FROM BOOKS')
print(len(c.fetchall()))
table = c.execute('SELECT * from BOOKS')
for x in table:
    print(x)
