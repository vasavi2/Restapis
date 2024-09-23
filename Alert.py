import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify

import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(host="localhost", port="5432", dbname="AHF_Project", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="assetdb", password="root", user="postgres")


class InputFile:

    def __init__(self):
        pass


    def GetAlert_with_Sensor(self, assed_id, sensor_group):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select alert_id,asset_name,alert,alert_status,start_time,end_time,alert_type  from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s limit %s offset %s) json_array",
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


    def GetAlert_with_Sensorwithalert(self, assed_id, sensor_group):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select alert_id,asset_name,alert,alert_status,start_time,end_time,alert_type  from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s order by alert_status desc limit %s offset %s) json_array",

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

    #sample
    def GetAlert_with_Sensors(self, assed_id, sensor_group):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select sensorgroup_id,asset_name,sensorgroup_name,alert,alert_type from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s  limit %s offset %s) json_array",
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

    def GetAlert_with_Sensors_powerbi(self, assed_id, sensor_group):
            global conn
            cur = conn.cursor()
            limit = request.args.get('limit')
            offset = request.args.get('offset')
            cur.execute(
                "select array_to_json(array_agg(row_to_json(json_array))) from (select * from  alert_table_consolidate where asset_id = %s and sensorgroup_id = %s  limit %s offset %s) json_array",
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

    def Update_Alert_Status(self):
        global conn
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            data_dict = isinstance(data, dict)
            if data_dict == True:
                cur.execute("update alert_table_consolidate  set alert_type = %s where alert_id = %s",
                            (data["AlertStatus"], data["AlertId"]))
                conn.commit()
                return "SINGLE VALUE UPDATED SUCCESSFULLY"
                conn.close()
            else:
                for item in data:
                    cur.execute("update alert_table_consolidate  set alert_type = %s where alert_id = %s",
                                (item["AlertStatus"], item["AlertId"]))
                    conn.commit()
                return "MULTIPLE VALUE UPDATED SUCCESSFULLY"
                conn.close()

    def Create_AddButton_AlertConsolidate(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

            cur.execute("select * from alert_table_consolidate")

            cur.execute("""create table  if not exists Add_Button(
            sensorgroup_id int ,asset_id int ,alert varchar(50),
            class varchar(50) ,alert_status varchar(100) ,
            start_time timestamp ,end_time timestamp ,
            alert_id bigint,alert_type varchar(50))""")

            #Default Attribute->alert_status,class
            query1 = '''alter table alert_table_consolidate alter column alert_status set default 'opened',alter column class set default 'alert' '''
            cur.execute(query1)
            query2 = '''alter table Add_Button alter column alert_status set default 'opened',alter column class set default 'alert' '''
            cur.execute(query2)

            cur.execute("truncate Add_Button")

            #Default Attribute->alert_id
            cur_insert.execute(
                "insert into Add_Button(sensorgroup_id,asset_id,alert,start_time,end_time,alert_id,alert_type) "
                # "values(%s,%s,%s,%s,%s,(SELECT alert_id FROM alert_table_consolidate ORDER BY alert_id DESC LIMIT 1) + 1,%s)",
                "VALUES (%s, %s, %s, %s, %s, (SELECT COALESCE(MIN(alert_id), 0) FROM Add_Button) - 1, %s)",

                (
                    data["sensorgroup_id"], data["asset_id"],
                    data["alert"], data["start_time"], data["end_time"], data["alert_type"]))


            cur.execute("""insert into alert_table_consolidate
            (sensorgroup_id,asset_id,
            asset_name,sensorgroup_name,
            alert,start_time,end_time,
            alert_id,
            alert_type)
            select
            Add_Button.sensorgroup_id,Add_Button.asset_id,
            asset_master.asset_name,sensorgroup_master.name,
            Add_Button.alert,Add_Button.start_time,Add_Button.end_time,
            Add_Button.alert_id,
            Add_Button.alert_type
            from asset_master
            join Add_Button
            on asset_master.id=Add_Button.asset_id
            join sensorgroup_master
             on sensorgroup_master.sensorgroup_id=Add_Button.sensorgroup_id;""")

            conn.commit()
            return "INSERTED"

    def DeleteAlertConsolidate(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_del = conn.cursor()
        if request.method == 'POST':
            data1 = request.get_json()
            cur_del.execute("DELETE FROM alert_table_consolidate WHERE alert_id=%s",(data1["alert_id"],))
            conn.commit()
            return "Successfully Delete"




    def Create_AddButton_AlertConsolidates(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

            cur.execute("select * from alert_table_consolidate")

            cur.execute("""create table  if not exists Add_Button(
            sensorgroup_id int ,asset_id int ,alert varchar(50),
            class varchar(50) ,alert_status varchar(100) ,
            start_time timestamp ,end_time timestamp ,
            alert_id bigint,alert_type varchar(50))""")

            #Default Attribute->alert_status,class
            query1 = '''alter table alert_table_consolidate alter column alert_status set default 'closed',alter column class set default 'alert' '''
            cur.execute(query1)
            query2 = '''alter table Add_Button alter column alert_status set default 'closed',alter column class set default 'alert' '''
            cur.execute(query2)

            cur.execute("truncate Add_Button")

            #Default Attribute->alert_id
            cur_insert.execute(
                "insert into Add_Button(sensorgroup_id,asset_id,alert,start_time,end_time,alert_id,alert_type) "
                "values(%s,%s,%s,%s,%s,(SELECT alert_id FROM alert_table_consolidate ORDER BY alert_id DESC LIMIT 1) + 1,%s)",
                (
                    data["sensorgroup_id"], data["asset_id"],
                    data["alert"], data["start_time"], data["end_time"], data["alert_type"]))


            cur.execute("""insert into alert_table_consolidate
            (sensorgroup_id,asset_id,
            asset_name,sensorgroup_name,
            alert,start_time,end_time,
            alert_id,
            alert_type)
            select
            Add_Button.sensorgroup_id,Add_Button.asset_id,
            asset_master.asset_name,sensorgroup_master.name,
            Add_Button.alert,Add_Button.start_time,Add_Button.end_time,
            Add_Button.alert_id,
            Add_Button.alert_type
            from asset_master
            join Add_Button
            on asset_master.id=Add_Button.asset_id
            join sensorgroup_master
             on sensorgroup_master.sensorgroup_id=Add_Button.sensorgroup_id;""")

            conn.commit()
            return "INSERTED"

    def getLatestOpenedRow(self):
            global conn
            # Open cursor to perform database operation
            cur = conn.cursor()

            # Query the database
            query = "select array_to_json(array_agg(row_to_json(json_array))) from (select count(*)::text from alert_table_consolidate where alert_status='opened') json_array;"
            cur.execute(query)

            result = cur.fetchone()
            count = result[0] if result else 0
            fin_count = count[0]

            return fin_count["count"]
            conn.close()









    def UpdateAlertStatus(self):
        cur = conn.cursor()
        update_query = "UPDATE alert_table_consolidate SET alert_status='closed' WHERE alert_status='opened'"
        cur.execute(update_query)
        conn.commit()
        rows_updated = cur.rowcount
        cur.close()
        return str(rows_updated)



    def GetAssetCard_with_asset_sensor(self, asset_name,sensor_name):
        global conn

        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select * from alert_table_consolidate_powerbi where asset_name=%s and sensorgroup_name=%s ) json_array",
            (asset_name,sensor_name,))

        # Fetch the data from the query
        data = cur.fetchall()
        # Convert the data into JSON
        for row in data:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            conn.close()


    def GetAssetCard(self):
        global conn

        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        cur.execute(
            "select array_to_json(array_agg(row_to_json(json_array))) from (select * from alert_table_consolidate_powerbi order by alert_age ) json_array")

        # Fetch the data from the query
        data = cur.fetchall()
        # Convert the data into JSON
        for row in data:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            return jsonify(json_obj)
            conn.close()



