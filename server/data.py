from typing import List
from flask import jsonify


class DataPoint:
    def __init__(self, row):
        self.date = row[0]
        self.wind_direction = row[1]
        self.wind_speed_knot = row[2]
        self.precipitation_mm = row[3]
        self.temperature = row[4]
        self.pressure = row[5]
        self.humidity = row[6]

    def json(self):
        return jsonify(self.__dict__)


class AggregatedDataPoint:
    def __init__(self, row):
        self.date = row[0]
        self.avg_wind_direction = row[1]
        self.avg_wind_speed_knot = row[2]
        self.total_precipitation_mm = row[3]
        self.avg_temperature = row[4]
        self.avg_pressure = row[5]
        self.avg_humidity = row[6]


def aggregated_data_point_json_vec(data: List[AggregatedDataPoint]):
    return jsonify(list(map(lambda d: d.__dict__, data)))


def data_point_json_vec(data: List[DataPoint]):
    return jsonify(list(map(lambda d: d.__dict__, data)))
