####
# ######## query func  ##########
from psycopg2.pool import ThreadedConnectionPool
def conn_pool(minconn, maxconn, / , host='localhost', database='phonebook', user='postgres', password=1):
    return ThreadedConnectionPool(minconn,
                                  maxconn,
                                  host=host,
                                  database=database,
                                  user=user,
                                  password=password)

connections = conn_pool(1,10)
conn = connections.getconn()
cur = conn.cursor()
def query(query, vals=''):



    # query_folder = query_loc.split('/')[0]
    # query_name = query_loc.split('/')[1]

    # file_name = query_name+'.sql'
    path = query
    from pathlib import Path
    path = Path(path)
    with open(path, 'r') as f:
        query_text = str(f.read())


    cur.execute(query_text,  vals)
    print(cur.fetchall())

query('sql/user/get_all.sql' )