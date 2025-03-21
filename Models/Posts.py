from datetime import datetime

from pymongo import MongoClient
import humanize
from bson import ObjectId

class Posts:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['codewizard']
        self.Users = self.db['Users']
        self.Posts = self.db['Posts']
        self.Comments = self.db['Comments']

    def insert_post(self, data):
        inserted = self.Posts.insert_one({"username" : data.username, "content" : data.content, "date_added" : datetime.now()})
        post = self.Posts.find_one({"_id":inserted.inserted_id})
        new_post = {}
        new_post["name"] = self.Users.find_one({"username": post["username"]})["name"]
        new_post["content"] = post["content"]
        return post

    def get_all_posts(self):
        all_posts = self.Posts.find().sort("date_added", -1)
        new_posts = []
        for post in all_posts:
            post["user"] = self.Users.find_one({"username": post["username"]})
            post["timestamp"] = humanize.naturaltime(datetime.now() - post["date_added"])
            post["old_comments"] = self.Comments.find({"post_id": str(post["_id"])})
            post["comments"] = []

            for comment in post["old_comments"]:
                print(comment)
                comment["user"] = self.Users.find_one({"username": comment["username"]})
                comment["timestamp"] = humanize.naturaltime(datetime.now() - comment["date_added"])
                post["comments"].append(comment)

            new_posts.append(post)

        return new_posts

    def get_user_posts(self, user):
        all_posts = self.Posts.find({"username":user}).sort("date_added", -1)
        new_posts = []
        if all_posts:
            for post in all_posts:
                post["user"] = self.Users.find_one({"username": user})
                post["timestamp"] = humanize.naturaltime(datetime.now() - post["date_added"])
                post["old_comments"] = self.Comments.find({"post_id": str(post["_id"])})
                post["comments"] = []
                for comment in post["old_comments"]:
                    print(comment)
                    comment["user"] = self.Users.find_one({"username": comment["username"]})
                    comment["timestamp"] = humanize.naturaltime(datetime.now() - comment["date_added"])
                    post["comments"].append(comment)
                new_posts.append(post)


        return new_posts

    def add_comment(self, comment):
        inserted = self.Comments.insert_one({"post_id": comment.post_id, "comment_text": comment["comment_text"], "date_added": datetime.now(), "username": comment["username"]})
        return inserted