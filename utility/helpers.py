import psycopg2
import psycopg2.extras
from pathlib import Path


# DEFINE 3 HELPER FUNCTIONS:

def open_conn(host='localhost', database='phonebook', user='postgres', password=1):
    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=1)

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return cur, conn


def close_conn(cur, conn):
    conn.commit()
    cur.close()
    conn.close()




def query(cur, path, query_name,  vals=''):

    file_name = query_name+'.txt'
    path = Path(path) / file_name

    with open(path, 'r') as f:
        query_text = str(f.read())
        f.close()

    cur.execute(query_text,  vals)
    try:
        rows = cur.fetchall()
        return rows
    except:
        pass

