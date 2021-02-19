from utility.helpers import query
from flask import g


####
class Contact():
    def __init__(self):
        pass

    def add(self, user_id, contact_name, contact_phone):

        query('contact/insert',
              vals=(user_id, contact_name, contact_phone))

    def find_by_user(self, user_id):
        query('contact/get_by_id', vals=(user_id,))
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
        query('contact/get_all')
        rows = g.cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'name': row['contact_name'],
                 'phone': row['contact_phone'],
                 'user_id': row['user_id']})
        return dic_list

    def delete(self, row_id):
        query('contact/delete', vals=(row_id,))

    def update(self, row_id, new_entry):

        user_id = new_entry['user_id']
        contact_name = new_entry['name']
        contact_phone = new_entry['phone']

        query('contact/update', vals=(contact_name,
                                      contact_phone, user_id))

    def clear_all(self):
        query('contact/truncate')
