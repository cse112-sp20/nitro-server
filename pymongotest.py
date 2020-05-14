import pymongo
import datetime
from pymongo import MongoClient

#Connect to MongoDB
client = MongoClient("mongodb://0.0.0.0:27017")
#Create Basecamp database
db = client.Basecamp
#Create collections within db
tasks = db.Tasks
users = db.Users

#variables
time = datetime.datetime(2020, 1, 1)

class Task:
  def __init__(self):
    self.init = True
  
  #insert task into Tasks collection
  def insert(self, info):
    tasks.insert_one(info)

class User:
  u_id = 0
  def __init__(self):
    self.user_id = User.u_id
    User.u_id += 1

  #insert user into Users collection
  def insert(self, info):
    users.insert_one(info)

user1 = User()
#hardcoded user info
userinfo = {"User_id": user1.user_id, "Name": "Johnny", "Email": "test@gmail.com",
  "Password": "password", "Points": 100}       

user1.insert(userinfo)

task1 = Task()
#hardcoded task info
taskinfo = {"_id": 0, "Team": "QA", "Name": "Task 1", "Due_data": time, "Assigned_to"  : 0, "Notes": "test task", "Points": 100}

task1.insert(taskinfo)    
