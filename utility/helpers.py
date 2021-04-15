import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from pathlib import Path
from flask import g, jsonify
import arrow
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

    arrow_time= arrow.get(f'{date} {time}', 'YYYY-MM-DD HH:mm')
    return arrow_time.format('h:m A - dddd MMM Do, YYYY')


################ Secure User info on appContext #############
def secure_g(g, attr='user', key='passkey'):
    if g is not None:
        g_obj = getattr(g, attr)
        mydic = dict(g_obj)
        mydic.pop(key)
        return mydic
    return []

############## Convert cursor to dict type ###################

def fetcher(cur):
    if cur is not None:
        output = []
        for row in cur:
            output.append({**row})
        return output
    return []


######### create an output dictionary containing
#  all information to return to the client #########

def JSON_output(message, g=None, cur=None, **kwargs):
    
    return jsonify({'message':message,
                    'info': {'user_info':secure_g(g),
                            'query_info':fetcher(cur)
                            },
                    **kwargs
                    })