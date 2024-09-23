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

class InputFile100:

    def __init__(self):
        pass

    def insert_date(self):
        global conn
        # Open cursor to perform database operation
        cur = conn.cursor()
        cur_insert = conn.cursor()
        if request.method == 'POST':
            data = request.get_json()

        # Get the maximum thresholdconfig_id from the table
        cur.execute("SELECT COALESCE(MAX(id), 0) FROM selectdates_final_1")

        max_id = cur.fetchone()[0]
        plant_id = max_id + 1

        cur.execute("insert into selectdates_final_1(id,start_date,end_date,exchanger) "
        "values(%s,%s,%s,%s)",
        (
            plant_id,
            data["start_date"],
            data["end_date"],
            data["exchanger"]
        ))

        conn.commit()
        cur.execute("(select id,start_date from selectdates_final_1 order by id desc limit 1)")
        result = cur.fetchall()
        dict1 = {}
        key = str(result[0][0])
        value = str(result[0][1])
        dict1.update({key: value})

        return dict1
