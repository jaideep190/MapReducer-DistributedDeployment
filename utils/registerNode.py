import requests
from config import *

api = CENTRAL_URL + '/register'
def Register():
    data = {'message':'child_registration'}

    try:
        response = requests.post(api, json=data)
        
        if(response.status_code == 200):
            data = response.json()
            NodeID = data.get('NodeID')
            print(f'Node Registered with ID {NodeID}')
            return NodeID
        else:
            print('Central Node Error')

    except Exception as e:
        print(f'Error : {e}')
        return None
