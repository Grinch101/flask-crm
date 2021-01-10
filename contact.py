

class Contact():
    def __init__(self):
        
        self.db = []
        self.id = 0
        # helper dictionaries:
        
        self.id_index_dict = {}
        self.id_phone_dict = {}
    def insert(self,client_name,name,phone):
        
        entry = {   'client_name':client_name,
                    'name':name,
                    'phone': phone,
                    'id':  self.id }
        self.db.append(entry)
        
        
        ## side dics:
        self.id_phone_dict[phone] = self.id
        self.id_index_dict[self.id] = len(self.db) - 1

        self.id += 1

    def find_index(self,id):
        
        
        return self.id_index_dict[id]

    def find_val(self,id): # returns value corresponding to i
        
        return self.db[self.find_index(id)]



    def GetAll(self):

        return self.db


    def delete(self, id):
        
        
        try:
            self.db.remove(self.find_val(id))

            del self.id_index_dict[id]
            del self.id_phone_dict[id]          
    
            for id in range(id+1,len(self.db)):
            
                self.id_index_dict[id] -= 1
        
        except:
            pass

        
    

    def update(self , id , new_client , new_name , new_phone):
        
        self.delete(id)
        new_entry = {   'client_name':new_client,
                    'name':new_name,
                    'phone': new_phone,
                    'id':id  }

        self.db.append(new_entry)

        self.db = sorted( self.db , key = lambda dic: dic['id'] )

      
    def __len__(self):
        return len(self.db)
    
