import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="TheJapaneseDB"
)

cursor = db.cursor()

def insert_user(user_id, username):
    cursor.execute("INSERT INTO users (user_id, username) VALUES (%s, %s)", (user_id, username))
    db.commit()
