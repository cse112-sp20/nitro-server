# pylint: disable=anomalous-backslash-in-string
# Disabling anomalous-backslash-in-string because it is needed for regexp
"""
Module to interface with Basecamp api. Used to instantiate endpoints and token
"""
import json
import re
import requests
from database_access_object import Task

# Gets the format (100)
POINTS_REGEXP = "\(\\b(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\\b\)"
# We only want to match the todos with (NITRO)
NITRO_TODO_REGEXP = "\(NITRO\)"

class Basecamp():
    """Object used to interact with basecamp api"""
    def __init__(self, auth_token, acc_id):

        # Set authentication parameters
        self.acc_id = acc_id
        self.header = {"Authorization": "Bearer " + auth_token}

        # Requests endpoint
        self.base_endpoint = "https://3.basecampapi.com/{}/projects.json".format(self.acc_id)
        self.complete_endpoint = 'https://3.basecampapi.com/{}/buckets/{}/todos/{}/completion.json'
        self.task_endpoint = "https://3.basecampapi.com/{}/buckets/{}/todos/{}.json"
        self.delete_todo_endpoint = "https://3.basecampapi.com/" + self.acc_id + "/buckets/{}/" \
                                    "recordings/{}/status/trashed.json"
        # Database access object
        self.tasks = Task()

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
            if projects['purpose'] == 'team':
                team = {}
                team['name'] = projects['name']
                team['project_id'] = projects['id']
                team['todoset_id'] = [item['id']
                                      for item in projects['dock']
                                      if item['name'] == 'todoset'][0]
                task_list_items = self.get_task_list([item['url']
                                                      for item in projects['dock']
                                                      if item['name'] == 'todoset'][0])
                # Consolidates the tasks into one giant array
                consolidated_tasks = consolidate_tasks(task_list_items)
                team['consolidated_tasks'] = consolidated_tasks[0]
                team['points_required'] = consolidated_tasks[1]
                team['points_completed'] = consolidated_tasks[2]
                team_res.append(team)
        return team_res

    def get_task_list(self, taskset_endpoint):
        """
        Generates List of todolists
        @ param taskset_endpoint (str): utf-8 string of the taskset endpoint
        @ returns [dict] : List of tasks_lists
        """
        taskset_response = requests.get(taskset_endpoint, headers=self.header)

        if taskset_response.status_code != 200:
            raise Exception(str(taskset_response.status_code))

        #Each project has multiple todo lists
        result_list = []
        task_set_data = json.loads(taskset_response.content)

        # Get the task_lists from task_set url
        task_list_url = task_set_data['todolists_url']
        task_list_response = requests.get(task_list_url, headers=self.header)

        if task_list_response.status_code != 200:
            raise Exception(str(task_list_response.status_code))

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
                task_list_elem['points'] = get_points_available(task_list_elem['task'])
                result_list.append(task_list_elem)

        for task_list in result_list:
            task_list['points_completed'] = self.get_points_completed(task_list['task_list_id'])

        return result_list

    def get_task(self, todos_url):
        """
        Get the individual tasks for each task list
        @ param todos_url (str) : url endpoint of the todo
        @ return ([dict]): List of todo json objexts
        """
        # Where we store the todo list
        res = []
        todo_response = requests.get(todos_url, headers=self.header)
        if todo_response.status_code != 200:
            raise Exception(str(todo_response.status_code))
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

    def get_points_completed(self, task_list_id):
        """
        returns the number of points that the team has completed
        @ param task_list_id (str): Id of the task_list we are parsing the points from
        @ returns (int) : All the points in the task list
        """
        points = 0
        tasks = self.tasks.get_all_task(task_list_id)
        for task in tasks:
            points += task['points']
        return points

    def complete_task(self, project_id, todo_id):
        """
        Makes a post request to Basecamp api to complete a todo
        """
        # Get task_list id so that we can store into the database
        task_endpoint = self.task_endpoint.format(self.acc_id, project_id, todo_id)
        task_res = requests.get(task_endpoint, headers=self.header)
        if task_res.status_code != 200:
            raise Exception(str(task_res.status_code))
        task_json = json.loads(task_res.content)
        task_list_id = task_json['parent']['id']
        points = parse_points(task_json['title'])

        complete_todo_endpoint = self.complete_endpoint.format(self.acc_id, project_id, todo_id)
        post_response = requests.post(complete_todo_endpoint, headers=self.header)
        if post_response.status_code != 204:
            raise Exception(str(post_response.status_code))

        # inserts the task into the datbase
        self.tasks.insert_task(self.acc_id, points, todo_id, project_id, task_list_id)
        return {"success" : "ok"}

    def init_webhook(self):
        """
        initializes the webhook endpoints
        @ returns None
        """
        project_data = requests.get(self.base_endpoint, headers=self.header)
        if project_data.status_code != 200:
            raise Exception('cannot make request to get projects')
        project_json = json.loads(project_data.content)

        for projects in project_json:
            if projects['purpose'] == 'team':
                webhook_endpoint = 'https://3.basecampapi.com/{}" \
                                    "/buckets/{}/webhooks.json'.format(self.acc_id, projects['id'])
                header = self.header
                header['Content-Type'] = 'application/json'
                header['User-Agent'] = 'Freshbooks (http://freshbooks.com/contact.php)'
                param = {'payload_url' : 'http://0.0.0.0:80'}
                requests.post(webhook_endpoint, headers=header, params=param)

    def delete_task(self, project_id, todo_id):
        """
        Deletes a task without allocating points
        @ param project_id (str): id of the project the task we want to delete is in
        @ param todo_id (str): id of the todo we want to delete
        @ returns None
        """
        endpoint = self.delete_todo_endpoint.format(project_id, todo_id)
        res = requests.put(endpoint, headers=self.header)
        if res.status_code != 204:
            raise Exception(str(res.status_code))
        # removes from the database
        self.tasks.remove(todo_id)

    def uncomplete(self, project_id, todo_id):
        """
        Uncompletes a completed task from basecamp and removes it from the database
        @ param project_id (str): id of the project the task we want to delete is in
        @ param todo_id (str): id of the todo we want to delete
        @ returns None
        """
        endpoint = self.complete_endpoint.format(self.acc_id, project_id, todo_id)
        requests.delete(endpoint, headers=self.header)
        self.tasks.remove(int(todo_id))

    def uncomplete_all(self):
        """
        uncompletes all completed tasks
        @ returns None
        """
        tasks = self.tasks.get_all()
        for task in tasks:
            self.uncomplete(task['proj_id'], task['todo_id'])

def consolidate_tasks(task_lists):
    """
    Helper method to flatten the multi level task-list into a single array of tasks
    @ task_list ([dict]): an array of task_list objects
    @ return tuple: First element is the flatted tasks, the second element is the points
    required, and the third elements is the points completed
    """
    # The flattened list containing all the tasks
    res = []
    points_required = 0
    points_completed = 0
    for task_list in task_lists:
        points_required += task_list['points']
        points_completed += task_list['points_completed']
        for tasks in task_list['task']:
            res.append(tasks)
    return (res, points_required, points_completed)

def get_points_available(tasks):
    """
    Gets all the points available in a task list
    @ param tasks([dict]): A list of task object
    @ return (int)
    """
    points = 0
    for task in tasks:
        points += task['points']
    return points

def parse_points(title):
    """
    Parses the points of the title of the todo must be in the form (0-255)
    @ param title (str): The string of the todo name
    @ returns int: points parsed
    """
    points = 0
    parsed = re.search(POINTS_REGEXP, title)
    # Parses the results and adds it to the points
    if parsed:
        points += int(parsed.group(1))
    return points
    