import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from pathlib import Path
from flask import g


##### Create Connection pool ######
def conn_pool(minconn, maxconn, /, host='localhost', database='phonebook', user='postgres', password=1):
    
    return ThreadedConnectionPool(minconn,
                                  maxconn,
                                  host=host,
                                  database=database,
                                  user=user,
                                  password=password)


############ query func  ##########
def query(query, vals=()):

    query = "sql/" + query + ".sql"
    path = Path(query)

    with open(path, 'r') as f:
        query_text = str(f.read())

    cur = g.conn.cursor(cursor_factory = DictCursor)
    cur.execute(query_text, vals)
    return cur