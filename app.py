import os
import requests
from flask import Flask, request, session, redirect, url_for
from dotenv import load_dotenv

"""
Load the enviornment variables and initialize flask object
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'shh'
load_dotenv() #Load enviornment variables
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
auth_base_url = 'https://launchpad.37signals.com/authorization/new'
redirect_uri = os.environ.get('REDIRECT_URI')

"""
Use this route to get redirected to basecamp
"""
@app.route('/')
def home():
    if 'token' in session:
        return "logged in"
    return "not logged in"
    
@app.route('/login')
def login():
    authorization_url = 'https://launchpad.37signals.com/authorization/new?type=web_server&client_id={}&redirect_uri={}'.format(client_id, redirect_uri)
    return redirect(authorization_url)

# Login route gets redirected here
@app.route('/get_token', methods=['GET'])
def get_Token():
    code = request.args.get('code')
    token_url = 'https://launchpad.37signals.com/authorization/token?type=web_server&client_id={}&redirect_uri={}&client_secret={}&code={}'.format(client_id,redirect_uri, client_secret, code)
    r = requests.post(token_url)
    if r.status_code == 200:
        token = r.json()['access_token'].encode('ascii', 'replace') #The Access token right here
        session['token'] = token
        return redirect(url_for('home'))
    else:
        return "sad"

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('localhost', debug=True)

