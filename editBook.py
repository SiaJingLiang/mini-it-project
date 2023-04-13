from tabulate import tabulate
import sqlite3
conn = sqlite3.connect('books.db')
c = conn.cursor()

def edit_book():
    id = int(input("Enter id of the book to be edited: "))
    ori_id = id
    books = c.execute(f"SELECT * FROM books WHERE ID={id}")
    headers = ["ID", "TITLE", "AUTHOR", "CATEGORY", "LANGUAGE", "FICTION", "AVAILABILITY", "PRICE", "PUBLISHER", "YEAR"]
    data = []
    for x in books:
        data.append(x)
    print(tabulate(data, headers=headers, tablefmt="outline"))
    choice_input = int(input("\nEdit: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Fiction \n[7]Amount \n[8]Publisher \n[9]Back to menu \nEnter your choice: "))
    while choice_input < 1 or choice_input > 8:
        choice_input = int(input("\nEdit: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Fiction \n[7]Amount \n[8]Publisher \n[9]Year \n[10]Back to menu \nEnter your choice: "))
    if choice_input == 1:
        title = str(input("Edit title: "))
        c.execute(f"UPDATE BOOKS SET TITLE = '{title}' WHERE ID = {id}")
    elif choice_input == 2:
        author = str(input("Edit author: "))
        c.execute(f"UPDATE BOOKS SET AUTHOR = '{author}' WHERE ID = {id}")
    elif choice_input == 3:
        year = int(input("Edit year: "))
        c.execute(f"UPDATE BOOKS SET YEAR = {year} WHERE ID = {id}")
    elif choice_input == 8:
        publisher = int(input("Edit publisher: "))
        c.execute(f"UPDATE BOOKS SET YEAR = {publisher} WHERE ID = {id}")
    elif choice_input == 9:
        menu()
    elif choice_input == 4:
        find_title = c.execute(f"SELECT TITLE FROM BOOKS WHERE ID = {id}")
        for x in find_title:
            title = x[0]
        print(title)
        category = int(input("Edit category: \n[1]Literature\n[2]Encyclopedia\n[3]Guidlines\n[4]Motivations\n[5]Dictionary\n[6]History\n[7]News\n[8]Others\nEnter choice: "))
        index = int(0)
        id_editor(id, ori_id, title, index, category)
    elif choice_input == 5:
        langChoice = int(input("Edit language: \n[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: "))
        while langChoice == '':
            print("Invalid")
            langChoice = int(input("Edit language: \n[1]English\n[2]Malay\n[3]Chinese\n[4]Tamil\n[5]Others\nEnter choice: "))
        index = int(1)
        id_editor(id, ori_id, title, index, langChoice)
    elif choice_input == 6:
        ficChoice = input("Edit fiction: \n[1]Fiction\n[2]Non-fiction\nEnter choice: ")
        while ficChoice not in ('1', '2'):
            print("Invalid")
            ficChoice = input("Edit fiction \n[1]Fiction\n[2]Non-fiction\nEnter choice: ")
        index = int(2)
        id_editor(id, ori_id, title, index, ficChoice)
    elif choice_input == 7:
        ids = []
        select_title = c.execute(f"SELECT TITLE FROM BOOKS WHERE ID={id}")
        find_amount = c.execute(f"SELECT ID FROM BOOOKS WHERE TITLE={select_title}")
        for x in find_amount:
            ids.append(x)
        amount = len(ids)
        print(f"The amount is {amount}")
        new_amount = int(input("Change to: "))
        if new_amount < amount:
            minus_amount = new_amount - amount
            i = 1
            while i < minus_amount:
                largest = max(ids)
                ids.pop(largest)
                c.execute(f"DELETE FROM BOOKS WHERE ID={largest}")
                i += 1
            conn.commit()
        else:
            add_amount = amount - new_amount
            get_details(id, add_amount)

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
    index = idf(catChoice, langChoice, ficChoice)
    title = details[1]
    author = details[2]
    category = details[3]
    language = details[4]
    fiction = details[5]
    amount = add_amount
    price = details[7]
    publisher = details[8]
    year = details[9]
    commitf(index, title, author, category, language, fiction, amount, price, publisher, year,)    

def id_editor(id, ori_id, title, index, value):
    id = str(id)
    splited = [*id]
    splited[6] = 1
    del splited[index]
    splited.insert(index, str(value))
    new_id = int("".join(splited))
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

    if int(amount) > 1:
        for i in range (1, int(amount) + 1):
            c.execute(f"UPDATE BOOKS SET ID={id} INTO BOOKS WHERE ID ={ori_id}")
            conn.commit()
            id += 1
            ori_id += 1   
    else:
        c.execute(f"UPDATE BOOKS SET ID={id} INTO BOOKS WHERE ID ={ori_id}")
        conn.commit()

    print("ID has been updated. ")
    c.close()
    conn.close()


edit_book()

# close the connection to the database
conn.close()
