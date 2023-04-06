import sqlite3
conn = sqlite3.connect('library.db')
c = conn.cursor()

# create the books table
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              author TEXT NOT NULL,
              year INTEGER NOT NULL,
              isbn INTEGER NOT NULL)''')

def menu():
    choice = int(input("[1]Search Book \n[2]View All Books \nEnter your choice: "))
    if choice == 1:
        search_menu()
    elif choice == 2:
        view_all_books()

    else:
        menu()
        quit()

def search_menu():
    choice = int(input("[1]Search Books \n[2]Search title \n[3]Search author \n[4]Search year \n[5]Search ISBN \nEnter your choice: "))
    if choice == 1:
        search_books()
    elif choice == 2:
        search_title()
    elif choice == 3:
        search_author()
    elif choice == 4:
        search_year()
    elif choice == 5:
        search_ISBN()

    else:
        menu()
        quit()

# Define a function to add a book to the database
#def add_book(title, author, year, isbn):
    #c.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", (title, author, year, isbn))
    #conn.commit()
    #print("Book added successfully.")

# Call the add_book function to add a new book to the database
#add_book("anderwear", "hanyi", 2011, "1994")
#add_book("ben", "hanyi", 2012, "2203")
#add_book("cd", "shunhong", 2013, "5594")
#add_book("dics", "shunhong", 2014, "7134")
#add_book("expend", "xiangze", 2015, "3294")
#add_book("fun", "xiangze", 2016, "9810")
#add_book("gg", "jingliang", 2017, "8129")
#add_book("hent", "jingliang", 2018, "3471")
#add_book("jib", "balia", 2019, "6106")
#add_book("palia", "balia", 2020, "4499")


# define the search book
def search_books():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    year = input("Enter the year of the book: ")
    isbn = input("Enter the ISBN of the book: ")

    library = "SELECT * FROM books WHERE "
    conditions = []
    if title:
        conditions.append("title LIKE '%{}%'".format(title))
    if author:
        conditions.append("author LIKE '%{}%'".format(author))
    if year:
        conditions.append("year = {}".format(year))
    if isbn:
        conditions.append("isbn = {}".format(isbn))

    if len(conditions) == 0:
        print("No search criteria specified.")
        return

    else:
        library = "SELECT * FROM books WHERE "
        library += " OR ".join(conditions)
        c.execute(library)
        books = c.fetchall()
        if len(books) == 0:
            print("No books found.")
        else:
            print("Search results:")
            for book in books:
                print(book)

    while True:
        choice = input("Another search? (y/n) ")
        if choice.lower() == 'y':
            search_menu()
        elif choice.lower() == 'n':
            print("***we will proceed back to menu***")
            menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def search_title():
    title = input("Enter the title of the book: ")

    library = "SELECT * FROM books WHERE "
    conditions = []
    if title:
        conditions.append("title LIKE '%{}%'".format(title))

    if len(conditions) == 0:
        print("No search criteria specified.")
        return

    else:
        library = "SELECT * FROM books WHERE "
        library += " OR ".join(conditions)
        c.execute(library)
        books = c.fetchall()
        if len(books) == 0:
            print("No books found.")
        else:
            print("Search results:")
            for book in books:
                print(book)

    while True:
        choice = input("Another search? (y/n) ")
        if choice.lower() == 'y':
            search_menu()
        elif choice.lower() == 'n':
            print("***we will proceed back to menu***")
            menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def search_author():
    author = input("Enter the author of the book: ")

    library = "SELECT * FROM books WHERE "
    conditions = []
    if author:
        conditions.append("author LIKE '%{}%'".format(author))

    if len(conditions) == 0:
        print("No search criteria specified.")
        return

    else:
        library = "SELECT * FROM books WHERE "
        library += " OR ".join(conditions)
        c.execute(library)
        books = c.fetchall()
        if len(books) == 0:
            print("No books found.")
        else:
            print("Search results:")
            for book in books:
                print(book)

    while True:
        choice = input("Another search? (y/n) ")
        if choice.lower() == 'y':
            search_menu()
        elif choice.lower() == 'n':
            print("***we will proceed back to menu***")
            menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def search_year():
    year = input("Enter the year of the book: ")

    library = "SELECT * FROM books WHERE "
    conditions = []
    if year:
        conditions.append("year = {}".format(year))

    if len(conditions) == 0:
        print("No search criteria specified.")
        return

    else:
        library = "SELECT * FROM books WHERE "
        library += " OR ".join(conditions)
        c.execute(library)
        books = c.fetchall()
        if len(books) == 0:
            print("No books found.")
        else:
            print("Search results:")
            for book in books:
                print(book)

    while True:
        choice = input("Another search? (y/n) ")
        if choice.lower() == 'y':
            search_menu()
        elif choice.lower() == 'n':
            print("***we will proceed back to menu***")
            menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def search_ISBN():
    isbn = input("Enter the ISBN of the book: ")

    library = "SELECT * FROM books WHERE "
    conditions = []
    if isbn:
        conditions.append("isbn = {}".format(isbn))

    if len(conditions) == 0:
        print("No search criteria specified.")
        return

    else:
        library = "SELECT * FROM books WHERE "
        library += " OR ".join(conditions)
        c.execute(library)
        books = c.fetchall()
        if len(books) == 0:
            print("No books found.")
        else:
            print("Search results:")
            for book in books:
                print(book)

    while True:
        choice = input("Another search? (y/n) ")
        if choice.lower() == 'y':
            search_menu()
        elif choice.lower() == 'n':
            print("***we will proceed back to menu***")
            menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def view_all_books():
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    if len(books) == 0:
        print("No books found.")
        menu()
    else:
        print("Books:")
        for book in books:
            print(book)
        menu()

menu()

# close the connection to the database
conn.close()
