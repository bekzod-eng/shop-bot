import sqlite3
conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

async def insert_product(data: dict):
    name = data.get("name")
    chat_id = data.get('chat_id')
    contact = data.get('contact')
    info = data.get('info')
    price = data.get('price')
    photo = data.get('image')

    query = (f""" insert into products (image, info, price, contact, chat_id, name)
             values ('{photo}', '{info}','{price}','{contact}',{chat_id}, '{name}')""")

    cursor.execute(query)
    conn.commit()
    return True
