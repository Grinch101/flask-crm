
class Contact():
    def __init__(self):
        
        self.db = []

    def insert(self,client_name,name,phone):
        self.client_name = client_name
        self.name = name
        self.phone = phone
        entry = {   'client_name':self.client_name,
                    'name':name,
                    'phone': phone  }
        self.db.append(entry)
    
    def GetAll(self):
      return self.db
        
      
      def __len__(self):
        return len(self.db)
    
