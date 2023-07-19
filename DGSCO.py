# import
from fastapi import FastAPI

# instantiate the FastAPI object
app = FastAPI()

# initialize the MongoClient


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