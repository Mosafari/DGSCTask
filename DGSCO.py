# import
from fastapi import FastAPI
from pymongo import MongoClient

# instantiate the FastAPI object
app = FastAPI()

# initialize the MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

# create user model to create and find users
class UserModel:
    collection = db["users"]  # MongoDB collection for storing users

    @classmethod # create a user
    def create_user(cls, username: str, password: str) -> str:
        user = {"username": username, "password": password}
        result = cls.collection.insert_one(user)
        return str(result.inserted_id)

    @classmethod # check if user already exists
    def find_user(cls, username: str) :
        return cls.collection.find_one({"username": username})
    
    @classmethod # check password with username
    def passcheck(cls, username: str, password: str) :
        return cls.collection.find_one({"username": username, "password": password})
    
    @classmethod # find user by id
    def find_user_by_id(cls, user_id: str):
        user = cls.collection.find_one({"_id": ObjectId(user_id)})
        return user

# signup
@app.post("/signup")
def signup(username: str, password: str):
    return {"message": "Signup successful"}

# Login


# Twitter Login


# logout from twitter


# Find all Followers


# Run App