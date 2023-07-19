# import
from fastapi import FastAPI
from pymongo import MongoClient

# instantiate the FastAPI object
app = FastAPI()

# initialize the MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

# create user model to create and find users


# signup
@app.post("/signup")
def signup(username: str, password: str):
    return {"message": "Signup successful"}

# Login


# Twitter Login


# logout from twitter


# Find all Followers


# Run App