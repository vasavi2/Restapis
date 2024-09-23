import psycopg2
import csv
import os
from typing import Union
from flask import Response
from flask import Flask, request, jsonify
app = Flask(__name__)
# Database connection
conn = psycopg2.connect(host="localhost", port="5432",  dbname="AHF_Project", password="root", user="postgres")

# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")


class InputFile5:
    def __int__(self):
        pass

# Route to insert CSV data into database
    def Upload_CsvFiles(self):
        # try:
        #     # Get CSV file from request
            csv_file = request.files['file']
            if csv_file.filename=="plant.csv":
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                cur = conn.cursor()
                next(csv_data) # Skip header row
            # Iterate through each row in the CSV data and insert into the database
                for row in csv_data:
                    cur.execute(
                                """INSERT INTO plant_master ("plant_id","plant_name","region","country","latitude","longitude","update_time_stamp")
                                VALUES (%s,%s,%s,%s,%s,%s,%s)""", (int(row[0]),row[1],row[2],row[3],row[4],row[5],row[6])
                                )
                conn.commit()
                cur.close()

                return jsonify({'message': 'PlantData inserted successfully'}), 200

            elif csv_file.filename=="asset.csv":
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                cur = conn.cursor()
                next(csv_data) # Skip header row
            # Iterate through each row in the CSV data and insert into the database
                for row in csv_data:
                    cur.execute(
                                """INSERT INTO asset_master ("id","plant_id","asset_tag","asset_name","update_time_stamp")
                                VALUES (%s,%s,%s,%s,%s)""", (row[0],row[1],row[2],row[3],row[4])
                                )
                conn.commit()
                cur.close()

                return jsonify({'message': 'AssetData inserted successfully'}), 200

            elif csv_file.filename == "sensor.csv":
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                cur = conn.cursor()
                next(csv_data)  # Skip header row
                # Iterate through each row in the CSV data and insert into the database
                for row in csv_data:
                    cur.execute(
                        """INSERT INTO sensorgroup_master ("sensorgroup_id","asset_id","name","component","endpoint","update_time_stamp")
                        VALUES (%s,%s,%s,%s,%s,%s)""", (row[0], row[1], row[2], row[3], row[4], row[5])
                    )
                conn.commit()
                cur.close()

                return jsonify({'message': 'SensorData inserted successfully'}), 200
            elif csv_file.filename == "threshold.csv":
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                cur = conn.cursor()
                next(csv_data)  # Skip header row
                # Iterate through each row in the CSV data and insert into the database
                for row in csv_data:
                    cur.execute(
                        """INSERT INTO threshold_config ("thresholdconfig_id","sensorgroup_id","algorithm","k_best","alertlevel","warninglevel","upper_limit","lower_limit","update_time_stamp")
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8])
                    )
                conn.commit()
                cur.close()

                return jsonify({'message': 'ThresholdData inserted successfully'}), 200
            elif csv_file.filename == "modelconfig.csv":
                csv_data = csv.reader(csv_file.read().decode('utf-8').splitlines())
                cur = conn.cursor()
                next(csv_data)  # Skip header row
                # Iterate through each row in the CSV data and insert into the database
                for row in csv_data:
                    cur.execute(
                        """INSERT INTO model_config ("modelconfig_id","thresholdconfig_id","cluster_id","cluster_name",,"update_time_stamp")
                        VALUES (%s,%s,%s,%s,%s,%s)""", (row[0], row[1], row[2], row[3], row[4],row[5])
                    )
                conn.commit()
                cur.close()

                return jsonify({'message': 'ModelConfigData inserted successfully'}), 200

            else:
                return jsonify({'Please Inserted Valid CSV Files'}), 200

    # except Exception as e:
    #     return jsonify({'message': 'Error inserting data into database', 'error': str(e)}), 400





