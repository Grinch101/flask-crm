
class Contact():
    def __init__(self):
        
        self.db = []
        self.counter = 0
    def insert(self,client_name,name,phone):
        
        entry = {   'client_name':client_name,
                    'name':name,
                    'phone': phone  }
        self.db.append({self.counter : entry})
        self.counter += 1


    def find_val(self,i): # returns value corresponding to i
        
        vals = [item.get(i) for item in self.GetAll()]

        val = [x for x in vals if x is not None][0]
        return val
    

    def GetAll(self):

        return self.db

    def delete(self, i):
        delval = self.find_val(i)
        self.db.remove({i:delval})
    

    def update(self , i , new_client , new_name , new_phone):
        
        """
        i = index to be updated
        """
        self.delete(i)
        new_entry = {   'client_name':new_client,
                    'name':new_name,
                    'phone': new_phone  }

        self.db.append({i : new_entry})

        # Sort:
        keys = [ i.keys() for i in self.db  ] # Get all the present keys
        sorted_keys = sorted([list(k)[0] for k in keys]) # sort the keys

        new_db = []
        for i in sorted_keys:
            new_db.append({i:self.find_val(i)}) # Create new db with sorted keys

        self.db = new_db    # replace the old db with new one
        del new_db  
        

    def keys(self):
        keys = [ i.keys() for i in self.db  ]
        return [list(k)[0] for k in keys]

    def values(self):
        
        return [self.find_val(i) for i in self.keys()]
            

      
    def __len__(self):
        return len(self.db)
    
