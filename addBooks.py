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
                YEAR INT);''')

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
    while catChoice < 1 or catChoice > 9:
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
    if ficChoice == 1:
        fiction = str("Fiction")
    else:
        fiction = str("Non-fiction")

def commitf(index, title, author, category, language, fiction, amount, price, publisher, year,):
    amountl = int(1)
    if int(amount) > 1:
        for i in range (1, int(amount) + 1):
            c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, title, author, category, language, fiction, amountl, price, publisher, year,))
            conn.commit()
            index = int(index) + 1   
    else:
        c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PRICE, PUBLISHER, YEAR) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (index, title, author, category, language, fiction, amountl, price, publisher, year,))
        conn.commit()
    print("Book has been added. ")
    c.close()
    conn.close()
    
def idf(catChoice, langChoice, ficChoice):
    #id = category, language, fiction, index
    global index
    catChoice = str(catChoice)
    langChoice = str(langChoice)
    ficChoice = str(ficChoice)
    x = (catChoice + langChoice + ficChoice + "0001")
    row = c.execute("SELECT * FROM BOOKS")
    rows = c1.execute("SELECT * FROM BOOKS")
    if row.fetchone() == None:
        index = str(x)
    elif len(rows.fetchall()) >= 1:
        h = (catChoice + langChoice + ficChoice + "0001")
        h = int(h)
        result = c.execute("SELECT * FROM BOOKS")
        for y in result:
            if y[0] == h:
                h += 1
        h = str(h)
        index = str(h.zfill(4))

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
