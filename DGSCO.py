# import
from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    # Check if username already exists
    existing_user = UserModel.find_user(username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user
    user_id = UserModel.create_user(username, password)

    return {"message": "Signup successful", "_id": user_id}

# Login
@app.post("/login")
def login(username: str, password: str):
    # Find the user and check user with password
    user = UserModel.passcheck(username, password)
    if user:
        return {"message": "Login successful", "_id": str(user.get("_id"))}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or password")


# Twitter Login


# logout from twitter


# Find all Followers


# Run App