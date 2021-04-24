from utility.helpers import query, conv_datetime
import arrow


class Activity():

    def __init__(self):
        pass

    def add(self, action, description, date, time, user_id, contact_id):

        arrow_time = conv_datetime(date, time)
        if query('contact/presence', vals=(contact_id,)).fetchone()['count'] >= 1:
            return query('activity/insert', vals=(action,
                                       description, arrow_time, user_id, contact_id))
        else:
            return False


    def get_all(self, contact_id):
        if query('contact/presence' , vals = (contact_id,)).fetchone()['count'] >= 1:
            cur = query('activity/get_all', vals=(contact_id,))
            return cur
        else: 
            return False

    def delete(self,contact_id, activity_id):
        if query('contact/presence' , vals = (contact_id,)).fetchone()['count'] >= 1:
            if query('activity/presence', vals=(activity_id,)).fetchone()['count'] >= 1:
                return query('activity/delete', vals=(activity_id, ))

            else: return (False, 'activity was not found!')
        else: return (False, 'contact was not found!')
