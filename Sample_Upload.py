from flask import Flask, request, jsonify,request
from flask import Response
from flask_cors import CORS
import psycopg2.pool

import psycopg2
import io
import csv
app = Flask(__name__)
CORS(app)

# Establish a connection to your PostgreSQL database

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="AHF_Project",
    password="root",
    user="postgres")
# conn = psycopg2.connect(host="localhost", port="5432", dbname="Demo", password="root", user="postgres")



@app.route('/api/createTable', methods=['POST'])
def create_table():
    try:
        data = request.json
        table_name = data.get('tableName')
        columns = data.get('columns')
        cursor = conn.cursor()
        create_table_query = f"CREATE TABLE {table_name} ("
        for column in columns:
            column_name = column['columnName']
            data_type = column['dataType']
            create_table_query += f"{column_name} {data_type}, "
        create_table_query = create_table_query.rstrip(', ') + ")"
        cursor.execute(create_table_query)

        conn.commit()

        return 'Table created successfully', 201



    except (Exception, psycopg2.Error) as error:

        print("Error:", error)

        return 'Failed to create table', 500


@app.route('/api/getTables', methods=['GET'])
def get_tables():
    try:

        cursor = conn.cursor()

        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")

        tables = [row[0] for row in cursor.fetchall()]

        cursor.close()

        return jsonify(tables)



    except (Exception, psycopg2.Error) as error:

        print("Error:", error)

        return 'Failed to fetch tables', 500


@app.route('/api/uploadCSV/<string:table_name>', methods=['POST'])
def upload_csv(table_name):
    try:

        file = request.files['file']

        if not file:
            return 'No file provided', 400

        # Read the CSV file

        csv_data = file.read().decode('utf-8')

        # Create a CSV reader

        csv_reader = csv.reader(io.StringIO(csv_data))

        cursor = conn.cursor()

        #skip the header row

        next(csv_reader)

        # Assuming the CSV columns match your table columns order

        for row in csv_reader:
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(row))})"
            # insert_query="INSERT INTO hello (id,name) Values(%s,%s)"
            # data=(1,"john")

            cursor.execute(insert_query, row)

        conn.commit()

        return 'CSV data inserted successfully', 201



    except (Exception, psycopg2.Error) as error:
        print("Error:", error)

        return 'Failed to insert CSV data', 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3005, debug=True)

