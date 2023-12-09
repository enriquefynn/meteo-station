#!/usr/bin/env python

from flask import Flask, request, jsonify
from flask_cors import CORS
from db import Db

app = Flask(__name__)
CORS(app)

db = Db()


@app.route('/save_air_data', methods=['POST'])
def save_data():
    data = request.json
    try:
        db.insert_air_data(data)
        return jsonify({'message': 'Data saved successfully!'}), 201
    except Exception as e:
        db.conn.rollback()
        print("Error inserting data:", e)
        return jsonify({'error': str(e)}), 400


@app.route('/get_instant_data', methods=['GET'])
def get_data():
    try:
        json_data = db.get_latest_point()
        return json_data, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/get_daily_data', methods=['GET'])
def get_daily_data():
    try:
        json_data = db.get_daily_points()
        return json_data, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/get_weekly_data', methods=['GET'])
def get_weekly_data():
    try:
        json_data = db.get_weekly_points()
        return json_data, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/get_monthly_data', methods=['GET'])
def get_monthly_data():
    try:
        json_data = db.get_monthly_points()
        return json_data, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5080', debug=True)
