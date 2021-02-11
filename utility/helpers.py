import psycopg2
from psycopg2.pool import SimpleConnectionPool
import psycopg2.extras
from pathlib import Path
from flask import g


# DEFINE 3 HELPER FUNCTIONS:

def open_conn(host='localhost', database='phonebook', user='postgres', password=1):
    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=1)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cur, conn


def open_pool(minconn, maxconn, /, host='localhost', database='phonebook', user='postgres', password=1):

    connections = SimpleConnectionPool(minconn,
                                       maxconn,
                                       host=host,
                                       database=database,
                                       user=user,
                                       password=1)

    def conn():
        return connections.getconn()

    def cur():
        conn = conn()
        return conn.cursor()
    
    return cur(), conn()


def close_conn(cur, conn):
    conn.commit()
    cur.close()
    conn.close()


def query(path, query_name,  vals=''):

    file_name = query_name+'.sql'
    path = Path(path) / file_name

    with open(path, 'r') as f:
        query_text = str(f.read())
        f.close()
    cur = g.cur
    conn = g.conn

    cur.execute(query_text,  vals)
    try:
        rows = cur.fetchall()
        return rows
    except:
        pass

