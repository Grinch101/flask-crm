from models.BaseModel import BaseModel


class User(BaseModel):

    def __init__(self):
        self.email_userid = {}
        # self.userid = 0
        super().__init__()

    # def add(self, entry):
    #     entry = {'client_name': client_name,
    #              'email': email,
    #              'password': password}
    #     super().add(entry)
        
        # self.id_index[self.id_sequence_counter] = len(self.list) - 1
        # self.email_userid[email] = self.id_sequence_counter

        # self.id_sequence_counter += 1

#     def find_index(self,userid):
#         return self.id_index[userid]

#     def find_val(self,userid):
#         index = self.find_index(userid)
#         return self.list[index]

    def validate(self, email, password):

        if self.old_user(email):
            userid = self.email_userid[email]
            entry = self.find_val(userid)
            return entry['password'] == password
        else:
            False

    def old_user(self, email):

        emails = list(self.email_userid.keys())
        return email in emails

    def delete(self, userid):

        entry = self.find_val(userid)
        super().delete(entry)
        del self.id_index[userid]
        for userid in range(userid+1, len(self.list)+1):
            self.id_index[userid] -= 1

    # def update(self, userid, new_value, entity='email'):

    #     old_entry = self.find_val(userid)
    #     if entity == 'email':
    #         email = old_entry.get('email')
    #         del self.email_userid[email]
    #         self.email_userid[new_value] = userid

    #     new_entry = old_entry
    #     new_entry[entity] = new_value

    #     super().update(userid, new_entry)

    def find_userid_by_email(self, email):

        return self.email_userid.get(email)
