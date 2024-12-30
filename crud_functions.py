import sqlite3


def initiate_db(title, description, price):
    connection1 = sqlite3.connect("Products.db")
    cursor = connection1.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL)
    """)

    cursor.execute("""INSERT INTO Products (title, description, price)
    VALUES (?, ?, ?)""", (title, description, price))

    connection1.commit()
    connection1.close()

    connection2 = sqlite3.connect('Users.db')
    cursor2 = connection2.cursor()

    cursor2.execute("""CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL)
        """)

    connection2.commit()
    connection2.close()

def get_all_products():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()

    result = cursor.execute("SELECT * FROM Products")
    res = result.fetchall()

    connection.commit()
    connection.close()

    return res

list_products = [('Банан', 'Питательный', 100),('Яблоко', 'Полезное', 200),
                 ('Абрикос', 'Сочный', 300),('Банан', 'Сладкий', 400)]


for args in list_products:
    initiate_db(*args)

def add_user(username, email, age):

    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO Users'
                   '(username, email, age, balance) VALUES (?, ?, ?, ?)', (username, email, age, 1000))

    connection.commit()
    connection.close()

def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()

    res = cursor.execute('SELECT username FROM Users WHERE username = ?', (username,))
    if res.fetchone() is None:
        return False
    else:
        return True




# connection = sqlite3.connect("Users.db")
# cursor = connection.cursor()
# cursor.execute('DELETE FROM Users')
# connection.commit()
# connection.close()
