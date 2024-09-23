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


class InputFile3:

    def __init__(self):
        pass

    # def insert_asset_data(self):
    #     global conn
    #     # Open cursor to perform database operation
    #     cur = conn.cursor()
    #     cur_insert = conn.cursor()
    #     if request.method == 'POST':
    #         data = request.get_json()
    #
    #
    #         query1 = '''alter table asset_master alter column update_time_stamp set default current_timestamp '''
    #         cur.execute(query1)
    #         cur.execute("select * from plant_master")
    #
    #         cur_insert.execute(
    #             "insert into asset_master(id,plant_id,asset_tag,asset_name) "
    #             "values(((SELECT id from asset_master ORDER BY id DESC LIMIT 1)+1),%s,%s,%s)",
    #             (
    #                 data["plant_id"],
    #                 data["asset_tag"], data["asset_name"],))
    #
    #         conn.commit()
    #         cur.execute("(select id,asset_name from asset_master order by id desc limit 1)")
    #         result = cur.fetchall()
    #         dict1 = {}
    #         key = str(result[0][0])
    #         value = str(result[0][1])
    #         dict1.update({key: value})
    #         return dict1

    def insert_asset_data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        query1 = '''alter table asset_master alter column update_time_stamp set default current_timestamp '''
        cur.execute(query1)

        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(id), 0) FROM asset_master")
        max_id = cur.fetchone()[0]
        id = max_id + 1

        cur.execute("insert into asset_master(id,plant_id,asset_tag,asset_name) "
        "values(%s,%s,%s,%s)",
        (
            id,
            data["plant_id"],
            data["asset_tag"], data["asset_name"],))

        conn.commit()
        cur.execute("(select id,asset_name from asset_master order by id desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1


    def GetAsset_with_plant(self, plant_id):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        limit = request.args.get('limit')
        offset = request.args.get('offset')

        # Query the database
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select id,asset_name,asset_tag,update_time_stamp from asset_master where plant_id= %s limit %s offset %s) json_array",
            (plant_id,limit,offset,))


        results = cur.fetchall()
        print("result",results)
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("select count(*) from asset_master where plant_id = %s",
                        (plant_id,))
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response



    def GetAsset_with_plantIds(self,plant_id):
        global conn

        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select id,asset_name,asset_tag,update_time_stamp from asset_master where plant_id= %s ) json_array",
            (plant_id, ))

        # Fetch the data from the query
        data = cur.fetchall()
        # Convert the data into JSON
        for row in data:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            conn.close()





    def GetAsset(self):
        global conn

        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from asset_master) json_array"
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



    def Update_AssetData(self):
        global conn
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            data_dict = isinstance(data, dict)
            json_data = request.json
            json_length = len(json_data)

            input_param = request.get_json()

            id = input_param.get("id")
            asset_tag = input_param.get("asset_tag")
            asset_name = input_param.get("asset_name")

            if data_dict == True:
                if json_length==4:
                    asset_tag = data["asset_tag"]
                    asset_name = data["asset_name"]
                    id = data["id"]
                    plant_id=data["plant_id"]

                    query ="update asset_master  set asset_tag = %s,asset_name = %s where id = %s and plant_id=%s"
                    attribute_values=(asset_tag,asset_name,id,plant_id)


                elif json_length==3:
                    asset_tag = data["asset_tag"]
                    asset_name = data["asset_name"]
                    id = data["id"]
                    query ="update asset_master  set asset_tag = %s,asset_name = %s where id = %s"
                    attribute_values=(asset_tag,asset_name,id)

                elif id and asset_tag :
                    query ="update asset_master  set asset_tag = %s where id = %s"
                    attribute_values=(asset_tag,id)


                elif id and asset_name :
                    query ="update asset_master  set asset_name = %s where id = %s"
                    attribute_values=(asset_name,id)



                cur.execute(query,attribute_values)

                conn.commit()
                # return json.dumps({"json_length":json_length})
                return "Sucessfully Updated"
                conn.close()

                # cur.execute("update asset_master  set asset_tag = %s,asset_name = %s where id = %s",
                #             (data["asset_tag"],data["asset_name"], data["id"]))





    def DeleteAsset(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_del = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

            cur_del.execute(
                "delete from sensorgroup_master where asset_id in (select id from asset_master where id in (%s))",
                (data["id"],))
            cur_del.execute("delete from asset_master where id=%s", (data["id"],))

        conn.commit()
        return "Successfully Delete"
