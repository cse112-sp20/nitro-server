import os
import requests
from flask import Flask, request, session, redirect, jsonify
from dotenv import load_dotenv
from Basecamp import Basecamp

"""
Load the enviornment variables and initialize flask object
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'shh'
load_dotenv() #Load enviornment variables

# Enciornment Variables
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
ACCOUNT_ID = os.environ.get('ACCOUNT_ID')

"""
Use this route to get redirected to basecamp
"""
@app.route('/login')
def login():
    authorization_url = 'https://launchpad.37signals.com/authorization/new?type=web_server&client_id={}&redirect_uri={}'.format(CLIENT_ID, REDIRECT_URI)
    return redirect(authorization_url), 302

@app.route('/task')
def home():
    return "hello" 

@app.route('/somename')
def somefunct():
    res = {"name" : "phuc"}
    return jsonify(res)


# Login route gets redirected here
@app.route('/get_token', methods=['GET'])
def get_Token():
    #print(request)
    code = request.args.get('code')
    token_url = 'https://launchpad.37signals.com/authorization/token?type=web_server&client_id={}&redirect_uri={}&client_secret={}&code={}'.format(CLIENT_ID,REDIRECT_URI, CLIENT_SECRET, code)
    r = requests.post(token_url)
    if r.status_code == 200:
        token = r.json()['access_token'].encode('ascii', 'replace') #The Access token right here
        """
        #Make a request
        url = 'https://3.basecampapi.com/4514340/projects.json'
        print(token)
        r = requests.get(url, headers={"Authorization": "Bearer " + token})
        res = r.json()
        """
        basecamp = Basecamp(token, ACCOUNT_ID)
        return jsonify(basecamp.jsonDump())
    return "Failure"

if __name__ == '__main__':
    app.run('localhost', debug=True)
