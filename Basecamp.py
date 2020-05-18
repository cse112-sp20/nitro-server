# pylint: disable=invalid-name
"""
Module to interface with Basecamp api. Used to instantiate endpoints and token
"""
import os
import json
import requests
import re
from Database_Access_Object import Task
from dotenv import load_dotenv

# Gets the format (100)
POINTS_REGEXP = "\(\\b(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\\b\)"
# We only want to match the todos with (NITRO)
NITRO_TODO_REGEXP = "\(NITRO\)"

class Basecamp():
    """Object used to interact with basecamp api"""
    def __init__(self, auth_token, acc_id):

        # Set authentication parameters
        self.auth_token = auth_token.decode()
        self.acc_id = acc_id
        self.header = {"Authorization": "Bearer " + self.auth_token}
        #self.project_id = os.environ.get('PROJECT_ID')
        self.HOST = os.environ.get('HOST')

        # Basecamp endpoints
        self.root_endpoint = "https://3.basecampapi.com"
        self.base_endpoint = "https://3.basecampapi.com/{}/projects.json".format(self.acc_id)
        self.complete_endpoint = 'https://3.basecampapi.com/{}/buckets/{}/todos/{}/completion.json'
        self.task_endpoint = self.root_endpoint + "/{}/buckets/{}/todos/{}.json"

        # Database access objects
        self.tasks = Task()
        
        print("The auth token is ", auth_token)

    def json_dump(self):
        """
        Gets a dump of the json that for the front-end
        returns: dict
        """
        # Gets the parent object of basecamp to parse
        project_response = requests.get(self.base_endpoint, headers=self.header)

        project_json = json.loads(project_response.content)
        acc_obj = {}
        acc_obj['account_id'] = self.acc_id
        acc_obj['teams'] = self.get_teams(project_json)
        return acc_obj

    def get_teams(self, project_json):
        """
        Gets all teams on basecamp
        project_json: dict
        returns: dictionary
        """
        team_res = []
        for projects in project_json:
            if projects['purpose'] == 'team' :
                team = {}
                team['name'] = projects['name']
                team['project_id'] = projects['id']
                team['todoset_id'] = [item['id']
                                      for item in projects['dock']
                                      if item['name'] == 'todoset'][0]
                team['task_list'] = self.get_task_list([item['url']
                                                        for item in projects['dock']
                                                        if item['name'] == 'todoset'][0])

                team_res.append(team)
        return team_res

    def get_task_list(self, taskset_endpoint):
        """
        Generate List of todolists
        taskset_endpoint: utf-8 string of the taskset endpoint
        """
        taskset_response = requests.get(taskset_endpoint, headers=self.header)

        if taskset_response.status_code != 200:
            raise Exception("Failed to fetch task list at endpint {}".format(taskset_endpoint))

        #Each project has multiple todo lists
        result_list = []
        task_set_data = json.loads(taskset_response.content)

        # Get the task_lists from task_set url
        task_list_url = task_set_data['todolists_url']
        task_list_response = requests.get(task_list_url, headers=self.header)

        if task_list_response.status_code != 200:
            raise Exception("unable to get result")

        # Add tasklist objects
        for task_list in json.loads(task_list_response.content):
            # Only take the task_list with the (NITRO) tag in the title
            if re.search(NITRO_TODO_REGEXP, task_list['name']):
                task_list_elem = {}
                task_list_elem['task_list_id'] = task_list['id']
                task_list_elem['description'] = task_list['description']
                task_list_elem['task_list_name'] = task_list['name']
                task_list_elem['parent_id'] = task_list['parent']['id']
                task_list_elem['parent_project'] = task_list['bucket']['name']
                task_list_elem['task'] = self.get_task(task_list['todos_url'])
                # Sums up the points of each individual task
                task_list_elem['points'] = self.get_points_available(task_list_elem['task'])
                result_list.append(task_list_elem)

        for task_list in result_list:
            task_list['points_completed'] = self.get_points_completed(task_list['task_list_id'])

        return result_list

    def get_task(self, todos_url):
        """
        Get the individual tasks for each task list
        """
        res = []
        todo_response = requests.get(todos_url, headers=self.header)
        if todo_response.status_code != 200:
            raise Exception("Faled to get todo items")
        todo_list = json.loads(todo_response.content)
        for todo in todo_list:

            self.tasks.remove(todo['id'])

            task_item = {}
            task_item['id'] = todo['id']
            task_item['title'] = todo['title']
            task_item['status'] = todo['status']
            task_item['due_on'] = todo['due_on']
            task_item['assignees'] = todo['assignees']

            #Parse the regular expression to get the number
            task_item['points'] = 0

            # returns "(number)"
            parsed = re.search(POINTS_REGEXP, todo['title'])
            # Parses the results and adds it to the points
            if parsed:
                task_item['points'] += int(parsed.group(1))
            res.append(task_item)
        return res

    def get_points_available(self, tasks):
        """
        @ param tasks: A list of task object
        @ return number
        """
        points = 0
        for task in tasks:
            points += task['points']
        return points

    def get_points_completed(self, task_list_id):
        """
        returns the number of points that the team has completed
        """
        points = 0
        tasks = self.tasks.get_all_task(task_list_id)
        for task in tasks:
            points += task['points']
        return points

    def parse_points(self, title):
        """
        Parses the points of the title of the todo must be in the form (0-255)
        """
        points = 0
        parsed = re.search(POINTS_REGEXP, title) 
        # Parses the results and adds it to the points
        if parsed:
            points += int(parsed.group(1))
        return points

    def complete_task(self, project_id, todo_id):
        """
        Makes a post request to Basecamp api to complete a todo
        """
        # Get task_list id so that we can store into the database
        task_endpoint = self.task_endpoint.format(self.acc_id, project_id, todo_id)
        task_res = requests.get(task_endpoint, headers=self.header)
        if task_res.status_code != 200:
            raise Exception("made bad request to get task meta data")
        task_json = json.loads(task_res.content)
        task_list_id = task_json['parent']['id']
        points = self.parse_points(task_json['title'])

        complete_todo_endpoint = self.complete_endpoint.format(self.acc_id, project_id, todo_id)
        post_response = requests.post(complete_todo_endpoint, headers=self.header)
        if post_response.status_code != 204:
            raise Exception("bad requests")

        # inserts the task into the datbase
        self.tasks.insert_task(self.acc_id, points, todo_id, project_id, task_list_id)
        return {"success" : "ok"}

    def init_webhook(self):
        project_data = requests.get(self.base_endpoint, headers=self.header)

        if project_data.status_code != 200:
            raise Exception('cannot make request to get projects')
        project_json = json.loads(project_data.content)
            
        # For some reason can't get webhooks to work to update the completed
        for projects in project_json:
            if projects['purpose'] == 'team' :
                webhook_endpoint = 'https://3.basecampapi.com/{}/buckets/{}/webhooks.json'.format(self.acc_id, projects['id'])
                header = self.header
                header['Content-Type'] = 'application/json'
                header['User-Agent'] = 'Freshbooks (http://freshbooks.com/contact.php)'
                param = {'payload_url' : 'http://localhost:80'}
                r = requests.post(webhook_endpoint, headers=header, params=param)
                print(r.status_code)
                print(r.text)
