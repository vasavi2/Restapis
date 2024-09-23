
from flask import Flask, request, jsonify
from flask import Response
from flask_cors import CORS
import psycopg2.pool

import psycopg2
import io
import csv
app = Flask(__name__)
CORS(app)

print("hi")
@app.route('/receive_features', methods=['POST'])
def receive_data():
    try:
        if request.method == 'POST':
            received_data = request.json  # Get the JSON data sent from frontend
            print(received_data)  # Print received data for testing purposes

#             print(list(received_data.values()))
            return jsonify(received_data)
        else:
            return jsonify({"message": "Invalid request method"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error processing data"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9003, debug=True)