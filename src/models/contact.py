from utility.helpers import query
from psycopg2.extras import DictCursor
from psycopg2.extensions import AsIs
from flask import g


####
class Contact():

    def __init__(self):
        pass

    def add(self, user_id, name, phone):
        return query('contact/insert',
                     vals=(user_id, name, phone))

    def get_by_user(self, user_id):
        return query('contact/get_by_user', vals=(user_id,))

    def get_by_id(self, row_id):
        if query('contact/presence',
                 vals=(row_id,)).fetchone()['count'] >= 1:
            cur = query('contact/get_by_id', vals=(row_id,))
            if cur:
                return cur.fetchone()
        else:
            return False

    def get_all(self, user_id):

        return query('contact/get_all', vals=(user_id,))

    def delete(self, row_id):
        if query('contact/presence',
                 vals=(row_id,)).fetchone()['count'] >= 1:
            # Can you suggest sth better?
            return query('contact/delete', vals=(row_id, row_id))
        else:
            return False

    def update(self, user_id, contact_id, new_name, new_phone):
        cur = query('contact/get_by_id', vals=(contact_id,))
        if cur.fetchone()['user_id'] == user_id:
            if query('contact/presence',
                     vals=(contact_id,)).fetchone()['count'] >= 1:
                return query('contact/update',
                             vals=(new_name, new_phone, contact_id,
                                   user_id))
            else:
                return (False, '400')
        else:
            return (False, "401")

    def clear_all(self):
        return query('contact/truncate')
