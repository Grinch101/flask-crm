from utility.helpers import query


class Activity():

    def __init__(self):
        pass

    def new_action(self, action, description, date_time, user_id, contact_id):
        query('activity/insert', vals=(action,
                                       description, date_time, user_id, contact_id))

    def get_history(self, user_id, contact_id):
        return query('activity/history', vals=(user_id, contact_id))

    def delete(self, activity_id, contact_id, user_id):
        query('activity/delete', vals=(activity_id, contact_id, user_id))
