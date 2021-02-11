import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor
from pathlib import Path
from flask import g


########### Helpers to work with one connection #####################

def open_conn(host='localhost', database='phonebook', user='postgres', password=1):
    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=1)

    cur = conn.cursor(cursor_factory=DictCursor)
    return cur, conn


def close_conn(cur, conn):
    conn.commit()
    cur.close()
    conn.close()


##################### Connection Pooling ###############

class get_cursor():
    def __init__(self, minconn, maxconn):
        self.bag = []
        self.host = 'localhost'
        self.database = 'phonebook'
        self.user = 'postgres'
        self.password = 1
        self.minconn = minconn
        self.maxconn = maxconn
        self.connections = ThreadedConnectionPool(self.minconn,
                                                  self.maxconn,
                                                  host=self.host,
                                                  database=self.database,
                                                  user=self.user,
                                                  password=self.password)

    def __enter__(self):
        conns = self.connections
        conn = conns.getconn()
        self.bag.append(conn)
        cur = conn.cursor(cursor_factory=DictCursor)
        return cur

    def run_and_fetch(self, query_text, vals=''):
        cursor = self.__enter__()
        cursor.execute(query_text, vals)
        try:
            return cursor.fetchall()
        except:
            return f'no value to fetch'

    def __exit__(self, *args):
        conn = self.bag.pop()
        conn.commit()
        self.connections.putconn(conn)


############ query func - working only with connection pooling ##########
def query(path, query_name,  vals=''):

    file_name = query_name+'.sql'
    path = Path(path) / file_name

    with open(path, 'r') as f:
        query_text = str(f.read())
        f.close()
    cur = g.cur
    with cur:
        rows = cur.run_and_fetch(query_text,  vals=vals)
        if rows != 'no value to fetch':
            return rows
