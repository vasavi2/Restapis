# from flask import Flask, request, jsonify,request
# from flask import Response
# from flask_cors import CORS
# import psycopg2.pool
#
# import psycopg2
# import io
# import csv
# app = Flask(__name__)
# CORS(app)
#
# @app.route('/receive_data', methods=['GET','POST'])
# def create_table():
#     try:
#         # if request.method=="POST":
#         data = request.json
#         return jsonify({"message":"data recieved sucessfully"})
#
#     except (Exception, psycopg2.Error) as error:
#
#         print("Error:", error)
#
#         return 'Failed to create table', 500
#
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=9005, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

print("hello")
@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        if request.method == 'POST':
            received_data = request.json  # Get the JSON data sent from frontend
            print(received_data)  # Print received data for testing purposes
            received_data['age']=str(int(received_data['age'])+10)
            print(received_data)
            # print(list(received_data.values()))
            return jsonify(received_data)
        else:
            return jsonify({"message": "Invalid request method"})
    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Error processing data"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9007, debug=True)