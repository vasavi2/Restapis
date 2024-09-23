import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify

import psycopg2
app = Flask(__name__)
conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")


class InputFile4:

    def __init__(self):
        pass

    # def insert_sensorgroup_data(self):
    #     global conn
    #     # Open cursor to perform database operation
    #     cur = conn.cursor()
    #     cur_insert = conn.cursor()
    #     if request.method == 'POST':
    #         data = request.get_json()
    #         query1 = '''alter table sensorgroup_master alter column update_time_stamp set default current_timestamp '''
    #         cur.execute(query1)
    #
    #         cur.execute("select * from asset_master")
    #
    #         cur_insert.execute(
    #             "insert into sensorgroup_master(sensorgroup_id,asset_id,name,component,endpoint) "
    #             "values(((SELECT sensorgroup_id FROM sensorgroup_master ORDER BY sensorgroup_id DESC LIMIT 1) + 1),%s,%s,%s,%s)",
    #             (
    #
    #                 data["asset_id"],data["name"],data["component"],data["endpoint"],))
    #
    #         conn.commit()
    #         cur.execute("(select sensorgroup_id,name from sensorgroup_master order by sensorgroup_id desc limit 1)")
    #         result = cur.fetchall()
    #
    #         dict1 = {}
    #         if result:
    #             key = str(result[0][0])
    #             value = str(result[0][1])
    #             dict1.update({key: value})
    #
    #             return dict1

    def insert_sensorgroup_data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        query1 = '''alter table sensorgroup_master alter column update_time_stamp set default current_timestamp '''
        cur.execute(query1)

        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(sensorgroup_id), 0) FROM sensorgroup_master")
        max_id = cur.fetchone()[0]
        sensorgroup_id = max_id + 1

        cur.execute("insert into sensorgroup_master(sensorgroup_id,asset_id,name,component,endpoint) "
        "values(%s,%s,%s,%s,%s)",
        (
            sensorgroup_id,
            data["asset_id"],
            data["name"], data["component"],data["endpoint"],))


        cur.execute("insert into static_table_info(id,table_name) select (select coalesce(max(sensorgroup_id),0)+1 from sensorgroup_master),endpoint from sensorgroup_master order by sensorgroup_id desc limit 1  ")

        conn.commit()
        cur.execute("(select sensorgroup_id,name from sensorgroup_master order by sensorgroup_id desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1

    def insert_sensorgroup_data2(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

        # Your logic to determine endpoint based on name
        endpoint_prefix = "_"
        if "name" in data:
            name = data["name"].lower()
            if "compressor dry gas seal" in name:
                endpoint = endpoint_prefix + "CDGS"
            elif "compressor journal bearing" in name:
                endpoint = endpoint_prefix + "CJB"
            elif "compressor lube oil bearing" in name:
                endpoint = endpoint_prefix + "CLOB"
            else:
                # Default endpoint logic if name doesn't match any predefined condition
                words=name.split()
                endpoint = endpoint_prefix + "".join(word[0].upper() for word in words)

        # Rest of your code remains unchanged
        query1 = '''alter table sensorgroup_master alter column update_time_stamp set default current_timestamp '''
        cur.execute(query1)

        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(sensorgroup_id), 0) FROM sensorgroup_master")
        max_id = cur.fetchone()[0]
        sensorgroup_id = max_id + 1

        cur.execute("insert into sensorgroup_master(sensorgroup_id,asset_id,name,component,endpoint) "
                    "values(%s,%s,%s,%s,%s)",
                    (
                        sensorgroup_id,
                        data["asset_id"],
                        data["name"], data["component"], endpoint,))



        # cur.execute("insert into static_table_info(id) select (select coalesce(max(sensorgroup_id),0)+1 from sensorgroup_master) from sensorgroup_master order by sensorgroup_id desc limit 1  ")


        conn.commit()
        cur.execute("(select sensorgroup_id,name from sensorgroup_master order by sensorgroup_id desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1
        # ... (rest of your code)



    def GetSensor(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select * from sensorgroup_master order by sensorgroup_id  ) json_array",
            )

        # Fetch the data from the query
        data = cur.fetchall()

        for row in data:
            data_str = str(row)[1:-2]

            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            # Close the connection
            conn.close()

    def GetSensor_with_asset(self, asset_id):
        global conn
        cur = conn.cursor()
        try:
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            cur.execute(
                "select array_to_json(array_agg(row_to_json(json_array))) from (select * from sensorgroup_master where asset_id = %s order by sensorgroup_id  limit %s offset %s ) json_array",
                (asset_id, limit, offset))

            results = cur.fetchall()
            for row in results:
                data_str = str(row)[1:-2]
                json_array = json.loads(json.dumps(data_str))
                json_obj = eval(json_array)
                cur.execute("select count(*) from sensorgroup_master where asset_id = %s",
                            (asset_id,))
                total_count = cur.fetchone()[0]
                response = jsonify(json_obj)
                response.headers.add('x-total-count', total_count)
                response.headers["Access-Control-Expose-Headers"] = "x-total-count"
                conn.commit()

                return response
        except Exception as e:
            conn.rollback()
            print("Error:",e)




    def Update_SensorData(self):
        global conn
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            data_dict = isinstance(data, dict)
            json_data = request.json
            json_length = len(json_data)
            input_param = request.get_json()

            sensorgroup_id = input_param.get("sensorgroup_id")
            asset_id = input_param.get("asset_id")
            name = input_param.get("name")
            component = input_param.get("component")
            endpoint = input_param.get("endpoint")

            if data_dict == True:
                if json_length==5:
                    asset_id=data["asset_id"]
                    sensorgroup_id=data["sensorgroup_id"]
                    name=data["name"]
                    component=data["component"]
                    endpoint=data["endpoint"]
                    query ="update sensorgroup_master  set name = %s,component=%s,endpoint=%s where asset_id = %s and sensorgroup_id=%s"
                    attribute_values=(name,component,endpoint,asset_id,sensorgroup_id)


                elif json_length==4:
                    asset_id=data["asset_id"]
                    sensorgroup_id=data["sensorgroup_id"]
                    name=data["name"]
                    component=data["component"]
                    query="update sensorgroup_master  set name = %s,component=%s where asset_id = %s and sensorgroup_id=%s"
                    attribute_values=(name,component,asset_id,sensorgroup_id)

                elif sensorgroup_id and asset_id and name:
                    query = "update sensorgroup_master  set name = %s where asset_id = %s and sensorgroup_id=%s"
                    attribute_values = (name,asset_id,sensorgroup_id)

                elif sensorgroup_id and asset_id and component:
                    query = "update sensorgroup_master  set component = %s where asset_id = %s and sensorgroup_id=%s"
                    attribute_values = (component,asset_id,sensorgroup_id)

                elif sensorgroup_id and asset_id and endpoint:
                    query = "update sensorgroup_master  set endpoint = %s where asset_id = %s and sensorgroup_id=%s"
                    attribute_values = (endpoint,asset_id,sensorgroup_id)




                cur.execute(query,attribute_values)

                conn.commit()
                # return json.dumps({"json_length":json_length})
                return "Sucessfully Updated"
                conn.close()

    def DeleteSensor(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_del = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            cur_del.execute("delete from sensorgroup_master where asset_id=%s and sensorgroup_id=%s", (data["asset_id"],data["sensorgroup_id"],))
        conn.commit()
        return "Successfully Delete"