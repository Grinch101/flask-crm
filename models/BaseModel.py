class BaseModel:
    def __init__(self):
        self.list = []
        self.id_index = {}
        self.id_sequence_counter = 0
        
    def add(self, entry):
        
        self.list.append(entry)


        self.id_index[self.id_sequence_counter] = len(self.list) - 1
        
        self.id_sequence_counter += 1


    def find_index(self,id):
        return self.id_index[id]
    
    def find_val(self,id):
        index = self.find_index(id)
        return self.list[index]

    def get_all(self):
        return self.list
    
    def delete(self, id):
        
        entry = self.find_val(id)
        self.list.remove(entry)
        del entry
    
    def update(self, id, new_entry):
        
        index = self.find_index[id]
        self.list[index] = new_entry
        
    


