#!/usr/bin/env python

from db import Db

db = Db()
db.conn.cursor().execute(
    """
        DROP TABLE IF EXISTS data
    """
)
db.conn.commit()
