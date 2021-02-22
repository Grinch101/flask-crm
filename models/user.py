from utility.helpers import query
from flask import g


####
class User():
    
    def __init__(self):
        pass

    def add(self, client_name, email, password):

        return query('user/register',
              vals=(client_name, email, password))


    def validate(self, email, password):

        cur = query('user/find_by_email', vals=(email,))

        row = cur.fetchone()

        if row is None or row == []:
            return False
        else:
            return password == row['passkey']


    def old_user(self, email):

        cur = query('user/find_by_email', vals=(email,))
        row = cur.fetchall()
        if row is None or row == []:
            return False
        else:
            return True


    def delete(self, user_id):

        return query('user/delete', vals=(user_id,))


    def find_by_email(self, email):

        return query('user/find_by_email', vals=(email,))


    def get_all(self):

        return query('user/get_all')


    def update(self, row_id, new_entry):

        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        return query('user/update',
              vals=(email, password, client_name, row_id))


    def find_by_id(self, user_id):
        
        return query('user/find_by_id', vals=(user_id,))


    def clear_all(self):

        query('user/truncate')
