import json
from __main__ import app

data = {'Team':'Nitro', 'Name': 'Joe', 'Due_date' : '05/14/20',
        'assigned_to' : 'fill', 'Notes' : "please work", 'point' : 12}

@app.route('/task', methods=['GET'])
def getTask():
    return json.dumps(data)

@app.route('/update', methods=['POST'])
def updateTask():
    return 'Soon to be completed'

    