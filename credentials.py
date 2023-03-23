import sqlite3

conn = sqlite3.connect('credentials.db')

conn.execute('''CREATE TABLE IF NOT EXISTS CREDENTIALS 
    (ID INT PRIMARY KEY   NOT NULL,
    NAME        TEXT   NOT NULL,
    PHONE       INT    NOT NULL,
    EMAIL       TEXT   NOT NULL,
    OCCUPATION  TEXT   NOT NULL);''')

conn.execute("INSERT INTO CREDENTIALS (ID,NAME,PHONE,EMAIL,OCCUPATION) \
    VALUES (1211106996, 'INSANE', '0123456789', 'MAIL@GMAIL.COM', 'STUDENT')");


cursor = conn.execute("SELECT ID, phone, email, occupation from LIBRARY")
for row in cursor:
    print(row)

conn.commit()
conn.close()

print("hello")
