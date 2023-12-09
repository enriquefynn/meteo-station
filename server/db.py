from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import jsonify
import psycopg2, os

from data import (
    DataPoint,
    AggregatedDataPoint,
    data_point_json_vec,
    aggregated_data_point_json_vec,
)


load_dotenv()


class Db:
    def __init__(self):
        # Get the environment variables
        DATABASE_NAME = os.getenv('DATABASE_NAME')
        DATABASE_USER = os.getenv('DATABASE_USER')
        DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
        DATABASE_HOST = os.getenv('DATABASE_HOST')
        DATABASE_PORT = os.getenv('DATABASE_PORT')

        # Set up the connection to the PostgreSQL database
        conn = psycopg2.connect(
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
        )

        self.conn = conn

    def insert_air_data(self, air_data):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO air_data (date, wind_direction, wind_speed_knot,
            temperature, pressure, humidity)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                air_data['date'],
                air_data['wind_direction'],
                air_data['wind_speed_knot'],
                air_data['temperature_c'],
                air_data['pressure_mbar'],
                air_data['humidity'],
            ),
        )
        self.conn.commit()

    def get_latest_point(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                date,
                wind_direction,
                wind_speed_knot,
                temperature,
                pressure,
                humidity
            FROM 
                air_data
            ORDER BY 
                date DESC
            LIMIT 1;
        """
        )
        row = cursor.fetchone()
        data_point = DataPoint(row)
        return data_point.json()

    def get_daily_points(self):
        today = datetime.now()
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                date_trunc('hour', date) AS hour,
                AVG(wind_direction) AS avg_wind_direction,
                AVG(wind_speed_knot) AS avg_wind_speed_knot,
                AVG(temperature) AS avg_temperature,
                AVG(pressure) AS avg_pressure,
                AVG(humidity) AS avg_humidity
            FROM 
                air_data
            WHERE 
                date >= %s AND date < %s
            GROUP BY 
                hour
            ORDER BY 
                hour;
        """,
            (
                today.strftime('%Y-%m-%d') + ' 00:00:00',
                today.strftime('%Y-%m-%d') + ' 23:59:59',
            ),
        )
        rows = cursor.fetchall()
        data_points = [AggregatedDataPoint(row) for row in rows]
        return aggregated_data_point_json_vec(data_points)

    def get_weekly_points(self):
        today = datetime.now()
        last_week = today - timedelta(weeks=1)
        cursor = self.conn.cursor()
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                date_trunc('day', date) + interval '6 hour' * floor(date_part('hour', date)::integer / 6) AS six_hour_interval,
                AVG(wind_direction) AS avg_wind_direction,
                AVG(wind_speed_knot) AS avg_wind_speed_knot,
                AVG(temperature) AS avg_temperature,
                AVG(pressure) AS avg_pressure,
                AVG(humidity) AS avg_humidity
            FROM 
                data
            WHERE 
                date >= %s AND date < %s
            GROUP BY 
                six_hour_interval
            ORDER BY 
                six_hour_interval;
        """,
            (
                last_week.strftime('%Y-%m-%d') + ' 00:00:00',
                today.strftime('%Y-%m-%d') + ' 23:59:59',
            ),
        )
        rows = cursor.fetchall()
        data_points = [AggregatedDataPoint(row) for row in rows]
        return aggregated_data_point_json_vec(data_points)

    def get_monthly_points(self):
        today = datetime.now()
        last_month = today - timedelta(weeks=4)
        cursor = self.conn.cursor()
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 
                date_trunc('week', date) AS week,
                AVG(wind_direction) AS avg_wind_direction,
                AVG(wind_speed_knot) AS avg_wind_speed_knot,
                SUM(precipitation_mm) AS total_precipitation_mm,
                AVG(temperature) AS avg_temperature,
                AVG(pressure) AS avg_pressure,
                AVG(humidity) AS avg_humidity
            FROM 
                data
            WHERE 
                date >= %s AND date < %s
            GROUP BY 
                week
            ORDER BY 
                week
        """,
            (
                last_month.strftime('%Y-%m-%d') + ' 00:00:00',
                today.strftime('%Y-%m-%d') + ' 23:59:59',
            ),
        )
        rows = cursor.fetchall()
        data_points = [AggregatedDataPoint(row) for row in rows]
        return aggregated_data_point_json_vec(data_points)
