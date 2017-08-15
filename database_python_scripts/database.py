import sys
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from clay import config
from copy import deepcopy

usage_info = 'Usage: python database.py [create|drop]'
meta = config.get('database')

url_meta = deepcopy(meta)
# dont use database property here
del url_meta['database']
url = URL(**url_meta)
engine = create_engine(url)


def create_db():
    connect = None
    try:
        connect = engine.connect()
        connect.execute('CREATE DATABASE IF NOT EXISTS ' + config.get('database.database'))
    finally:
        if connect:
            connect.close()


def drop_db():
    connect = None
    try:
        connect = engine.connect()
        connect.execute('DROP DATABASE IF EXISTS ' + config.get('database.database'))
    finally:
        if connect:
            connect.close()


if __name__ == '__main__':
    if not len(sys.argv) == 2:
        print usage_info
    else:
        command = sys.argv[1]

        if (command == 'create'):
            create_db()
        elif (command == 'drop'):
            drop_db()
        else:
            print usage_info
