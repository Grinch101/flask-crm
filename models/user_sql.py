

import psycopg2
import psycopg2.extras
from SQL_commands import User_queries

host = 'localhost'
database = 'phonebook'
user = 'postgres'


class User():
    def __init__(self):
        pass

    def _query(self, query, *vals):
        conn = psycopg2.connect(host=host,
                                database=database,
                                user=user,
                                password=1)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, tuple(vals))
        conn.commit()
        try:
            return cur.fetchall()
        except:
            pass

        cur.close()
        conn.close()

    def add(self, entry):
        client_name = entry['client_name']
        email = entry['email']
        password = entry['password']

        self._query(User_queries.register,
                    client_name, email, password)

    def validate(self, email, password):

        cur = self._query(User_queries.validate, email)
        inquired_password = cur[0]['passkey']

        return password == inquired_password

    def old_user(self, email):

        email_list = self._query(User_queries.old_user)
        email_list = [x['email'] for x in email_list]
        return email in email_list

    def delete(self, userid):

        self._query(User_queries.delete, userid)

    def find_userid_by_email(self, email):

        cur = self._query(User_queries.userid_email, email)
        return cur[0]['userid']

    def get_all(self):
        try:
            rows = self._query(User_queries.get_all, userid)
            dic_list = []
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'password': row['passkey'],
                     'userid': row['userid']})
            return dic_list
        except:
            return []

    def update(self, userid, new_entry):
        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        self._query(User_queries.update,
                    email, password, client_name)
    
    def find_val(self,userid):
        value = self._query(User_queries.find_val, userid)
                    # rows = self._query(User_queries.get_all)
        dic_list = []
        for row in value:
            dic_list.append(
                {'client_name': row['client_name'],
                    'password': row['passkey'],
                    'userid': row['userid']})
        return dic_list[0]
    
    def clear_all(self):
        self._query(User_queries.truncate)
