from MyModels.BaseModel import BaseModel


class Contact(BaseModel):

    def __init__(self):
        # self.id = 0
        self.userid_id = {}
        super().__init__()

    def insert(self, userid, client_name, name, phone):

        entry = {'userid': userid,
                 'client_name': client_name,
                 'name': name,
                 'phone': phone,
                 'id': self.id_sequence_counter}
        self.add(entry)

    def delete(self, id_sequence_counter):

        try:
            super().delete(id_sequence_counter)
            del self.id_index[id_sequence_counter]
            for id in range(id_sequence_counter+1, len(self.list)+1):
                self.id_index[id] -= 1
        except:
            pass

    # def update(self, id_sequence_counter, new_value):

    #     entry = self.find_val(id_sequence_counter)
    #     entry[entity] = new_value
    #     super().update(id_sequence_counter, entry)

    def find_book(self, userid):
        try:
            entry_list = self.userid_id.get(userid)
            return [self.find_val(id) for id in entry_list]
        except:
            return []
