#!/usr/bin/env python

import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import db

db = db.Db()
db.conn.cursor().execute(
    """
        CREATE TABLE air_data (
            date TIMESTAMP PRIMARY KEY NOT NULL,
            wind_direction smallint,
            wind_speed_knot smallint,
            temperature smallint,
            pressure smallint,
            humidity smallint
        );
        CREATE INDEX idx_air_data_date ON air_data(date);

        CREATE TABLE precipitation_data (
            precipitation_mm smallint NOT NULL,
            date TIMESTAMP PRIMARY KEY NOT NULL
        );
        CREATE INDEX idx_precipitation_data_date ON precipitation_data(date);
    """
)
db.conn.commit()
