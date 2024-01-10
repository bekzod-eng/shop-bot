import sqlite3

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# query = """
# CREATE TABLE users (
# id INTEGER PRIMARY KEY AUTOINCREMENT,
# full_name TEXT NOT NULL,
# phone_number TEXT NOT NULL,
# login TEXT NOT NUll,
# password TEXT NOT NULL,
# chat_id INTEGER NOT NULL 
# )
# """




query = """
CREATE TABLE product (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
phone_number TEXT NOT NULL,
login TEXT NOT NUll,
chat_id INTEGER NOT NULL 
)
"""

cursor.execute(query)
conn.commit()




async def insert_product(data: dict):
    name = data.get("name")
    chat_id = data.get('chat_id')
    contact = data.get('contact')


    query = (f""" insert into products (contact, chat_id, name)
             values (''{contact}',{chat_id}, '{name}')""")

    cursor.execute(query)
    conn.commit()
    return True
