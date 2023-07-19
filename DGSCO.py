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
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver as wd
import os
from selenium.webdriver.common.by import By   
import time
def logintwitter(username: str, password: str):
    global driver
    # initialize the driver
    path = os.getcwd() + '\geckodriver.exe'
    ser = Service(r'{}'.format(path))
    options = Options()
    options.headless = True
    driver = wd.Firefox(options=options,  service=ser)#
    driver.implicitly_wait(20)
    URL = "https://twitter.com/"
    driver.get(URL)
    time.sleep(5)
    # enter username and password
    driver.find_element(By.CSS_SELECTOR, ".r-30o5oe").send_keys(username)
    driver.find_element(By.CSS_SELECTOR, "div.css-18t94o4:nth-child(6) > div:nth-child(1)").click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, ".r-homxoj").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, ".r-19yznuf").click()
    if driver.find_elements(By.CSS_SELECTOR, "a.r-1habvwh:nth-child(1) > div:nth-child(1)"): # if its on home page
        return True
    else: return False
    
@app.post("/twitterlogin")
def twitterlogin(username: str, password: str, id : str):
    data = dict()
    login = logintwitter(username, password)
    if login:
        data['message'] = "Add successful"
    else:
        # if it doesn't exist close the session 
        driver.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if data['message'] == "Add successful" :
        collection = db["users"]
        filter = {"_id": ObjectId(id)}
        update = {"$set": {"Tusername": username, "Tpassword": password}}

        # Update the record
        collection.update_one(filter, update)

    return {"message": data["message"], "_id": id}

# logout from twitter
@app.post("/twitterlogout")
def logouttwitter():
    global driver
    if driver is  None:
        return {"message": "You'r not logged in!"}
    else: 
        if driver.find_elements(By.CSS_SELECTOR, "a.r-1habvwh:nth-child(1) > div:nth-child(1)"): # if its on home page
            time.sleep(5)
            # click the menu to logout
            driver.find_element(By.CSS_SELECTOR, "div.r-1q142lx:nth-child(1) > div:nth-child(1)").click()
            driver.find_element(By.CSS_SELECTOR, ".r-usiww2 > div:nth-child(1) > div:nth-child(1)").click() 
            driver.find_element(By.CSS_SELECTOR, "a.r-18u37iz:nth-child(3) > div:nth-child(1) > div:nth-child(1)").click()
            if driver.find_element(By.CSS_SELECTOR, "div.css-18t94o4:nth-child(1) > div:nth-child(1)"):
                driver.find_element(By.CSS_SELECTOR, "div.css-18t94o4:nth-child(1) > div:nth-child(1)").click()
                driver.close()
            driver = None
            return {"message": "Successfully closed"}

# Find all Followers
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys   
@app.post("/followers")
def followers(id : str, username : str):
    if not driver.find_elements(By.CSS_SELECTOR, "a.r-1habvwh:nth-child(1) > div:nth-child(1)"): # if its on home page
        return {"message": "First Login!"}
    else:
        # Find the user
        user = UserModel.find_user_by_id(id)
        driver.get(f"https://twitter.com/{username}/followers")
        for _ in range(10):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END) # scroll to end of body
            time.sleep(1)  # Add a small delay to wait for the content to load
        # find the section for the followers
        section = driver.find_element(By.CSS_SELECTOR, "section.css-1dbjc4n:nth-child(3)").text
        followers = [i for i in section.split('\n') if '@' in i]
        return {f'{username}_followers': followers}
    # or this way ( with twitter api)
    # if you have a pro account
    # import tweepy

    # # Authenticate to Twitter
    # auth = tweepy.OAuthHandler("CONSUMER_KEY", "CONSUMER_SECRET")
    # auth.set_access_token("ACCESS_TOKEN", "ACCESS_TOKEN_SECRET")

    # api = tweepy.API(auth)

    # try:
    #     api.verify_credentials()
    #     print("Authentication OK")
    # except:
    #     print("Error during authentication")
    # print(user["Tusername"])
    # username = user["Tusername"]
    # followers = api.get_follower_ids(screen_name="bi3da021")
    # for follower_id in followers:
    #     follower = api.get_user(user_id=follower_id)
    #     print(follower.screen_name)
    # testuserdata = api.get_followers(user_id="bi3da021")
    # print(testuserdata)
    # for j in testuserdata.followers():
    #     print(j.name)
    # userdata = api.get_followers(user_id=username)
    # print(userdata)
    # for i in userdata.followers():
    #     print(i.name)

# Run App