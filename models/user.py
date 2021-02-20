from utility.helpers import query
from flask import g


####
class User():
    
    def __init__(self):
        pass

    def add(self, client_name, email, password):

        query('user/register',
              vals=(client_name, email, password))


    def validate(self, email, password):

        query('user/find_by_email', vals=(email,))

        row = g.cur.fetchone()

        if row is None or row == []:
            return False
        else:
            return password == row['passkey']


    def old_user(self, email):

        query('user/find_by_email', vals=(email,))
        row = g.cur.fetchall()
        if row is None or row == []:
            return False


    def delete(self, user_id):

        query('user/delete', vals=(user_id,))


    def find_by_email(self, email):

        query('user/find_by_email', vals=(email,))
        rows = g.cur.fetchone()
        return rows


    def get_all(self):

        query('user/get_all')
        rows = g.cur.fetchall()
        dic_list = []
        for row in rows:
            dic_list.append(
                {'client_name': row['client_name'],
                    'email': row['email'],
                    'password': row['passkey'],
                    'user_id': row['id']})
        return dic_list


    def update(self, row_id, new_entry):

        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        query('user/update',
              vals=(email, password, client_name, row_id))


    def find_by_id(self, user_id):
        
        query('user/find_by_id', vals=(user_id,))
        row = g.cur.fetchone()
        entry = {'client_name': row['client_name'],
                 'email': row['email'],
                 'password': row['passkey'],
                 'user_id': row['id']}
        return row


    def clear_all(self):

        query('user/truncate')
