import bcrypt
from pymongo import MongoClient


class RegisterModel:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['codewizard']
        self.Users = self.db['Users']

    def insert_user(self, data):
        hashed =bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        try:
            result = self.Users.insert_one({"username" : data.username, "name" : data.name, "password" : hashed,
                                            "email" : data.email, "avatar" : "", "background" : "", "about" : "",
                                            "birthday" : ""})
            id = result.inserted_id
        except Exception as e:
            print("Error inserting data:", e)
            raise

        print("uid is ", id)