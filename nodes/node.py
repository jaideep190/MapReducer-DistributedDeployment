from flask import Flask, request, jsonify
from registerNode import Register

app = Flask('__name__')


#register the node
NodeID = Register()

if not NodeID:
    print('Node Creation Failed')


# start the api
@app.route('/api/childNode/<int:NodeID>', methods = ['POST'])
def startNode(NodeID):
    print('Child Node Started')
    return jsonify({'message': f'Node {NodeID} Started'})


if __name__ == '__main__':
    if NodeID:
        app.run(host='0.0.0.0', port=5001)