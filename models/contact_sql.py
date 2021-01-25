import psycopg2
import psycopg2.extras
from SQL_commands import Contact_queries


host = 'localhost'
database = 'phonebook'
user = 'postgres'


class Contact():
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

        userid = entry['userid']
        contact_name = entry['name']
        contact_phone = entry['phone']

        self._query(Contact_queries.add,
                    contact_name, contact_phone, userid)

    def find_book(self, userid):
        try:
            rows = self._query(Contact_queries.find,
                               userid)
            dic_list = []
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'name': row['contact_name'],
                     'phone': row['contact_phone']})
            return dic_list
        except:
            return []

    def get_all(self):
        try:
            rows = self._query(Contact_queries.get_all)
            dic_list = []
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'name': row['contact_name'],
                     'phone': row['contact_phone']})
            return dic_list
        except:
            return []

    def delete(self, row_id):
        self._query(Contact_queries.delete, row_id)

    def update(self, row_id, new_entry):
        userid = new_entry['userid']
        contact_name = new_entry['name']
        contact_phone = new_entry['phone']

        self._query(Contact_queries.update,
                    contact_name, contact_phone, userid)

    def clear_all(self):
        self._query(Contact_queries.truncate)
