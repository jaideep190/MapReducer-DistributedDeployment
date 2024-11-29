from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/node1', methods = ['POST'])
def handle_post_request():
    data = request.json
    if not data:
        return jsonify({"error": "No Json Data Provided"}), 400
    
    response = {
        "status" : "Success node 1"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)