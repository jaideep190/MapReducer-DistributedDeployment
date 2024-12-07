from flask import Flask, request, jsonify
from registerNode import Register
import sys
sys.path.append('../')
from config import *
from utils.mapper import mapper
from utils.shuffleSort import shuffleSort
from utils.reduce import reducer
from threading import Thread, Event

app = Flask('__name__')


#register the node
NodeID = Register()

if not NodeID:
    print('Node Creation Failed')

shuffle_sorted_pairs = {}
work_done = Event()

# start the api
@app.route('/api/childNode/<int:NodeID>', methods = ['POST'])
def startNode(NodeID):
    print('Child Node Started')
    return jsonify({'message': f'Node {NodeID} Started'})


@app.route('/api/childNode/<int:NodeID>/upload', methods = ['POST'])
def get_documents(NodeID):
    try:
        file = request.files['file']
        
        output_dir = os.path.join(os.path.dirname(__file__), f'../uploads_{NodeID}')
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, file.filename)
        file.save(output_path)
        print(f'{NodeID} recieved {file.filename}')

        return "File uploaded success", 200
    except Exception as e:
        print(f'Error Occured : {e}')

        return "Upload Failed", 500




@app.route('/api/childNode/<int:NodeID>/mapReduce', methods = ['POST'])
def map_reduce(NodeID):
    print('Map Reduce Started')
    '''
    Expected Request keys
    documents
    '''
    global shuffle_sorted_pairs
    nodesMetadata = dict(request.get_json())
    print(nodesMetadata)
    documents_path = f'../uploads_{NodeID}'
    documents = os.listdir(documents_path)
    print(documents)
    
    #run the mapper on the documents
    key_value_pairs = []

    for index in documents:
        key_value_pairs = key_value_pairs + mapper(os.path.join(documents_path, index), index)
    
    print('Intermediate Key Value Pairs :')
    print(key_value_pairs)
    print('-'*10)
    #perform shuffle and sort
    def shuffleSortWoker(key_value_pairs, nodesMetadata, shuffle_sorted_pairs, NodeID):
        shuffleSort(key_value_pairs, nodesMetadata, shuffle_sorted_pairs, NodeID)
        print(shuffle_sorted_pairs)
        work_done.set()
    
    thread = Thread(
        target=shuffleSortWoker,
        args=(key_value_pairs, nodesMetadata, shuffle_sorted_pairs, NodeID)
    )
    thread.start()

    return jsonify({"message": "MapReduce job started, shuffleSort running in the background."}), 200

@app.route('/api/childNode/<int:NodeID>/getPairs', methods = ['POST'])
def updateShuffleSortPairs(NodeID):
    global shuffle_sorted_pairs
    try:
        item = request.get_json()
        if item and 'key' in item and 'value' in item:
            key, value = item['key'], item['value']
            if key in shuffle_sorted_pairs:
                shuffle_sorted_pairs[key].append(value)
            else:
                shuffle_sorted_pairs[key] = [value]

            print('Updated shuffle_sorted_pairs:', shuffle_sorted_pairs)
            return jsonify({'message': 'Pair received'}), 200
        else:
            return jsonify({'error': 'Invalid request'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    if NodeID:
        port_no = int(('500'+str(NodeID)))
        app.run(host='0.0.0.0', port=port_no)