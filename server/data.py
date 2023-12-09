from typing import List
from flask import jsonify


class DataPoint:
    def __init__(self, row):
        self.date = row[0].strftime('%Y-%m-%d %H:%M:%S')
        self.wind_direction = row[1]
        self.wind_speed_knot = row[2]
        self.temperature_c = row[3]
        self.pressure_mbar = row[4]
        self.humidity = row[5]

    def json(self):
        return jsonify(self.__dict__)


class AggregatedDataPoint:
    def __init__(self, row):
        self.date = row[0].strftime('%Y-%m-%d %H:%M:%S')
        self.avg_wind_direction = row[1]
        self.avg_wind_speed_knot = row[2]
        # self.total_precipitation_mm = row[3]
        self.avg_temperature_c = row[3]
        self.avg_pressure_mbar = row[4]
        self.avg_humidity = row[5]


def aggregated_data_point_json_vec(data: List[AggregatedDataPoint]):
    return jsonify(list(map(lambda d: d.__dict__, data)))


def data_point_json_vec(data: List[DataPoint]):
    return jsonify(list(map(lambda d: d.__dict__, data)))
