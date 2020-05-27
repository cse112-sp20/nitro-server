# pylint: disable=too-many-arguments
# Disabling to many arguments because it is needed
"""
Objects used to make CRUD operations on the database
"""
from pymongo import MongoClient

#Connect to MongoDB
client = MongoClient("mongodb://0.0.0.0:27017")
#Create Basecamp database
db = client.Basecamp
#Create collections within db
tasks = db.Tasks
users = db.Users

class Task:
    """
    Object used to interface with the task collections
    """
    def __init__(self):
        # updated flag
        self.num_inserted = 0
        self.query_count = 0

    def insert(self, info):
        """
        inserts a task into the task collection
        @ param info (dict): Task dictionary we want to insert
        """
        self.num_inserted += 1
        tasks.insert_one(info)

    def insert_task(self, acc_id, points, todo_id, proj_id, task_list_id, title):
        """
        Inserts a completed todo list into the database
        @ acc_id = the account id the task is associated with
        @ param points: How much points the task was worth
        @ param proj_id: The project id the task was apart of
        @ param todo_id: The todo's id
        @ return True if collection successfully inserted
        """
        res = tasks.find_one({"todo_id": todo_id})
        self.num_inserted += 1
        if not res:
            tasks.insert({"todo_id" : todo_id,
                          "points" : points,
                          "proj_id" : proj_id,
                          "acc_id" : acc_id,
                          "task_list_id" : task_list_id,
                          "title" : title})
            return True
        return False

    def find_one(self, todo_id):
        """
        Finds a completed to_do given a todo id
        @ param todo_id (str): finds a task with id todo_id
        @ returns dict
        """
        self.query_count += 1
        return tasks.find_one({'todo_id' : todo_id})

    def remove(self, todo_id):
        """
        removes a task collection with a todo_id
        @ param todo_id (int): id of the task we are deleting
        """
        self.num_inserted -= 1
        tasks.delete_one({'todo_id' : str(todo_id)})

    def get_all_task(self, task_list_id):
        """
        gets all task associated with a task_list_id
        @ param taks_list_id the id of the taks list that you want to query from
        """
        self.query_count += 1
        return tasks.find({"task_list_id" : task_list_id})

    def get_all_task_with_projid(self, proj_id):
        """
        gets all the tasks with the associated project id
        """
        self.query_count += 1
        completed_tasks = list(tasks.find({"proj_id" : str(proj_id)}))
        for i in completed_tasks:
            i.pop("_id")
        return completed_tasks

    def get_all(self):
        """
        gets all tasks
        @ return [dict]: List of tasks
        """
        self.query_count += 2
        return tasks.find()
