import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify

import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")


class InputFile7:

    def __init__(self):
        pass

    def GetModelConfig_Table(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from model_config) json_array;"
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

    def insert_ModelConfig_Data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        query1 = '''alter table model_config alter column update_time_stamp set default current_timestamp '''
        cur.execute(query1)

        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(modelconfig_id), 0) FROM model_config")
        max_id = cur.fetchone()[0]
        modelconfig_id = max_id + 1

        cur.execute("insert into model_config(modelconfig_id,thresholdconfig_id,cluster_id,cluster_name) "
        "values(%s,%s,%s,%s)",
        (
            modelconfig_id,
            data["thresholdconfig_id"],
            data["cluster_id"], data["cluster_name"],))

        conn.commit()
        cur.execute("(select modelconfig_id,cluster_name from model_config order by modelconfig_id  desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1



    def Update_ModelConfigData(self):
        global conn
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            data_dict = isinstance(data, dict)
            json_data = request.json
            json_length = len(json_data)
            input_param = request.get_json()
            modelconfig_id = input_param.get("modelconfig_id")
            cluster_id = input_param.get("cluster_id")
            cluster_name = input_param.get("cluster_name")

            if data_dict == True:
                if json_length==4:
                    cluster_id = data["cluster_id"]
                    cluster_name = data["cluster_name"]
                    modelconfig_id = data["modelconfig_id"]
                    thresholdconfig_id=data["thresholdconfig_id"]

                    query ="update model_config  set cluster_id = %s,cluster_name = %s where modelconfig_id = %s and thresholdconfig_id=%s"
                    attribute_values=(cluster_id,cluster_name,modelconfig_id,thresholdconfig_id)


                elif json_length==3:
                    cluster_id = data["cluster_id"]
                    cluster_name = data["cluster_name"]
                    modelconfig_id = data["modelconfig_id"]
                    query ="update model_config  set cluster_id = %s,cluster_name = %s where modelconfig_id = %s"
                    attribute_values=(cluster_id,cluster_name,modelconfig_id)

                elif modelconfig_id and cluster_id :
                    query ="update model_config  set cluster_id = %s where modelconfig_id = %s"
                    attribute_values=(cluster_id,modelconfig_id)


                elif modelconfig_id and cluster_name :
                    query ="update model_config  set cluster_name = %s where modelconfig_id = %s"
                    attribute_values=(cluster_name,modelconfig_id)



                cur.execute(query,attribute_values)

                conn.commit()
                # return json.dumps({"json_length":json_length})
                return "Sucessfully Updated"
                conn.close()


    def GetModel_limit(self):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select * from model_config limit %s offset %s) json_array",
            (limit, offset))

        results = cur.fetchall()
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("SELECT COUNT(*) FROM model_config")
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response



