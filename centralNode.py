from flask import Flask, jsonify, request
import requests
import os
from utils.uploadDocuments import uploadFile
from config import *
app = Flask(__name__)

nodesMetadata = {}
NODE_COUNTER = 0
workDoneNodes = set()

@app.route('/api/centralNode/register', methods= ['POST'])
def registerNode():
    data = request.json

    if not data:
        return jsonify({'Error': 'No Data Provided'})
    try:
        ip_address = request.remote_addr
        
        global NODE_COUNTER
        NODE_COUNTER = NODE_COUNTER + 1

        print(data.get('message'))

        nodesMetadata.update({NODE_COUNTER:(ip_address, '500'+str(NODE_COUNTER))})
        
        print(f'Node Added with ID {NODE_COUNTER}')

        response = jsonify({
            'NodeID' : NODE_COUNTER
        })

        return response, 200
    except Exception as e:
        response = jsonify({'Error' :f'Error Occured: {e}'})
        return response, 500
    

@app.route('/api/centralNode/mapReduce', methods=['POST'])
def mapReduce():
    print("started")
    #send the files equally
    doc_path = os.path.join(BASE_DIR, 'documents')
    file_paths = os.listdir(doc_path)
    totalFiles = len(file_paths)

    file_status = {}

    for i in range(0, totalFiles):
        node_number = (i % NODE_COUNTER) + 1
        ip_address = str(nodesMetadata[node_number][0])
        port_no = str(nodesMetadata[node_number][1])

        url = f'http://{ip_address}:{port_no}/api/childNode/{node_number}/upload'
        response = uploadFile(os.path.join(doc_path, file_paths[i]), url, file_paths[i])
        if(response.status_code == 200):
            file_status.update({file_paths[i]:'Success'})
        else:
            file_status.update({file_paths[i]:'Failed'})
    
    for i in range(0, NODE_COUNTER):
        ip_address = str(nodesMetadata[i+1][0])
        port_no = str(nodesMetadata[i+1][1])
        url = f'http://{ip_address}:{port_no}/api/childNode/{i+1}/mapReduce'

        requests.post(url=url, json=nodesMetadata)
        print(f'Node {i+1} started')
        

    return jsonify(file_status), 200
    

@app.route('/api/centralNode/workDone', methods = ['POST'])
def workDone():
    global workDoneNodes
    try:
        data = request.get_json()
        '''
        data = {
        'message':'job done',
        'NodeID':{NodeID}
        }
        '''
        workDoneNodes.add(data.get('NodeID'))
        print(f"Work Completed by {data.get('NodeID')}")

        if len(workDoneNodes) == NODE_COUNTER:
            print("All nodes have reported work completion.")
            # Reset state for potential future MapReduce cycles
            workDoneNodes.clear()
            return jsonify({'message': 'All nodes have completed their tasks'}), 200
        
        return jsonify({'message': 'Work completion tracked'}), 200
    except Exception as e:
        print(e)
        return jsonify(f'error: {str(e)}'), 500
    


if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000, debug=True)
    
