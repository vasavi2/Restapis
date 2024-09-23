import json
import os
from typing import Union
from flask import Response
import datetime
from flask import Flask, request, jsonify
import psycopg2
import psycopg2.pool
app = Flask(__name__)


conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")

class InputFile2:

    def __init__(self):
        pass

    def insert_Plant_Data(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        query1 = '''alter table plant_master alter column update_time_stamp set default current_timestamp '''
        cur.execute(query1)
        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(plant_id), 0) FROM plant_master")
        max_id = cur.fetchone()[0]
        plant_id = max_id + 1

        cur.execute("insert into plant_master(plant_id,plant_name,region,country,latitude,longitude) "
        "values(%s,%s,%s,%s,%s,%s)",
        (
            plant_id,
            data["plant_name"],
            data["region"], data["country"],data["latitude"],data["longitude"],))

        conn.commit()
        cur.execute("(select plant_id,plant_name from plant_master order by plant_id desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1


    def insert_Plant_ID(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        cur.execute("insert into plant_ids (plant_id) "
        "values(%s)",
        data["id"])

        conn.commit()
        return "Successfully Inserted"


    def GetPlantId(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select plant_id from plant_ids) json_array;"
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




    def GetPlant(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        print("plant---->")

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select  * from plant_master) json_array;"
        cur.execute(query)

        # Fetch the data from the query
        data = cur.fetchall()
        print("data fetch--->",data)

        # Convert the data into JSON
        for row in data:
            print("row",row)
            data_str = str(row)[1:-2]
            print("data_str",data_str)

            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            print("json_obj for plants--->",json_obj)
            return jsonify(json_obj)
            # Close the connection
            conn.close()



    # Delete Plant Data based upon plant_id automatically delete asset_master table and sensorgroup_master table based upon related data
    def DeleteEntirePlantData(self):
        global conn
        # Open cursor to perform database operation
        cur_del = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

            cur_del.execute(
                "delete from sensorgroup_master where asset_id in (select id from asset_master where plant_id in (%s))",
                (data["plant_id"],))
            cur_del.execute(
                "delete from asset_master where plant_id in (select plant_id from plant_master where plant_id in (%s))",
                (data["plant_id"],))
            cur_del.execute("delete from plant_master where plant_id in (%s)", (data["plant_id"],))

        conn.commit()
        return "Successfully Delete"


    def GetPlant_limit(self):
        global conn
        cur = conn.cursor()
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        cur.execute(
            # "select array_to_json(array_agg(row_to_json(json_array))) from (select alert_id, alert,start_time,end_time,alert_type from alert_table_consolidate where asset_id = %s and sensorgroup_id = %s limit %s offset %s) json_array",
            # (assed_id, sensor_group, limit, offset))

            "select array_to_json(array_agg(row_to_json(json_array))) from (select * from plant_master order by plant_id  limit %s offset %s) json_array",
            (limit, offset))

        results = cur.fetchall()
        for row in results:
            data_str = str(row)[1:-2]
            json_array = json.loads(json.dumps(data_str))
            json_obj = eval(json_array)
            cur.execute("SELECT COUNT(*) FROM plant_master")
            total_count = cur.fetchone()[0]
            response = jsonify(json_obj)
            response.headers.add('x-total-count', total_count)
            response.headers["Access-Control-Expose-Headers"] = "x-total-count"
            return response

        conn.commit()

        # Close the cursor and the database connection
        cur.close()
        conn.close()

    #update plant data based upon ids


    def DeletePlant(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_del = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

            cur_del.execute("delete from plant_master where plant_id=%s", (data["plant_id"],))

        conn.commit()
        return "Successfully Delete"


    def Update_PlantData(self):
        pool=psycopg2.pool.SimpleConnectionPool(minconn=1,maxconn=25,host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")
        # pool=psycopg2.pool.SimpleConnectionPool(minconn=1,maxconn=25,host="localhost", port="5432", dbname="Demo", password="root", user="postgres")

        input_param=request.get_json()
        plant_id = input_param.get("plant_id")
        plant_name = input_param.get("plant_name")
        region = input_param.get("region")
        country = input_param.get("country")
        latitude = input_param.get("latitude")
        longitude = input_param.get("longitude")

        conn = pool.getconn()
        cur = conn.cursor()

        if "region" not  in input_param:
            region=None
        if "country" not  in input_param:
            country=None
        if "latitude" not in input_param:
            latitude=None
        if "longitude" not in input_param:
            longitude=None
        if "plant_name" not in input_param:
            plant_name=None


        #6
        if plant_id and plant_name and region and country and latitude and longitude:
            query = "update plant_master  set plant_name = %s,region=%s,country=%s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = (plant_name, region, country, latitude, longitude, plant_id)

        #5
        elif plant_id and plant_name and region and country and latitude :
            query = "update plant_master  set plant_name = %s,region=%s,country=%s,latitude=%s where plant_id = %s"
            attribute_values = (plant_name, region, country, latitude, plant_id)


        elif plant_id and plant_name and region and country and longitude:
            query = "update plant_master  set plant_name = %s,region=%s,country=%s,longitude=%s where plant_id = %s"
            attribute_values = (plant_name, region, country, longitude, plant_id)

        elif plant_id and plant_name and region and  latitude and longitude:
            query = "update plant_master  set plant_name = %s,region=%s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = (plant_name, region, latitude, longitude, plant_id)

        elif plant_id and plant_name and country and latitude and longitude:
            query = "update plant_master  set plant_name = %s,country=%s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = (plant_name, country, latitude, longitude, plant_id)

        elif plant_id and region and country and latitude and longitude:
            query = "update plant_master  set region=%s,country=%s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = ( region, country, latitude, longitude, plant_id)

        #4

        elif plant_id and plant_name and region and country :
            query = "update plant_master  set plant_name = %s,region=%s,country=%s where plant_id = %s"
            attribute_values = (plant_name, region, country, plant_id)
        elif plant_id and plant_name and latitude and longitude :
            query = "update plant_master  set plant_name = %s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = (plant_name, latitude,longitude, plant_id)

        elif plant_id and region and latitude and longitude :
            query = "update plant_master  set region = %s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = (region, latitude,longitude, plant_id)

        elif plant_id and country and latitude and longitude :
            query = "update plant_master  set country = %s,latitude=%s,longitude=%s where plant_id = %s"
            attribute_values = (country, latitude,longitude, plant_id)

        #3

        elif plant_id and plant_name and region  :
            query = "update plant_master  set plant_name = %s,region=%s where plant_id = %s"
            attribute_values = (plant_name, region, plant_id)
        elif plant_id and plant_name and country  :
            query = "update plant_master  set plant_name = %s,countyr=%s where plant_id = %s"
            attribute_values = (plant_name, country, plant_id)
        elif plant_id and plant_name and latitude  :
            query = "update plant_master  set plant_name = %s,latitude=%s where plant_id = %s"
            attribute_values = (plant_name, latitude, plant_id)
        elif plant_id and plant_name and longitude  :
            query = "update plant_master  set plant_name = %s,longitude=%s where plant_id = %s"
            attribute_values = (plant_name, longitude, plant_id)

        elif plant_id and country and region  :
            query = "update plant_master  set country = %s,region=%s where plant_id = %s"
            attribute_values = (country, region, plant_id)

        elif plant_id and latitude and region  :
            query = "update plant_master  set region = %s,latitude=%s where plant_id = %s"
            attribute_values = (region, latitude, plant_id)

        elif plant_id and longitude and region  :
            query = "update plant_master  set region = %s,longitude=%s where plant_id = %s"
            attribute_values = (region, longitude, plant_id)

        elif plant_id and latitude and longitude  :
            query = "update plant_master  set longitude = %s,latitude=%s where plant_id = %s"
            attribute_values = (longitude,latitude,plant_id)





        #2
        elif plant_id and plant_name:

            query = "update plant_master  set plant_name = %s where plant_id = %s"
            attribute_values = (plant_name, plant_id)
        elif plant_id and region:
            query = "update plant_master  set region = %s where plant_id = %s"
            attribute_values = (region, plant_id)

        elif plant_id and country:
            query = "update plant_master  set country = %s where plant_id = %s"
            attribute_values = (country, plant_id)

        elif plant_id and latitude:
            query = "update plant_master  set latitude = %s where plant_id = %s"
            attribute_values = (latitude, plant_id)

        else:
            query = "update plant_master  set longitude = %s where plant_id = %s"
            attribute_values = (longitude, plant_id)


        # Execute the SQL query with the attribute values
        cur.execute(query, attribute_values)

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and the database connection
        cur.close()
        conn.close()

        return 'Record updated successfully'

    def DeleteEntirePlantData2(self):
        global conn

        # Open cursor to perform database operation
        cur_del = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

        # Delete rows from model_config table
        cur_del.execute(
            "DELETE FROM model_config WHERE thresholdconfig_id IN (SELECT thresholdconfig_id FROM threshold_config WHERE sensorgroup_id IN (SELECT sensorgroup_id FROM sensorgroup_master WHERE asset_id IN (SELECT id FROM asset_master WHERE plant_id = %s)))",
            (data["plant_id"],))

        # Delete rows from threshold table
        cur_del.execute(
            "DELETE FROM threshold_config WHERE sensorgroup_id IN (SELECT sensorgroup_id FROM sensorgroup_master WHERE asset_id IN (SELECT id FROM asset_master WHERE plant_id = %s))",
            (data["plant_id"],))

        # Delete rows from sensor table
        cur_del.execute(
            "DELETE FROM sensorgroup_master WHERE asset_id IN (SELECT id FROM asset_master WHERE plant_id = %s)",
            (data["plant_id"],))

        # Delete rows from asset table
        cur_del.execute(
            "DELETE FROM asset_master WHERE plant_id = %s",
            (data["plant_id"],))

        # Delete rows from plant table
        cur_del.execute(
            "DELETE FROM plant_master WHERE plant_id = %s",
            (data["plant_id"],))

        conn.commit()
        return "Successfully Delete"




    def getPlantName(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
            print("data",data)
            country=data["country"]["selected_country"]
            region=data["region"]["selected_region"]
            print("country--->",country,region)
            print("data recived from backend---->",data)
            cur.execute("select array_to_json(array_agg(row_to_json(json_array))) from (select * from plant_master) json_array where country=%s and region=%s", (country,region))
            # data=cur.fetchall()
            # query = "select array_to_json(array_agg(row_to_json(json_array))) from (select  * from plant_master) json_array;"

            # Fetch the data from the query
            data_query = cur.fetchall()
            print("data fetch--->", data_query)

            for i in data_query:
                print("items-->",i)
                data_str = str(i)[1:-2]
                print("data_str---->", data_str)
                json_array = json.loads(json.dumps(data_str))
                json_obj = eval(json_array)
                print("json_obj--->",json_obj)
                return jsonify(json_obj)
                # Close the connection
                # conn.close()








