import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
app = Flask(__name__)
CORS(app)
conn = psycopg2.connect(host="localhost", port="5432", dbname="AHF_Project", password="root", user="postgres")
def get_data(table_name, page, per_page):
    global conn
    cur = conn.cursor()
    offset = (page - 1) * per_page
    query = f"SELECT array_to_json(array_agg(row_to_json(json_array))) FROM (SELECT * FROM {table_name} LIMIT {per_page} OFFSET {offset}) json_array"
    cur.execute(query)
    data = cur.fetchone()[0]
    cur.close()
    return data


@app.route("/<table_name>", methods=['GET'])
def get_table_data(table_name):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    data = get_data(table_name, page, per_page)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)