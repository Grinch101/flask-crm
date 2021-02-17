from utility.helpers import query
from utility.decor import path_set
from flask import g



####
class User():
    def __init__(self):
        pass

    @path_set(path='SQL/user')
    def add(self, client_name, email, password, path):

        query(path, 'register',
              vals=(client_name, email, password))

    @path_set(path='SQL/user')
    def validate(self, email, password, path):

        query(path, 'validate', vals=(email,))
        cur = g.cur 
        row = cur.fetchone()

        if row is None or row==[]:
            return False
        else:
            inquired_password = row['passkey']
            return password == inquired_password

    @path_set(path='SQL/user')
    def old_user(self, email, path):

        query(path, 'old_user')
        cur = g.cur 
        email_list = cur.fetchall()
        for record in email_list:
            if record == email:
                return True
            else:
                return False

    @path_set(path='SQL/user')
    def delete(self, userid, path):

        query(path,  'delete', vals=(userid,))

    @path_set(path='SQL/user')
    def find_userid_by_email(self, email, path):

        query(path, 'userid_email', vals=(email,))
        cur = g.cur
        rows = cur.fetchone()
        return rows['userid']

    @path_set(path='SQL/user')
    def get_all(self, path):

        query(path, 'get_all')
        cur  = g.cur
        rows  = cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'client_name': row['client_name'],
                    'email': row['email'],
                    'password': row['passkey'],
                    'userid': row['userid']})
        return dic_list
        

    @path_set(path='SQL/user')
    def update(self, userid, new_entry, path):
        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        query(path, 'update',
              vals=(email, password, client_name))

    @path_set(path='SQL/user')
    def find_val_by_id(self, userid, path):
        query(path, 'find_val_by_id', vals=(userid,))
        cur = g.cur
        row = cur.fetchone()
        entry = {'client_name': row['client_name'],
                    'email': row['email'],
                    'password': row['passkey'],
                    'userid': row['userid']}
        return row
        
    @path_set(path='SQL/user')
    def clear_all(self, path):
        query(path, 'truncate')
