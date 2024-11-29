from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/centralNode', methods= ['POST'])
def initiate_map_reduce():
    data = request.json

    if not data:
        return jsonify({'Error': 'No JSON data'}), 400
    
    key = data.get('key')
    
    response = {
        'Status': 'Success',
        'key' : key
    }

    return jsonify(response), 200

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5000, debug=True)
    
