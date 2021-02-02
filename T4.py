# from models.contact import Contact
# from models.user import User
# from utility.helpers import close_conn, open_conn
from functools import wraps
import psycopg2
import psycopg2.extras
from pathlib import Path
from models.user import User
from models.contact import Contact
from utility.helpers import query
from utility.decor import sql_connection



# DEFINE 3 HELPER FUNCTIONS:


@sql_connection
def test_set(cur, conn):

    # cur = kwargs['cur']
    # conn = kwargs['conn']
    # path = kwargs['path']

    user = User()
    phonebok = Contact()

    user.clear_all(cur , conn)
    phonebok.clear_all(cur , conn)

    user.add('Os Akbar','Os@gmail.com',"fireboy", cur, conn )
    print('Os Akbar added')

    akbar_id = user.find_userid_by_email('Os@gmail.com', cur, conn)
    print(f"Os Akbar's ID is {akbar_id}")

    output = user.validate('Os@gmail.com' , 'fireboy',cur,conn)
    print(output)

    phonebok.add(akbar_id, 'Gholam Safkar', 1, cur, conn)
    print(f"Gholam number's saved to Os Akbar's phonebook")


test_set()
