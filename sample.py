# pylint: skip-file
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import requests, json

# Enable Cors
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Connect to MongoDB
client = MongoClient("mongodb://0.0.0.0:27017")
db = client.testdb
issues = db.test_collections

"""
imports issues by calling github api
"""
@app.route('/import', methods=['POST'])
@cross_origin()
def run():
    # Requests require an access token
    url = URL
    token = TOKEN
    params = {"Authorization": token}
    #r is type list(dict)
    r = requests.get(url, params).json()

    # Parse the list of issues and insert into the database
    for elem in r:
        # function to get only title, updated_at, or id keys from json
        def is_title_id_updated(key):
            return key == 'title' or key == 'updated_at' or key == 'id' or key == '_id';
        # insert element into the database
        issues.insert_one({key:val for key, val in elem.items() if is_title_id_updated(key)})
    return jsonify({"message": "ok"})

@app.route('/', methods=['GET'])
@cross_origin()
def hello():
    return "hello"

"""
Get issues from the database
"""
@app.route('/issues', methods=['GET'])
@cross_origin()
def getIssues():
    issue_list = issues.find()
    response = []
    for r in issue_list:
        obj = {}
        if 'title' in r:
            obj['title'] = r['title']
            obj['id'] = r['id']
            obj['updated_at'] = r['updated_at']
            response.append(obj)
    return jsonify(response)

"""
delete from the database with a given id
"""
@app.route('/delete', methods=['POST'])
@cross_origin()
def deleteItem():
    id = int(request.args.get('id'))
    print("deleteing with id {}".format(id))
    issues.delete_many({"id": id});
    return "bye", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
