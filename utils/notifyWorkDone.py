import requests
from flask import jsonify
from config import *

api = CENTRAL_URL + '/workDone'

def notifyCentralNode(NodeID):
    try:
        data = ({
            'message':'Job Done',
            'NodeID':NodeID
        })

        response = requests.post(url=api, json=data)
        if(response.status_code == 200):
            print(f'Work Done by {NodeID} notified')
        else:
            print(f'Failed to notify by node {NodeID}')
    except Exception as e:
        print(str(e))
        