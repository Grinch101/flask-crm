
class BaseModel:
    def __init__(self):
        self.list = []
        self.id_index = {}
        self.id_sequence_counter = 0

    def add(self, entry):

        entry['id'] = self.id_sequence_counter
        self.list.append(entry)

        self.id_index[self.id_sequence_counter] = len(self.list) - 1
        self.id_sequence_counter += 1
        return self.id_sequence_counter - 1

    def find_index(self, id):
        return self.id_index[id]

    def find_val(self, id):
        index = self.id_index[id]
        return self.list[index]

    def get_all(self):
        return self.list
    
    def clear_all(self):
        self.list = []
        self.id_index = {}
        self.id_sequence_counter = 0

    def delete(self, id):
    
        entry = self.find_val(id)
        self.list.remove(entry)

        del self.id_index[id]
        # find ids after id, and reduce their indexes by 1:
        for i in self.id_index.keys(): ## BUG NUMBER 1
            if i > id:
                self.id_index[i]  -= 1
        return entry


    def update(self, id, new_entry):

        index = self.find_index(id)  ## BUG NUMBER 2
        self.list[index] = new_entry
