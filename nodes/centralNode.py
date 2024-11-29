from flask import Flask, jsonify, request

app = Flask(__name__)

local_db = {}
NODE_COUNTER = 0

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
        local_db.update({ip_address:NODE_COUNTER})
        print(f'Node Added with ID {NODE_COUNTER}')
        
        response = jsonify({
            'NodeID' : NODE_COUNTER
        })

        return response, 200
    except Exception as e:
        response = jsonify({'Error' :f'Error Occured: {e}'})
        return response, 500
    




if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000, debug=True)
    
