# pylint: disable=line-too-long
"""
Entry point for application
"""
import os
import requests
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from pymongo import MongoClient
from basecamp import Basecamp, parse_user_from_json

# Initializing the database access objects
client = MongoClient("mongodb://0.0.0.0:27017")
db = client.Basecamp
#Create collections within db
auth = db.Auth

# Configurations
APP = Flask(__name__)
APP.config['SECRET_KEY'] = 'shh'
load_dotenv()
cors = CORS(APP)

# Enviornment Variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
ACCOUNT_ID = os.environ.get('ACCOUNT_ID')

# Endpoints
AUTH_BASE = 'https://launchpad.37signals.com/authorization/new?type=web_server&client_id={}&redirect_uri={}'
TOKEN_BASE = 'https://launchpad.37signals.com/authorization/token?type=web_server&client_id={}&redirect_uri={}&client_secret={}&code={}'

@APP.route('/')
@cross_origin()
def home():
    """
    base route
    """
    return jsonify({"status": 200})

@APP.route('/login')
@cross_origin()
def login():
    """
    Logs the user in and stores a new authentication token in their session
    """
    authorization_url = AUTH_BASE.format(CLIENT_ID, REDIRECT_URI)
    return redirect(authorization_url), 302

@APP.route('/tasks')
@cross_origin()
def get_task():
    """
    Returns json dump of all of basecamp data
    """
    auth_object = auth.find_one()
    if not auth_object:
        return "no token found", 400
    token = auth_object["Auth"]
    basecamp = Basecamp(token, ACCOUNT_ID)
    return jsonify(basecamp.json_dump())

@APP.route('/delete', methods=['POST', 'GET'])
@cross_origin()
def delete_task():
    """
    Delete tasks
    """
    auth_object = auth.find_one()
    if not auth_object:
        return "no token found", 400
    token = auth_object["Auth"]

    # Get the id of the todo item we want to delete and the id of the project
    todo_id = request.args.get('task')
    project_id = request.args.get('project')

    # If either one is not give then return 400
    if not todo_id or not project_id:
        return "did not give task or project id", 400

    basecamp = Basecamp(token, ACCOUNT_ID)
    basecamp.delete_task(project_id, int(todo_id))
    return "hi"

@APP.route('/complete', methods=['POST', 'GET'])
@cross_origin()
def complete_task():
    """
    Marks a task as complete
    @param todo: id of the todo item to be completed
    @param proejct: id of the project todo is located in
    """
    auth_object = auth.find_one()
    if not auth_object:
        return "no token found", 400
    token = auth_object["Auth"]

    # Get the id of the todo item we want to delete and the id of the project
    todo_id = request.args.get('task')
    project_id = request.args.get('project')

    # If either one is not give then return 400
    if not todo_id or not project_id:
        return "bad request", 400

    basecamp = Basecamp(token, ACCOUNT_ID)
    basecamp.complete_task(project_id, todo_id)
    return "good", 200

# Login route gets redirected here
@APP.route('/get_token', methods=['GET'])
@cross_origin()
def get_token():
    """
    redirect uri to get the auth token
    """
    code = request.args.get('code')
    token_url = TOKEN_BASE.format(CLIENT_ID, REDIRECT_URI, CLIENT_SECRET, code)
    token_response = requests.post(token_url)
    print(token_response)
    if token_response.status_code == 200:
        token = token_response.json()['access_token'].encode('ascii', 'replace') #The Access token right here
        auth.delete_many({})
        auth.insert_one({"Auth" : token.decode("utf-8")})
        basecamp = Basecamp(token.decode("utf-8"), ACCOUNT_ID)
        return redirect("https://3.basecamp.com/" + str(basecamp.acc_id))
    return "bad request", 400

@APP.route('/clear_completed', methods=['DELETE'])
@cross_origin()
def clear_completed():
    """
    Resets the completed tasks from the database
    """
    #token = request.headers.get('Authorization')
    auth_object = auth.find_one()
    if not auth_object:
        return "no token found", 400
    token = auth_object["Auth"]
    basecamp = Basecamp(token, ACCOUNT_ID)
    basecamp.uncomplete_all()
    return "uncompleted"

@APP.route('/logout')
@cross_origin()
def logout():
    """
    logout route that deletes every auth token from basecamp
    """
    auth.delete_many({})
    return "logged out"

@APP.route('/users')
@cross_origin()
def get_user():
    """
    Returns user profile dictionary parsed from json dump
    """
    auth_object = auth.find_one()
    if not auth_object:
        return "no token found", 400
    token = auth_object["Auth"]
    basecamp = Basecamp(token, ACCOUNT_ID)
    return jsonify(parse_user_from_json(basecamp.json_dump()))

if __name__ == '__main__':
    APP.run('0.0.0.0', port=8000, debug=True)
