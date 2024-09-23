import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify

import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")


class InputFile6:

    def __init__(self):
        pass

    def insertAlgorithm_data(self):

                    global conn
                    # Parse the JSON data from the POST request
                    data = json.loads(request.data)

                    # Extract the values for asset_id and algorithm from the JSON data
                    asset_id = data.get("asset_id")
                    algorithm = data.get("algorithm")



                    # Open a cursor to perform database operations
                    cur = conn.cursor()

                    # Define the SQL statement with placeholders for asset_id and algorithm
                    sql = """INSERT INTO threshold_config (sensorgroup_id, algorithm)
                    SELECT sensorgroup_master.sensorgroup_id, %s
                    FROM sensorgroup_master
                    WHERE sensorgroup_master.asset_id = %s"""

                    # Execute the SQL statement with the values for asset_id and algorithm
                    cur.execute(sql, (algorithm, asset_id))

                    # Commit the changes to the database
                    conn.commit()

                    sql=" select t2.asset_id,t1.asset_name from asset_master as t1 join sensorgroup_master as t2 on t1.id=t2.asset_id  where t2.asset_id=%s limit 1"

                    cur.execute(sql,(asset_id,))

                    result = cur.fetchall()
                    dict1 = {}
                    if result:
                        key = str(result[0][0])
                        value = str(result[0][1])
                        dict1.update({key: value})

                        return dict1

                    # # Close the cursor and connection
                    # cur.close()
                    # conn.close()
                    # return "inserted"


    def insertThreshold_data(self):

                    global conn
                    # Parse the JSON data from the POST request
                    data = json.loads(request.data)

                    # Extract the values for asset_id and algorithm from the JSON data
                    k_best = data.get("k_best")
                    alert_level = data.get("alert_level")
                    warning_level=data.get("warning_level")
                    upper_limit=data.get("upper_limit")
                    lower_limit=data.get("lower_limit")
                    sensorgroup_id=data.get("sensorgroup_id")




                    # Open a cursor to perform database operations
                    cur = conn.cursor()

                    # Define the SQL statement with placeholders for asset_id and algorithm
                    sql = """update threshold_config set k_best=%s,alertlevel=%s,warninglevel=%s,upper_limit=%s,lower_limit=%s where sensorgroup_id=%s"""

                    # Execute the SQL statement with the values for asset_id and algorithm
                    cur.execute(sql, (k_best,alert_level,warning_level,upper_limit,lower_limit,sensorgroup_id))

                    # Commit the changes to the database
                    conn.commit()

                    # Close the cursor and connection
                    cur.close()
                    # conn.close()
                    return "updated"


    def GetThreshold_with_AssetID(self, asset_id):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        limit = request.args.get('limit')
        offset = request.args.get('offset')

        # Query the database
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select sensorgroup_id,name from sensorgroup_master where asset_id= %s limit %s offset %s) json_array",
            (asset_id,limit,offset))


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
            return response

    def GetThreshold(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from threshold_config where upper_limit is not null and lower_limit is not null) json_array;"
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

    def GetThreshold_Table(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select * from threshold_config) json_array;"
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

    def insert_Threshold_Data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        query1 = '''alter table threshold_config alter column update_time_stamp set default current_timestamp '''
        cur.execute(query1)

        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(thresholdconfig_id), 0) FROM threshold_config")
        max_id = cur.fetchone()[0]
        thresholdconfig_id = max_id + 1

        cur_insert.execute(
            "INSERT INTO threshold_config (thresholdconfig_id, sensorgroup_id, algorithm, k_best, alertlevel, warninglevel, upper_limit, lower_limit) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                thresholdconfig_id,
                data["sensorgroup_id"],
                data["algorithm"],
                data["k_best"],
                data["alertlevel"],
                data["warninglevel"],
                data["upper_limit"],
                data["lower_limit"],
            )
        )

        conn.commit()
        cur.execute(
            "SELECT thresholdconfig_id, algorithm FROM threshold_config ORDER BY thresholdconfig_id DESC LIMIT 1")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1

    def GetThreshold_limit(self):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select * from threshold_config limit %s offset %s) json_array",
            (limit, offset))

        results = cur.fetchall()
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("SELECT COUNT(*) FROM threshold_config")
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response

    def updateThreshold(self):
        # pool=psycopg2.pool.SimpleConnectionPool(minconn=1,maxconn=25,host="localhost", port="5432", dbname="Ammi2", password="postgres", user="postgres")
        pool=psycopg2.pool.SimpleConnectionPool(minconn=1,maxconn=25,host="localhost", port="5432", dbname="Demo", password="root", user="postgres")

        input_param=request.get_json()
        thresholdconfig_id= input_param.get("thresholdconfig_id")
        sensorgroup_id= input_param.get("sensorgroup_id")
        algorithm= input_param.get("algorithm")
        k_best = input_param.get("k_best")
        alertlevel = input_param.get("alertlevel")
        warninglevel= input_param.get("warninglevel")
        upper_limit=input_param.get("upper_limit")
        lower_limit=input_param.get("lower_limit")

        conn = pool.getconn()
        cur = conn.cursor()

        query = "UPDATE threshold_config SET "
        attribute_values = []

        if sensorgroup_id is not None:
            query += "sensorgroup_id = %s, "
            attribute_values.append(sensorgroup_id)
        if algorithm is not None:
            query += "algorithm = %s, "
            attribute_values.append(algorithm)
        if k_best is not None:
            query += "k_best = %s, "
            attribute_values.append(k_best)
        if alertlevel is not None:
            query += "alertlevel = %s, "
            attribute_values.append(alertlevel)
        if warninglevel is not None:
            query += "warninglevel = %s, "
            attribute_values.append(warninglevel)
        if upper_limit is not None:
            query += "upper_limit = %s, "
            attribute_values.append(upper_limit)
        if lower_limit is not None:
            query += "lower_limit = %s, "
            attribute_values.append(lower_limit)

        # Remove the trailing comma and space from the query
        query = query.rstrip(", ")

        # Add the WHERE clause to specify the thresholdconfig_id
        query += " WHERE thresholdconfig_id = %s"
        attribute_values.append(thresholdconfig_id)

        # Execute the SQL query with the attribute values
        cur.execute(query,tuple( attribute_values))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and the database connection
        cur.close()
        conn.close()

        return 'Record updated successfully'


