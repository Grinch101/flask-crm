from utility.helpers import query, conv_datetime
import arrow


class Activity():

    def __init__(self):
        pass

    def add(self, action, description, date, time, user_id, contact_id):

        arrow_time = conv_datetime(date, time)
        query('activity/insert', vals=(action,
                                       description, arrow_time, user_id, contact_id))


    def get_all(self, contact_id):
        
        return query('activity/get_all', vals=(contact_id,))


    def delete(self, activity_id):
        if query('activity/presence', vals=(activity_id,)).fetchone()['count'] >= 1:
            return query('activity/delete', vals=(activity_id, ))
        else:
            False