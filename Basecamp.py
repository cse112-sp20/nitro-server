
import requests
import json
"""
Helper methods to parse the basecamp api
"""
class Basecamp:
    def __init__(self, auth_token, acc_id):
        self.auth_token = auth_token
        self.acc_id = acc_id
        self.base_endpoint = "https://3.basecampapi.com/{}/projects.json".format(self.acc_id)
        self.header = {"Authorization": "Bearer " + self.auth_token}
        r = requests.get(self.base_endpoint, headers=self.header)
        if r.status_code != 200:
            raise Exception("unabl to reach json api status code:{}".format(r.status_code))
        else:
            self.json_dump = r
    """
    Gets a dump of the json that for the front-endj
    """
    def jsonDump(self):
        acc_obj = {}
        acc_obj['account_id'] = self.acc_id
        #print(self.json_dump.content)
        acc_obj['teams'] = self.getTeams()
        return acc_obj

    """
    Returns a list of dictionary of team objects
    """
    def getTeams(self):
        data = json.loads(self.json_dump.content)
        team_res = []
        for projects in data:
            if(projects['purpose'] == 'team'):
                team = {}
                team['name'] = projects['name']
                team['project_id'] = projects['id']
                team['todoset_id'] = [item['id'] for item in projects['dock'] if item['name'] == 'todoset' ][0]
                team['task_list'] = self.getTaskList([item['url']  for item in projects['dock'] if item['name'] == 'todoset' ][0])
                team_res.append(team)
        return team_res

    """
    Generate List of todolists
    @todoset_endpoint: list of todoset url endpoints
    """
    def getTaskList(self, taskset_endpoint):
        taskset_response = requests.get(taskset_endpoint, headers=self.header)
        if taskset_response.status_code != 200:
            raise Exception("Failed to fetch task list at endpint {}".format(taskset_endpoint))    
        
        #Each project has multiple todo lists
        result_list = []
        task_set_data = json.loads(taskset_response.content)

        # Get the task_lists from task_set url
        task_list_url = task_set_data['todolists_url']
        task_list_response = requests.get(task_list_url, headers=self.header)
        assert(task_list_response.status_code == 200)
        
        # Add tasklist objects
        for task_list in json.loads(task_list_response.content):
            task_list_elem = {}
            task_list_elem['task_list_id'] = task_list['id']
            task_list_elem['description'] = task_list['description']
            task_list_elem['task_list_name'] = task_list['name']
            task_list_elem['parent_id'] = task_list['parent']['id']
            task_list_elem['parent_project'] = task_list['bucket']['name']
            task_list_elem['tasks'] = self.getTask(task_list_elem['todos_url'])
            result_list.append(task_list_elem)
        return result_list

    """
    Get the individual tasks for each task list
    """
    def getTask(self, todos_url):
        print(todos_url)
        return []

        
