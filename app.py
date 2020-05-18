# pylint: disable=line-too-long
"""
Entry point for application
"""
import os
import requests
from flask import Flask, request, session, redirect, jsonify, url_for, abort
from dotenv import load_dotenv
from Basecamp import Basecamp
from flask_cors import CORS, cross_origin

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
    if 'AUTH_TOKEN' in session:
        return "logged in"
    return jsonify({"status" : "not logged in"}), 200

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
    if 'AUTH_TOKEN' not in session:
        return redirect('/login')
    basecamp = Basecamp(session.get('AUTH_TOKEN'), ACCOUNT_ID)
    return jsonify(basecamp.json_dump())

@APP.route('/complete', methods=['POST', 'GET'])
@cross_origin()
def complete_task():
    """
    Marks a task as complete
    @param todo: id of the todo item to be completed
    @param proejct: id of the project todo is located in
    """
    if 'AUTH_TOKEN' not in session:
        return redirect('/login')

    # Get the id of the todo item we want to delete and the id of the project
    todo_id = request.args.get('task')
    project_id = request.args.get('project')

    # If either one is not give then return 400
    if not todo_id or not project_id:
        return "bad request", 400

    basecamp = Basecamp(session.get('AUTH_TOKEN'), ACCOUNT_ID)
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
    print("the toke nresponse is {}".format(token_response.status_code))
    if token_response.status_code == 200:
        token = token_response.json()['access_token'].encode('ascii', 'replace') #The Access token right here
        session['AUTH_TOKEN'] = token
        base_camp = Basecamp(token, ACCOUNT_ID)
        # base_camp.init_webhook()
        return redirect(url_for('home'))
    return "lit"

@APP.route('/task_update_webhook', methods=['POST'])
@cross_origin()
def recieve_webhook():
    print("hello")

@APP.route('/logout')
@cross_origin()
def logout():
    session.pop('AUTH_TOKEN', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    APP.run('0.0.0.0',  port=80, debug=True)
