import sqlite3
from datetime import datetime, timedelta
conn = sqlite3.connect('database.db')
c = conn.cursor()
conne = sqlite3.connect('books.db')
b = conne.cursor()
global userName
userName = 'user1'

def addBooks():
#later replace with xiangze
    categoryList =['literature', 'encyclopedia', 'guidlines', 'motivations', 'dictionary', 'history', 'news', 'others']
    b.execute('''CREATE TABLE IF NOT EXISTS BOOKS 
                    (ID           INT  PRIMARY KEY NOT NULL, 
                     TITLE        TEXT             NOT NULL,
                     AUTHOR       TEXT,
                     CATEGORY     TEXT             NOT NULL, 
                     AMOUNT       INT              NOT NULL,
                     AMOUNTLEFT   INT,
                     PRICE        REAL             NOT NULL)''')
    fetch = b.execute('SELECT ID from BOOKS WHERE ID=?',(1,))
    if fetch.fetchone() == None:
        b.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, AMOUNT, AMOUNTLEFT, PRICE)\
            VALUES('1', 'G101', 'LOGITECH', 'MOUSE', 100, 100, 100.5) ");
        b.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, AMOUNT, AMOUNTLEFT, PRICE)\
            VALUES('2', 'G102', 'LOGITECH', 'MOUSE', 100, 100, 100.5) ");
        conne.commit()

#show all books
def showBook():
#later replace with shun hong
    cursor = b.execute("SELECT * from BOOKS")
    for row in cursor:
        print (row)
  
def BorrowBook():
    list = []
    qty = 0
    count = 0
    user = "user1"
    while qty <= 0 or qty >= 4:
        qty = int(input("input amount of book u want to borrow maximum 3: "))
    while count < qty:
        bookMau = int(input("input book ID that u want to borrow: "))
        list.append(bookMau)

        now = datetime.datetime.now()
        time = now.strftime("%d-%m-%Y %H:%M:%S")
        c.execute('UPDATE BOOKS SET AMOUNTLEFT=AMOUNTLEFT-?, BORROWEDDATE=?, BORROWEDBY=? WHERE ID=?',(1,time,user,bookMau,));
        c.execute("UPDATE BOOKS SET BORROWEDDATE=? || 'updated' WHERE ID=?",(time,bookMau))
        conn.commit()
        count += 1

    cursor = conn.execute("SELECT * from BOOKS") 
    for row in cursor:
        print(row)

def BorrowBook():
    c.execute('''CREATE TABLE IF NOT EXISTS LIST
                    (ID           INT       NOT NULL, 
                     TITLE        TEXT      NOT NULL,
                     BORROWEDBY   TEXT      NOT NULL,  
                     BORROWEDDATE TIMESTAMP NOT NULL,
                     EXPIREDDATE  TIMESTAMP NOT NULL, 
                     COLLECT      INT       NOT NULL)''')
    
    qty = 0
    count = 0
    while qty <= 0 or qty >= 4:
        qty = int(input("input amount of book u want to borrow maximum 3: "))

    while count < qty:
        #select the book u want
        bookMau = int(input("input book ID that u want to borrow: "))
        #get book title
        title = b.execute('SELECT * from BOOKS WHERE ID=?', (bookMau,))
        for bookName in title:
            title = bookName[1]

        #create borrow datetime
        now = datetime.now().strftime("%Y-%m-%d")
        #time = datetime.strptime(now, "%Y-%m-%d")

        #create expried datetime
        expDate = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        #expdate = datetime.strptime(expDate, "%Y-%m-%d")

        #update amount left into BOOKS.db & insert data into LIST.db
        b.execute('UPDATE BOOKS SET AMOUNTLEFT=AMOUNTLEFT-? WHERE ID=?',(1,bookMau,))
        c.execute('INSERT INTO LIST (ID, TITLE, BORROWEDBY, BORROWEDDATE, EXPIREDDATE, COLLECT) VALUES(?, ?, ?, ?, ?, ?)', (bookMau, title, userName, now, expDate, 1))

        conne.commit()
        conn.commit()
        count += 1
    print('borrow successful')

def ReturnBook(): 
    penalty = 0
    rtnAmt = int(input('Enter how many books u want to return: '))
    for count in range (1, rtnAmt+1, 1):
        rtnBookID = int(input('Enter book ID that u want to return: '))

        c.execute("SELECT EXPIREDDATE from LIST WHERE ID=?",(rtnBookID,))
        ExpriredDate = c.fetchone()[0]
    
        now = datetime.now()
        #convert to object
        Exprired_date = datetime.strptime(ExpriredDate, "%Y-%m-%d")

        #date diff
        dateDiff = (now - Exprired_date).days
        if dateDiff > 0:
            penalty = penalty + (dateDiff*1)

        #AMOUNTLEFT + 1
        b.execute('UPDATE BOOKS SET AMOUNTLEFT=AMOUNTLEFT+? WHERE ID=?',(1,rtnBookID,))
        conne.commit()

        #delete data in LIST after the people return the book
        c.execute('DELETE from LIST WHERE ID=?;',(rtnBookID,))
        conn.commit()

    #update credentials penalty database
    c.execute('UPDATE CREDENTIALS SET PENALTY=PENALTY+? WHERE NAME=?',(penalty, userName))
    conn.commit()
    print(penalty)

