from flask import Flask, request, jsonify,request
from flask import Response
from flask_cors import CORS
import psycopg2.pool
import json

import psycopg2
import io
import csv
app = Flask(__name__)
CORS(app)
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="AHF_Project",
    password="root",
    user="postgres")
class InputFile12:

    def __init__(self):
        pass

    def insert_workspace_data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()

        if request.method == 'POST':
            data = request.get_json()

            cur.execute("SELECT COALESCE(MAX(id), 0) FROM workspace")
            max_id = cur.fetchone()[0]
            sensorgroup_id = max_id + 1

        cur.execute("insert into workspace(id,workspaceName,Screenimage) "
        "values(%s,%s,%s)",
        (
            sensorgroup_id,data["workspaceName"],data["Screenimage"],))
        conn.commit()
        return "Successfully Inserted"


    def GetWorkspace(self):
        global conn

        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from workspace) json_array"
        cur.execute(query)

        # Fetch the data from the query
        data = cur.fetchall()
        # Convert the data into JSON
        for row in data:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            conn.close()









