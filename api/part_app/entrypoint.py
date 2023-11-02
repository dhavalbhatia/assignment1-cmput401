#!/usr/bin/env python
import time
import sqlalchemy_utils

SQLALCHEMY_DATABASE_URL = "postgresql://db_user:test_db@db/docker-compose"

while True:
    try:
        if sqlalchemy_utils.database_exists(SQLALCHEMY_DATABASE_URL):
            break
    except:
        print("...  db not up")
    
    print("... waiting for db")
    time.sleep(.5)

print("... db connected")