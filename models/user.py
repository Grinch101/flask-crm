from utility.helpers import query
from utility.decor import path_set


####
class User():
    def __init__(self):
        pass

    @path_set(path='SQL/user')
    def add(self, client_name, email, password, cur,  path):

        query(cur, path, 'register',
              vals=(client_name, email, password))

    @path_set(path='SQL/user')
    def validate(self, email, password, cur,  path):

        rows = query(cur, path, 'validate', vals=(email,))
        # print(rows)
        if rows is None:
            return False
        elif rows == []:
            return False
        else:
            inquired_password = rows[0]['passkey']
            return password == inquired_password

    @path_set(path='SQL/user')
    def old_user(self, email, cur, path):

        email_list = query(cur, path, 'old_user')
        email_list = [x['email'] for x in email_list]
        return email in email_list

    @path_set(path='SQL/user')
    def delete(self, userid,  cur, path):

        query(cur, path,  'delete', vals=(userid,))

    @path_set(path='SQL/user')
    def find_userid_by_email(self, email,  cur,  path):

        cur = query(cur,  path, 'userid_email', vals=(email,))
        return cur[0]['userid']

    @path_set(path='SQL/user')
    def get_all(self, cur,  path):

        rows = query(cur,  path, 'get_all')
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

    @path_set(path='SQL/user')
    def update(self, userid, new_entry, cur,  path):
        email = new_entry['email']
        password = new_entry['password']
        client_name = new_entry['client_name']

        query(cur,  path, 'update',
              vals=(email, password, client_name))

    @path_set(path='SQL/user')
    def find_val(self, userid, cur,  path):
        value = query(cur,  path, 'find_val', vals=(userid,))
        # rows = self._query(User_queries.get_all)
        dic_list = []
        for row in value:
            dic_list.append(
                {'client_name': row['client_name'],
                    'password': row['passkey'],
                    'userid': row['userid']})
        return dic_list[0]

    @path_set(path='SQL/user')
    def clear_all(self, cur,  path):
        query(cur,  path, 'truncate')

    def __init__(self):
        pass
