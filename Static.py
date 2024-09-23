import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.pool
app = Flask(__name__)

conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")

class InputFile8:

    def __init__(self):
        pass


    def GetStatic(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from  static_table_info) json_array;"
        cur.execute(query)

        # Fetch the data from the query
        data = cur.fetchall()

        # Convert the data into JSON
        for row in data:
            data_str = str(row)[1:-2]

            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            # Close the connection
            conn.close()

    def GetCpsi(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from  _2k1701_cps1_raw) json_array"
        cur.execute(query)

        # Fetch the data from the query
        data = cur.fetchall()

        # Convert the data into JSON
        for row in data:
            data_str = str(row)[1:-2]

            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            # Close the connection
            conn.close()


