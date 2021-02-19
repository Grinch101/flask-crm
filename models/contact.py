from utility.helpers import query
from utility.decor import path_set
from flask import g


####
class Contact():
    def __init__(self):
        self.path = 'SQL/contact'

    def add(self, userid, contact_name, contact_phone):

        query(self.path, 'insert',
              vals=(userid, contact_name, contact_phone))

    def find_by_user(self, userid):
        query(self.path, 'get_by_id', vals=(userid,))
        rows = g.cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'client_name': row['client_name'],
                    'name': row['contact_name'],
                    'phone': row['contact_phone'],
                    'id': row['id']})
        return dic_list

    def get_all(self):
        query(self.path, 'get_all')
        rows = g.cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'name': row['contact_name'],
                 'phone': row['contact_phone'],
                 'userid': row['userid']})
        return dic_list

    def delete(self, row_id):
        query(self.path, 'delete', vals=(row_id,))

    def update(self, row_id, new_entry):

        userid = new_entry['userid']
        contact_name = new_entry['name']
        contact_phone = new_entry['phone']

        query(self.path, 'update', vals=(contact_name,
                                         contact_phone, userid))

    def clear_all(self):
        query(self.path, 'truncate')
