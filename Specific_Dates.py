import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify

import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")


class InputFile15:

    def __init__(self):
        pass


    def GetAlert_with_Sensor_thirtydays(self, assed_id, sensor_group):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select *  from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s and  end_time>=CURRENT_DATE-INTERVAL '30 days' limit %s offset %s) json_array",
            (assed_id, sensor_group, limit, offset))
        results = cur.fetchall()
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("SELECT COUNT(*) FROM alert_table_consolidate where asset_id = %s and sensorgroup_id = %s",
                        (assed_id, sensor_group))
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response

    def GetAlert_with_Sensor_sixmonth(self, assed_id, sensor_group):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select *  from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s and  end_time>=CURRENT_DATE-INTERVAL '6 months' limit %s offset %s) json_array",
            (assed_id, sensor_group, limit, offset))
        results = cur.fetchall()
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("SELECT COUNT(*) FROM alert_table_consolidate where asset_id = %s and sensorgroup_id = %s",
                        (assed_id, sensor_group))
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response


    def GetAlert_with_Sensor_lastyear(self, assed_id, sensor_group):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select *  from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s and  end_time>=CURRENT_DATE-INTERVAL '1 year' limit %s offset %s) json_array",
            (assed_id, sensor_group, limit, offset))
        results = cur.fetchall()
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("SELECT COUNT(*) FROM alert_table_consolidate where asset_id = %s and sensorgroup_id = %s",
                        (assed_id, sensor_group))
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response










