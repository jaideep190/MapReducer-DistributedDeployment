import requests

CENTRAL_URL = "http://192.168.31.24:5000/api/centralNode/register"

def Register():
    data = {'message':'child_registration'}

    try:
        response = requests.post(CENTRAL_URL, json=data)
        
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
