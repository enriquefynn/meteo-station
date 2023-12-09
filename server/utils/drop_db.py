#!/usr/bin/env python

import os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import db


db = db.Db()
db.conn.cursor().execute(
    """
        DROP TABLE IF EXISTS air_data;
        DROP TABLE IF EXISTS precipitation_data;
    """
)
db.conn.commit()
