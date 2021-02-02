from utility.helpers import query 
from utility.decor import path_set


####
class Contact():
    def __init__(self):
        pass

    @path_set(path='SQL/contact')
    def add(self, userid, contact_name, contact_phone, cur,  path):

        query(cur,  path, 'insert',
              vals=(userid, contact_name, contact_phone))

    @path_set(path='SQL/contact')
    def find_book(self, userid, cur,  path):

        try:
            rows = query(cur,  path, 'find', vals=(userid,))
            dic_list = []
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'name': row['contact_name'],
                     'phone': row['contact_phone'],
                     'id': row['id']})
            return dic_list
        except:
            return []

    @path_set(path='SQL/contact')
    def get_all(self, cur,  path):

        try:
            rows = query(cur,  path, 'get_all')
            dic_list = []
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'name': row['contact_name'],
                     'phone': row['contact_phone']})
            return dic_list
        except:
            return []

    @path_set(path='SQL/contact')
    def delete(self, row_id, cur, path):

        query( cur, path, 'delete', vals=(row_id,))

    @path_set(path='SQL/contact')
    def update(self, row_id, new_entry, cur,  path):

        userid = new_entry['userid']
        contact_name = new_entry['name']
        contact_phone = new_entry['phone']

        query(cur,  path, 'update', vals=(contact_name,
                                                          contact_phone, userid))

    @path_set(path='SQL/contact')
    def clear_all(self, cur,  path):
        query(cur,  path, 'truncate')
