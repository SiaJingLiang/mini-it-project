import sqlite3
from datetime import datetime, timedelta
conn = sqlite3.connect('books.db')
con = sqlite3.connect('list.db')
c = conn.cursor()
d = con.cursor()

def addBooks():
    categoryList =['literature', 'encyclopedia', 'guidlines', 'motivations', 'dictionary', 'history', 'news', 'others']
    c.execute('''CREATE TABLE IF NOT EXISTS BOOKS 
                    (ID           INT  PRIMARY KEY NOT NULL, 
                     TITLE        TEXT             NOT NULL,
                     AUTHOR       TEXT,
                     CATEGORY     TEXT             NOT NULL, 
                     AMOUNT       INT              NOT NULL,
                     AMOUNTLEFT   INT,
                     PRICE        REAL             NOT NULL)''')
    fetch = c.execute('SELECT ID from BOOKS WHERE ID=?',(1,))
    if fetch.fetchone() == None:
        c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, AMOUNT, AMOUNTLEFT, PRICE)\
            VALUES('1', 'G101', 'LOGITECH', 'MOUSE', 100, 100, 100.5) ");
        c.execute("INSERT INTO BOOKS (ID, TITLE, AUTHOR, CATEGORY, AMOUNT, AMOUNTLEFT, PRICE)\
            VALUES('2', 'G102', 'LOGITECH', 'MOUSE', 100, 100, 100.5) ");
        conn.commit()
    
def showBook():
    #show all books
    cursor = c.execute("SELECT * from BOOKS")
    for row in cursor:
        print (row)

#borrow book and booking the book#
#update time manualy
  
def BorrowBook():
    d.execute('''CREATE TABLE IF NOT EXISTS LIST
                    (ID           INT       NOT NULL, 
                     TITLE        TEXT      NOT NULL,
                     BORROWEDBY   TEXT      NOT NULL,  
                     BORROWEDDATE TIMESTAMP NOT NULL,
                     EXPIREDDATE  TIMESTAMP NOT NULL,
                     RETURNDATE   TIMESTAMP)''')

    qty = 0
    count = 0
    user = "user1"
    while qty <= 0 or qty >= 4:
        qty = int(input("input amount of book u want to borrow maximum 3: "))
    while count < qty:
        #select the book u want
        bookMau = int(input("input book ID that u want to borrow: "))
        #get book title
        title = conn.execute('SELECT * from BOOKS WHERE ID=?', (bookMau,))
        for bookName in title:
            title = bookName[1]

        #create borrow datetime
        now = datetime.now().strftime("%Y-%m-%d")
        #time = datetime.strptime(now, "%Y-%m-%d")

        #create expried datetime
        expDate = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
        #expdate = datetime.strptime(expDate, "%Y-%m-%d")

        #update amount left into BOOKS.db & insert data into LIST.db
        c.execute('UPDATE BOOKS SET AMOUNTLEFT=AMOUNTLEFT-? WHERE ID=?',(1,bookMau,))
        d.execute('INSERT INTO LIST (ID, TITLE, BORROWEDBY, BORROWEDDATE, EXPIREDDATE) VALUES(?, ?, ?, ?, ?)', (bookMau, title, user, now, expDate,))

        conn.commit()
        con.commit()
        count += 1

    print('borrow successful')
    cursor = d.execute("SELECT * from LIST") 
    for row in cursor:
        print('The data of the book you borrowed.')
        print(row)

def ReturnBook(): 
    penalty = 0
    rtnAmt = int(input('Enter how many books u want to return: '))
    for count in range (1, rtnAmt+1, 1):
        rtnBookID = int(input('Enter book ID that u want to return: '))

        d.execute("SELECT BORROWEDDATE, EXPIREDDATE from LIST WHERE ID=?",(rtnBookID,))
        BorrowDate, ExpriredDate = d.fetchone()
        #convert to object
        Borrow_date = datetime.strptime(BorrowDate, "%Y-%m-%d")
        Exprired_date = datetime.strptime(ExpriredDate, "%Y-%m-%d")
        #date diff
        dateDiff = (Exprired_date - Borrow_date).days
        print(dateDiff)
        if dateDiff > 7:
            penalty = penalty + ((dateDiff-7)*1)
    print(penalty)

addBooks()
showBook()
BorrowBook()
ReturnBook()

