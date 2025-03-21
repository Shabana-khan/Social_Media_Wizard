import bcrypt
from pymongo import MongoClient
from dotenv import load_dotenv
import os

class LoginModel:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()

        # Get MongoDB URI from .env file
        mongo_uri = os.getenv("MONGO_URI")

        self.client = MongoClient(mongo_uri)
        self.db = self.client['codewizard']
        self.Users = self.db['Users']

    def check_user(self, data):
        user = self.Users.find_one({"username": data.username})
        if user:
            password = user["password"].encode("utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            if bcrypt.checkpw(data.password.encode(), hashed_password):
                return user
            else:
                return False
        else:
            return False

    def update_info(self, data):
        updated = self.Users.update_one({
            "username" : data["username"]
        }, {"$set" : data})
        print(updated)
        return True

    def get_profile(self,user):
        user_info = self.Users.find_one({"username": user})
        print(user_info)
        return user_info

    def update_image(self, update):
        updated = self.Users.update_one({"username": update["username"]},
                                        {"$set": {update["type"]: update["img"]}})

        return updated