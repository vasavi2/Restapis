import json
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify
from psycopg2 import sql
import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(host="localhost", port="5432", dbname="AHF_Project", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="assetdb", password="root", user="postgres")


class InputFile20:

    def __init__(self):
        pass

    def GetImages(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select name,description,status from image_gallery) json_array;"
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

    def PostImages(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()
        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(id), 0) FROM image_gallery")
        max_id = cur.fetchone()[0]
        id = max_id + 1
        num=0
        cur.execute("insert into image_gallery(id,name,status,description) "
                    "values(%s,%s,%s,%s)",
                    (
                        id,
                        data["name"],
                        num,
                        data["desc"],))

        conn.commit()
        cur.execute("(select id,name from image_gallery order by id desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1
    def getLatestRow(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()

        # Query the database
        query = "select array_to_json(array_agg(row_to_json(json_array))) from (select count(*)::text from image_gallery where status='0') json_array;"
        cur.execute(query)

        result=cur.fetchone()
        count=result[0] if result else 0
        fin_count=count[0]

        return  fin_count["count"]
        conn.close()

    # def UpdateImages(self):
    #     global conn
    #     # Open cursor to perform database operation
    #     cur = conn.cursor()
    #     if request.method == 'POST':
    #         data = request.get_json()
    #         cur.execute("update image_gallery set status=1 where status=0")
    #         conn.commit()
    #         return "Images updated successfully"


    # def UpdateImages(self):
    #     global conn
    #     cur = conn.cursor()
    #
    #     update_query = sql.SQL("UPDATE image_gallery SET status = {} WHERE status = {};").format(
    #         sql.Identifier(1),  # Set status to 1
    #         sql.Identifier(0)  # Where status is 0
    #     )
    # #
    #     cur.execute(update_query)
    #     conn.commit()
    #     rows_updated = cur.rowcount
    # #
    #     return rows_updated
    #     conn.close()

    def UpdateImages(self):
        cur = conn.cursor()
        update_query = "UPDATE image_gallery SET status='1' WHERE status='0'"
        cur.execute(update_query)
        conn.commit()
        rows_updated = cur.rowcount
        cur.close()
        return str(rows_updated)

















