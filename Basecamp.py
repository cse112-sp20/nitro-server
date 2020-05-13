#pylint: disable=invalid-name
"""
Module to interface with Basecamp api. Used to instantiate endpoints and token
"""
import json
import requests

class Basecamp:
    """Object used to interact with basecamp api"""
    def __init__(self, auth_token, acc_id):

        # Set authentication parameters
        self.auth_token = auth_token.decode()
        self.acc_id = acc_id
        self.header = {"Authorization": "Bearer " + self.auth_token}

        # Basecamp endpoints
        self.base_endpoint = "https://3.basecampapi.com/{}/projects.json".format(self.acc_id)
        self.complete_endpoint = 'https://3.basecampapi.com/{}/buckets/{}/todos/{}/completion.json'

    def json_dump(self):
        """
        Gets a dump of the json that for the front-end
        returns: dict
        """
        # Gets the parent object of basecamp to parse
        project_response = requests.get(self.base_endpoint, headers=self.header)

        if project_response.status_code != 200:
            raise Exception("failed request")

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
                team['task_list'] = self.get_task_list([item['url']
                                                        for item in projects['dock']
                                                        if item['name'] == 'todoset'][0])
                team['points'] = self.calculate_points()
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
            task_list_elem = {}
            task_list_elem['task_list_id'] = task_list['id']
            task_list_elem['description'] = task_list['description']
            task_list_elem['task_list_name'] = task_list['name']
            task_list_elem['parent_id'] = task_list['parent']['id']
            task_list_elem['parent_project'] = task_list['bucket']['name']
            task_list_elem['task'] = self.get_task(task_list['todos_url'])
            result_list.append(task_list_elem)
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
            task_item = {}
            task_item['id'] = todo['id']
            task_item['title'] = todo['title']
            task_item['status'] = todo['status']
            task_item['due_on'] = todo['due_on']
            task_item['assignees'] = todo['assignees']
            res.append(task_item)
        return res

    def complete_task(self, project_id, todo_id):
        """
        Makes a post request to Basecamp api to complete a todo
        """
        complete_todo_endpoint = self.complete_endpoint.format(self.acc_id, project_id, todo_id)
        post_response = requests.post(complete_todo_endpoint, headers=self.header)
        if post_response.status_code != 204:
            raise Exception("bad requests")
        return {"success" : "ok"}

    @staticmethod
    def calculate_points():
        """ Cacluate the points for each team"""
        return 100 + 10
