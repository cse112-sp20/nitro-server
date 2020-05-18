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

class Task:
    def insert(self, info):
        tasks.insert_one(info)

    def insert_task(self, acc_id, points, todo_id, proj_id, task_list_id):
        """
        Inserts a completed todo list into the database
        @ acc_id = the account id the task is associated with
        @ param points: How much points the task was worth
        @ param proj_id: The project id the task was apart of
        @ param todo_id: The todo's id
        @ return True if collection successfully inserted
        """
        res = tasks.find_one({"todo_id": todo_id})
        if not res:
            tasks.insert({"todo_id" : todo_id, "points" : points, "proj_id" : proj_id, "acc_id" : acc_id, 'task_list_id' : task_list_id})
            return True
        return False

    def find_one(self, todo_id):
        """
        Finds a completed to_do given a todo id
        """
        print('searching for ' + str(todo_id))
        return tasks.find_one({'todo_id' : todo_id})
    
    def remove(self, todo_id):
        assert isinstance(todo_id, int)
        tasks.delete_one({'todo_id' : str(todo_id)})

    def get_all_task(self, task_list_id):
        """
        gets all task associated with a task_list_id
        @ param taks_list_id the id of the taks list that you want to query from
        """
        return tasks.find({"task_list_id" : task_list_id})       


class User:
    u_id = 0
    def __init__(self):
        self.user_id = User.u_id
        User.u_id += 1

    #insert user into Users collection
    def insert(self, info):
        users.insert_one(ifo)

