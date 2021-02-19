from utility.helpers import query
from utility.decor import path_set
from flask import g


####
class User():
    def __init__(self):
        self.path='SQL/user'

    def add(self, client_name, email, password):
        query(self.path, 'register',
              vals=(client_name, email, password))

    def validate(self, email, password):
        query(self.path, 'validate', vals=(email,))
        row = g.cur.fetchone()

        if row is None or row == []:
            return False
        else:
            return password == row['passkey']

    def old_user(self, email):
        query(self.path, 'old_user', vals=(email,))
        appear_num = g.cur.fetchall()
        return appear_num != 0

    def delete(self, userid):
        query(self.path,  'delete', vals=(userid,))

    def find_by_email(self, email):
        query(self.path, 'userid_email', vals=(email,))
        rows = g.cur.fetchone()
        return rows

    def get_all(self):
        query(self.path, 'get_all')
        rows = g.cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'client_name': row['client_name'],
                    'email': row['email'],
                    'password': row['passkey'],
                    'userid': row['userid']})
        return dic_list

    def update(self, userid, new_entry):
        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        query(self.path, 'update',
              vals=(email, password, client_name))

    def find_val_by_id(self, userid):
        query(self.path, 'find_val_by_id', vals=(userid,))
        row = g.cur.fetchone()
        entry = {'client_name': row['client_name'],
                 'email': row['email'],
                 'password': row['passkey'],
                 'userid': row['userid']}
        return row

    def clear_all(self):
        query(self.path, 'truncate')
