from utility.helpers import query 
from utility.decor import path_set

#####
class Contact():
    def __init__(self):
        pass
    
    @path_set(path = 'SQL/contact')
    def add(self, userid , contact_name , contact_phone, **kwargs):
    
        query( query_name='insert',  vals=(userid, contact_name,contact_phone)  , **kwargs)

    @path_set(path = 'SQL/contact')
    def find_book(self, userid, **kwargs):

        try:
            rows = query(query_name='find', vals=(userid,) , **kwargs)
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

    @path_set(path = 'SQL/contact')
    def get_all(self, *args, **kwargs):

        try:
            rows = query(query_name='get_all' , **kwargs)
            dic_list = []
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'name': row['contact_name'],
                     'phone': row['contact_phone']})
            return dic_list
        except:
            return []

    @path_set(path = 'SQL/contact')
    def delete(self, row_id, **kwargs):

        query( query_name='delete', vals=(row_id,) , **kwargs)

    @path_set(path = 'SQL/contact')
    def update(self, row_id , new_entry, **kwargs):

        userid = new_entry['userid']
        contact_name = new_entry['name']
        contact_phone = new_entry['phone']

        query(query_name='update', vals=(contact_name,
                                     contact_phone, userid) , **kwargs)

    @path_set(path = 'SQL/contact')
    def clear_all(self, *args, **kwargs):
        query( query_name='truncate' , **kwargs)
