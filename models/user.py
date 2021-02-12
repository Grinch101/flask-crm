from utility.helpers import query
from utility.decor import path_set


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

        rows = query(path, 'validate', vals=(email,))
        # print(rows)
        if rows is None or rows==[]:
            return False
        else:
            inquired_password = rows[0]['passkey']
            return password == inquired_password

    @path_set(path='SQL/user')
    def old_user(self, email, path):

        email_list = query(path, 'old_user')
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

        rows = query(path, 'userid_email', vals=(email,))
        return rows[0]['userid']

    @path_set(path='SQL/user')
    def get_all(self, path):

        rows = query(path, 'get_all')
        return rows
        # dic_list = []
        # try:
        #     for row in rows:
        #         dic_list.append(
        #             {'client_name': row['client_name'],
        #              'password': row['passkey'],
        #              'userid': row['userid']})
        #     return dic_list
        # except:
        #     return []

    @path_set(path='SQL/user')
    def update(self, userid, new_entry, path):
        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        query(path, 'update',
              vals=(email, password, client_name))

    @path_set(path='SQL/user')
    def find_val(self, userid, path):
        rows = query(path, 'find_val', vals=(userid,))
        return rows[0]
        # rows = self._query(User_queries.get_all)
        # dic_list = []
        # for row in value:
        #     dic_list.append(
        #         {'client_name': row['client_name'],
        #             'password': row['passkey'],
        #             'userid': row['userid']})
        # return dic_list[0]
        
    @path_set(path='SQL/user')
    def clear_all(self, path):
        query(path, 'truncate')
