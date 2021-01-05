
class Contact():
    def __init__(self):
        
        self.db = []

    def insert(self,client_name,name,phone):

        entry = {   'client_name':client_name,
                    'name':name,
                    'phone': phone  }
        self.db.append(entry)
    
    def GetAll(self):

        return self.db

    def delete(self, i):
        self.db.remove(i)
    
      
    def __len__(self):
        return len(self.db)
    
