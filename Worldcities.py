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

class InputFile9:

    def __init__(self):
        pass
    #
    # def GetPlant(self):
    #     global conn
    #     # Open cursor to perform database operation
    #     cur = conn.cursor()





    def get_countries(self):
        global conn
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT country FROM worldcities ORDER BY country')
        countries = [{'name': country[0]} for country in cursor.fetchall()]
        return jsonify(countries)
        # conn.close()

    def get_regions(self):
        global conn
        selected_country = request.args.get('country')
        cursor = conn.cursor()
        cursor.execute('SELECT  region FROM worldcities WHERE country=%s ', (selected_country,))
        regions = [{'name': region[0]} for region in cursor.fetchall()]

        return jsonify(regions)

        # conn.close()

    # def get_coordinates(self):
    #     global conn
    #     selected_country = request.args.get('country')
    #     selected_region = request.args.get('region')
    #     cursor = conn.cursor()
    #     cursor.execute('SELECT latitude, longitude FROM worldcities WHERE country=%s AND region=%s LIMIT 1', (selected_country, selected_region))
    #     latitude, longitude = cursor.fetchone()
    #     return jsonify({'latitude': latitude, 'longitude': longitude})
    #     # conn.close()

    def get_coordinates(self):
        global conn
        selected_country = request.args.get('country')
        selected_region = request.args.get('region')
        cursor = conn.cursor()
        cursor.execute('SELECT latitude, longitude FROM worldcities WHERE country=%s AND region=%s LIMIT 1',
                       (selected_country, selected_region))
        result = cursor.fetchone()
        if result is not None:
            latitude, longitude = result
            return jsonify({'latitude': latitude, 'longitude': longitude})
        else:
            return jsonify({'error': 'No results found'})
