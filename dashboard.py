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
class InputFile10:

    def __init__(self):
        pass
    def insert_dashboard_data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

            cur.execute("SELECT COALESCE(MAX(taskno), 0) FROM dashboard")
            max_id = cur.fetchone()[0]
            sensorgroup_id = max_id + 1

        cur.execute("insert into dashboard(taskno,pipilinename,created_no,status,owner,description,remark) "
        "values(%s,%s,%s,%s,%s,%s,%s)",
        (
            sensorgroup_id,data["PipilineName"],data["Created_on"], data["Status"],data["Owner"],data["Description"],data["remark"],))

        conn.commit()
        return "Successfully Inserted"







    def GetDashboard(self):
        global conn

        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from dashboard order by taskno) json_array"
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









