import sqlite3

conn = sqlite3.connect('test.db')

conn.execute('''CREATE TABLE IF NOT EXISTS LIBRARY 
    (ID INT PRIMARY KEY   NOT NULL,
    TITLE        TEXT   NOT NULL,
    AUTHOR       TEXT   NOT NULL,
    PUBLISHER    TEXT   NOT NULL);''')

conn.execute("INSERT INTO LIBRARY (ID,TITLE,AUTHOR,PUBLISHER) \
    VALUES (1, 'Test', 'California', 'A1 Pic' )");


cursor = conn.execute("SELECT ID, title, author, publisher from LIBRARY")
for row in cursor:
    print(row)

conn.commit()
conn.close()

print("hello")
