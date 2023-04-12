from tabulate import tabulate
import sqlite3
conn = sqlite3.connect('books.db')
c = conn.cursor()

def menu():
    choice = int(input("[1]Search Book \n[2]View All Books \n[3]Back to menu \nEnter your choice: "))
    while choice == '' or choice < 1 or choice > 3: 
        print("Invalid")
        choice = input("[1]Search Book \n[2]View All Books \nEnter your choice: ")
    if choice == 1:
        search_menu()
    elif choice == 2:
        view_all_books()
    else:
        menu()
        quit()

def search_menu():
    choices = ["title", "author", "year", "category", "language", "availability", "publisher"]
    choice_input = int(input("Search with: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Availability \n[7]Publisher \n[8]Back to menu \nEnter your choice: "))
    while choice_input < 1 or choice_input > 8:
        choice_input = int(input("Search with: \n[1]Title \n[2]Author \n[3]Year \n[4]Category \n[5]Language \n[6]Availability \n[7]Publisher \n[8]Back to menu \nEnter your choice: "))
    if choice_input == 8:
        menu()
    else:
        choice = choices[choice_input-1]
        if choice_input == 6:
            user_input = str(input(f"Enter {choice} (0 or 1): "))
        else:
            user_input = str(input(f"Enter {choice}: "))
    library = str(f"SELECT ID, TITLE, AUTHOR, CATEGORY, LANGUAGE, FICTION, AMOUNT, PUBLISHER, YEAR FROM books WHERE {choice} LIKE '%{user_input}%'")
    print(library)
    data = []
    c.execute(library)
    books = c.fetchall()
    print(books)
    if len(books) == 0:
        print("No books found.")
    else:
        print("Search results:")
        for book in books:
            data.append(book)
        listing(data)

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
    data = []
    if len(books) == 0:
        print("No books found.")
        menu()
    else:
        print("Books:")
        for book in books:
            data.append(book)
        listing(data)
    
    while True:
        choice = input("Another search? (y/n) ")
        if choice.lower() == 'y':
            search_menu()
        elif choice.lower() == 'n':
            print("***we will proceed back to menu***")
            menu()
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def listing(data):
    headers = ["ID", "TITLE", "AUTHOR", "CATEGORY", "LANGUAGE", "FICTION","AVAILABILITY", "PUBLISHER", "YEAR"]
    print(tabulate(data, headers=headers, tablefmt="outline"))

menu()

# close the connection to the database
conn.close()
