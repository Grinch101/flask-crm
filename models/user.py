from models.BaseModel import BaseModel


class User(BaseModel):

    def __init__(self):
        self.email_userid = {}
        super().__init__()

    def add(self, entry):
        userid = super().add(entry)
        email = entry['email']
        self.email_userid[email] = userid

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

        super().delete(userid)
        del self.id_index[userid]
        for userid in range(userid+1, len(self.list)+1):
            self.id_index[userid] -= 1

    def find_userid_by_email(self, email):

        return self.email_userid.get(email)
