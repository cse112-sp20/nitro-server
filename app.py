# pylint: disable=line-too-long
"""
Entry point for application
"""
import os
import requests
from flask import Flask, request, session, redirect, jsonify, url_for
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from basecamp import Basecamp


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
    token = request.headers.get('Authorization')
    if not token:
        return "no Auth token found", 401
    basecamp = Basecamp(token, ACCOUNT_ID)
    return jsonify(basecamp.json_dump())

@APP.route('/delete', methods=['POST', 'GET'])
def delete_task():
    """
    Delete tasks
    """
    token = request.headers.get('Authorization')
    if not token:
        return "no Auth token found", 401

    # Get the id of the todo item we want to delete and the id of the project
    todo_id = request.args.get('task')
    project_id = request.args.get('project')

    # If either one is not give then return 400
    if not todo_id or not project_id:
        return "did not give task or project id", 400

    basecamp = Basecamp(token, ACCOUNT_ID)
    basecamp.delete_task(project_id, todo_id)
    return "hi" 

@APP.route('/complete', methods=['POST', 'GET'])
@cross_origin()
def complete_task():
    """
    Marks a task as complete
    @param todo: id of the todo item to be completed
    @param proejct: id of the project todo is located in
    """
    token = request.headers.get('Authorization')
    if not token:
        return "no Auth token found", 401

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
    if token_response.status_code == 200:
        token = token_response.json()['access_token'].encode('ascii', 'replace') #The Access token right here
        return jsonify({"Authorization" : token.decode("utf-8")})
    return "bad request"

@APP.route('/clear_completed', methods=['DELETE'])
@cross_origin()
def clear_completed():
    """
    Resets the completed tasks from the database
    """
    token = request.headers.get('Authorization')
    if not token:
        return "no Auth token found", 401
    basecamp = Basecamp(token, ACCOUNT_ID)
    basecamp.uncomplete_all()
    return "uncompleted"

@APP.route('/logout')
@cross_origin()
def logout():
    """
    logs the current user out of the session
    """
    session.pop('AUTH_TOKEN', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    APP.run('0.0.0.0', port=80, debug=True)
