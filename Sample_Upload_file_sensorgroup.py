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
@app.route('/upload', methods=['POST'])
def receive_data():
    try:
        if request.method == 'POST':
            print("received data")
            csv_file = request.files['file']
            csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
            print("csv_data",csv_data)
            for row in csv_data:
                print("data",row)

            return jsonify({'message': 'PlantData inserted successfully'}), 200
        else:
            return jsonify({"message": "Invalid request method"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error processing data"}), 500


# if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=9005, debug=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9003, debug=False)