#!/usr/bin/env python

from db import Db

db = Db()
db.conn.cursor().execute(
    """
        CREATE TABLE data (
            date TIMESTAMP UNIQUE,
            wind_direction smallint,
            wind_speed_knot smallint,
            precipitation_mm smallint,
            temperature smallint,
            pressure smallint,
            humidity smallint
        );
        CREATE INDEX idx_date ON data (date);
    """
)
db.conn.commit()
