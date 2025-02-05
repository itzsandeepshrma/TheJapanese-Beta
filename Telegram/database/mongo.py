from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["TheJapaneseDB"]

def insert_user(user_id, username):
    db.users.insert_one({"user_id": user_id, "username": username})
