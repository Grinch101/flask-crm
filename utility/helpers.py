import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from pathlib import Path
from flask import g


##### Create Connection pool ######
def conn_pool(minconn, maxconn, / , host='localhost', database='phonebook', user='postgres', password=1):
    return ThreadedConnectionPool(minconn,
                                  maxconn,
                                  host=host,
                                  database=database,
                                  user=user,
                                  password=password)


############ query func  ##########
def query(path, query_name, vals=''):

    file_name = query_name+'.sql'
    path = Path(path) / file_name

    with open(path, 'r') as f:
        query_text = str(f.read())

    cur = g.cur
    cur.execute(query_text,  vals)