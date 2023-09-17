#!/usr/bin/env python

from flask import Flask, request, jsonify

from db import Db

app = Flask(__name__)

db = Db()


@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json
    try:
        cursor = db.conn.cursor()
        cursor.execute(
            """
            INSERT INTO data (date, wind_direction, wind_speed_knot,
            precipitation_mm, temperature, pressure, humidity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data['date'],
                data['wind_direction'],
                data['wind_speed_knot'],
                data['precipitation_mm'],
                data['temperature'],
                data['pressure'],
                data['humidity'],
            ),
        )
        db.conn.commit()
        return jsonify({'message': 'Data saved successfully!'}), 201
    except Exception as e:
        db.conn.rollback()
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
    app.run(debug=True)
