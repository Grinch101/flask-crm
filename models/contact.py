from models.BaseModel import BaseModel


class Contact(BaseModel):

    def __init__(self):
        self.userid_id = {}
        super().__init__()

    def add(self, entry):

        id = super().add(entry)

        # extract the userid back, add to helper dictionaries:
        userid = entry['userid']

        if self.userid_id.get(userid):
            self.userid_id[userid].append(id)
        else:
            self.userid_id[userid] = [id]

    def find_book(self, userid):
        try:
            entry_list = self.userid_id.get(userid)
            return [self.find_val(id) for id in entry_list]
        except:
            return []
