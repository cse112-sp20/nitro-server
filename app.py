from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import requests, json

# Enable Cors
# We need this because the browser throws errors if we don't have it
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#Connect to MongoDB instance
#Note Mongo will create the database if it does not exist
client = MongoClient("mongodb://0.0.0.0:27017") #Specify our host
db = client.testdb #specify which db to use (in our case it is testdb)
issues = db.test_collections #Within each db we have collections, choose the collection named 'test_collection'

"""
Client will call this endpoint, which will call another endpoint (github api) and return the result to the client
"""
@app.route('/import', methods=['POST'])
@cross_origin()
def run():
    # Requests require an access token
    url = "https://api.github.com/repos/112-test/test/issues"
    token = "token e0551eae9ffbcde9b6d83183eafff6542e3f35a0"
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
    #Return JSON to the user
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
    #Request.args are parameters that the client will send to us
    id = int(request.args.get('id'))
    print("deleteing with id {}".format(id))
    issues.delete_many({"id": id});
    return "bye", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
