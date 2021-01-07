
class Contact():
    def __init__(self):
        
        self.db = []
        self.id = 0
    def insert(self,client_name,name,phone):
        
        entry = {   'client_name':client_name,
                    'name':name,
                    'phone': phone,
                    'id':  self.id }
        self.db.append(entry)
        self.id += 1


    def find_index(self,id):
        
        
        for i , dic in enumerate(self.db):
            if dic['id'] == id:
                index = i
        return index

    def find_val(self,id): # returns value corresponding to i
        
        return self.db[self.find_index(id)]



    def GetAll(self):

        return self.db


    def delete(self, id):
        delval = self.find_val(id)
        self.db.remove(delval)
    

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
    
