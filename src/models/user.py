from utility.helpers import query


####
class User():
    
    def __init__(self):
        pass

    def add(self, client_name, email, password):

        return query('user/register',
              vals=(client_name, email, password))


    def get_by_email(self, email):
        if query('user/presence_using_email', vals=(email,)).fetchone()['count'] ==1:
            return query('user/get_by_email', vals=(email,))
        else:
            return False

        
    def validate(self, email, password):

        
        row = self.get_by_email(email)

        if row is None or row == False or row == []:
            return False
        else:
            return password == row.fetchone()['passkey']


    def delete(self, user_id):
        if query('user/presence', vals=(user_id,)).fetchone()['count']==1:
            return query('user/delete', vals=(user_id,))
        else:
            return False


    def get_all(self):

        return query('user/get_all')


    def update(self, user_id, new_email , new_name , new_password):
        if query('user/presence', vals=(user_id,)).fetchone()['count']==1:
            return query('user/update', vals=(new_email, new_password, new_name, user_id))
        else:
            return False
    

    def get_by_id(self, user_id):
        if query('user/presence', vals=(user_id,)).fetchone()['count']==1:
            cur = query('user/get_by_id', vals=(user_id,))
            return cur.fetchone()
        else:
            return False

    def clear_all(self):
        query('user/truncate')
