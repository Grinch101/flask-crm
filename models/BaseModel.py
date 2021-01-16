class BaseModel:
    def __init__(self):
        self.list = []
        self.id_index = {}
        self.id_sequence_counter = 0
        
    def add(self, entry):
        
        self.list.append(entry)

        userid = entry['userid'] # Applicable in Contact.py Only
        if userid:
            if self.userid_id.get(userid):
                self.userid_id[userid].append(self.id_sequence_counter)
            else:
                self.userid_id[userid] = [self.id_sequence_counter]
            
        self.id_index[self.id_sequence_counter] = len(self.list) - 1
        
        self.id_sequence_counter += 1


    def find_index(self,id_sequence_counter):
        return self.id_index[id_sequence_counter]
    
    def find_val(self,id_sequence_counter):
        index = self.find_index(id_sequence_counter)
        return self.list[index]

    def get_all(self):
        return self.list
    
    def delete(self, id_sequence_counter):
        
        entry = self.find_val(id_sequence_counter)
        self.list.remove(entry)
        del entry
    
    def update(self, id_sequence_counter, new_entry):
        
        index = self.find_index[id_sequence_counter]
        self.list[index] = new_entry
        
    


