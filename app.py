"""
Entry point for application
"""
import os
import requests
from flask import Flask, request, session, redirect, jsonify
from dotenv import load_dotenv
from Basecamp import Basecamp

#Configurations
app = Flask(__name__)
app.config['SECRET_KEY'] = 'shh'
load_dotenv() 

# Enviornment Variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
ACCOUNT_ID = os.environ.get('ACCOUNT_ID')

"""
Use this route to get redirected to basecamp
"""
@app.route('/login')
def login():
    """
    Logs the user in and stores a new authentication token in their session
    """
    authorization_url = 'https://launchpad.37signals.com/authorization/new?type=web_server&client_id={}&redirect_uri={}'.format(CLIENT_ID, REDIRECT_URI)
    return redirect(authorization_url), 302

@app.route('/tasks')
def get_task():
    if 'AUTH_TOKEN' not in session:
        return redirect('/login')
    basecamp = Basecamp(session.get('AUTH_TOKEN'), ACCOUNT_ID)
    return jsonify(basecamp.json_dump()) 

@app.route('/complete', methods=['POST', 'GET'])
def complete_task():
    if 'AUTH_TOKEN' not in session:
        return redirect('/login')

    # Get the id of the todo item we want to delete and the id of the project
    todo_id = request.args.get('todo')
    project_id = request.args.get('project')

    # If either one is not give then return 400
    if not todo_id or not project_id:
        return "bad request", 400

    basecamp = Basecamp(session.get('AUTH_TOKEN'), ACCOUNT_ID)
    basecamp.complete_task(project_id, todo_id)
    return "good", 200

# Login route gets redirected here
@app.route('/get_token', methods=['GET'])
def get_Token():
    code = request.args.get('code')
    token_url = 'https://launchpad.37signals.com/authorization/token?type=web_server&client_id={}&redirect_uri={}&client_secret={}&code={}'.format(CLIENT_ID,REDIRECT_URI, CLIENT_SECRET, code)
    r = requests.post(token_url)
    if r.status_code == 200:
        token = r.json()['access_token'].encode('ascii', 'replace') #The Access token right here
        session['AUTH_TOKEN'] = token
        base_camp = Basecamp(token, ACCOUNT_ID)
        return jsonify(base_camp.json_dump())
    return "Failure"

if __name__ == '__main__':
    app.run('localhost', debug=True)
