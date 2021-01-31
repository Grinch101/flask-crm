from utility.helpers import query
from utility.decor import path_set


####
class User():
    def __init__(self):
        pass


    @path_set(path = 'SQL/user')
    def add(self, entry , *args, **kwargs):
        client_name = entry['client_name']
        email = entry['email']
        password = entry['password']

        query(query_name='register', vals=(client_name, email, password) , **kwargs)

    @path_set(path = 'SQL/user')
    def validate(self, email, password , *args, **kwargs):

        rows = query( query_name='validate', vals =( email ,) ,**kwargs )
        inquired_password = rows[0]['passkey']

        return password == inquired_password

    @path_set(path = 'SQL/user')
    def old_user(self, email , *args, **kwargs):

        email_list = query(query_name='old_user' , **kwargs)
        email_list = [x['email'] for x in email_list]
        return email in email_list

    @path_set(path = 'SQL/user')
    def delete(self, userid, *args, **kwargs):

        query(query_name='delete' , vals=(userid,) , **kwargs)

    @path_set(path = 'SQL/user')
    def find_userid_by_email(self, email, *args, **kwargs):

        cur = query(query_name='userid_email', vals = (email,) , **kwargs )
        return cur[0]['userid']

    @path_set(path = 'SQL/user')
    def get_all(self, *args, **kwargs):
        
        rows = query( query_name =  'get_all' , **kwargs)
        dic_list = []
        try:
            for row in rows:
                dic_list.append(
                    {'client_name': row['client_name'],
                     'password': row['passkey'],
                     'userid': row['userid']})
            return dic_list
        except:
            return []

    @path_set(path = 'SQL/user')
    def update(self, userid, new_entry, *args, **kwargs):
        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        query( query_name= 'update', vals=(email, password, client_name) , **kwargs)
    
    @path_set(path = 'SQL/user')
    def find_val(self,userid , *args, **kwargs):
        value = query(  query_name='find_val' , vals=(userid,) , **kwargs)
                    # rows = self._query(User_queries.get_all)
        dic_list = []
        for row in value:
            dic_list.append(
                {'client_name': row['client_name'],
                    'password': row['passkey'],
                    'userid': row['userid']})
        return dic_list[0]
    
    @path_set(path = 'SQL/user')
    def clear_all(self , *args, **kwargs):
        query(query_name='truncate' , *args, **kwargs)
