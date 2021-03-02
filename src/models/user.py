from utility.helpers import query


####
class User():
    
    def __init__(self):
        pass

    def add(self, client_name, email, password):

        return query('user/register',
              vals=(client_name, email, password))


    def get_by_email(self, email):

        cur = query('user/get_by_email', vals=(email,))
        return cur.fetchone()

        
    def validate(self, email, password):

        row = self.get_by_email(email)

        if row is None or row == []:
            return False
        else:
            return password == row['passkey']


    def delete(self, user_id):

        return query('user/delete', vals=(user_id,))



    def get_all(self):

        return query('user/get_all')


    def update(self, row_id, new_entry):

        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        return query('user/update',
              vals=(email, password, client_name, row_id))


    def get_by_id(self, user_id):
        
        cur = query('user/get_by_id', vals=(user_id,))
        return cur.fetchone()


    def clear_all(self):

        query('user/truncate')
