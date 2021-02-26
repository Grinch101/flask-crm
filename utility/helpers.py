import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from pathlib import Path
from flask import g
import datetime as dt
import plotly
import plotly.graph_objects as go
import json

##### Create Connection pool ######
def conn_pool(minconn, maxconn, /, host='localhost', database='phonebook', user='postgres', password=1):

    return ThreadedConnectionPool(minconn,
                                  maxconn,
                                  host=host,
                                  database=database,
                                  user=user,
                                  password=password)


############ query func  ##########
def query(query, vals=""):

    query = "sql/" + query + ".sql"
    path = Path(query)

    with open(path, 'r') as f:
        query_text = str(f.read())

    cur = g.conn.cursor(cursor_factory=DictCursor)
    cur.execute(query_text, vals)
    return cur


############## convet date and time to datetime ############

def conv_datetime(date, time):
    date = str(date)
    time = str(time)
    # # reference for date formatting
    # %d	Day of the month (decimal number)
    # %m	Month (decimal number)
    # %b	Month (abbreviated)
    # %B	Month (full name)
    # %y	Year (2 digit)
    # %Y	Year (4 digit)
    return dt.datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
