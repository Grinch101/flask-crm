class BaseModel:
    def __init__(self):
        self.list = []
        self.id_index = {}
        
    def add(self, entry):
        
        self.list.append(entry)
    
#     def find_index(self,entry):
#         for i, item in self.list:
#             if item==entry:
#                 return i
            
#     def find_val(self,index):
#         return self.list[index]

#####################

    def find_index(self,id):
        return self.id_index[id]
    
    def find_val(self,id):
        index = self.find_index(id)
        return self.list[index]


###################
    def GetAll(self):
        return self.list
    
    def delete(self, entry):
        
        self.list.remove(entry)
    
    def update(self,id, new_entry):
        
        index = self.id_index[id]
        self.list[index] = new_entry
        
    

class User(BaseModel):
    
    def __init__(self):
        self.email_userid = {}
        self.userid = 0
        super().__init__()
        
    
    def register(self, client_name, email, password):
        entry = {'client_name' : client_name,
                'email': email,
                'password':password,
                'userid': self.userid }
        self.add(entry = entry)
        self.id_index[self.userid] = len(self.list) - 1
        self.email_userid[email] = self.userid
        
        self.userid += 1
        
#     def find_index(self,userid):
#         return self.id_index[userid]
    
#     def find_val(self,userid):
#         index = self.find_index(userid)
#         return self.list[index]
    
    def validate(self,email,password):
        
        if self.old_user(email):
            userid = self.email_userid[email]
            entry = self.find_val(userid)
            return entry['password'] == password
        else:
            False
        
    def old_user(self,email):
        
        emails = list(self.email_userid.keys())
        return email in emails
        
    def delete(self,userid):
        
        entry = self.find_val(userid)
        super().delete(entry)
        del self.id_index[userid]
        for userid in range(userid+1 , len(self.list)+1):
            self.id_index[userid] -= 1
        
    def update(self,userid,new_value,entity = 'email'):
        
        old_entry = self.find_val(userid)
        if entity == 'email':
            email = old_entry.get('email')
            del self.email_userid[email]
            self.email_userid[new_value] = userid
            
        new_entry = old_entry
        new_entry[entity] = new_value
        
        super().update(userid, new_entry)
        

    def find_userid_by_email(self,email):
        
        return self.email_userid.get(email)


class Contact(BaseModel):
    
    def __init__(self):
        self.id = 0
        self.userid_id = {}
        super().__init__()
    
    def insert(self,userid,client_name,name,phone):
        entry = {   'userid'        :userid     ,
                    'client_name'   :client_name,
                    'name'          :name       ,
                    'phone'         :phone      ,
                    'id'            :self.id    }
        self.add(entry)
        
        if self.userid_id.get(userid):
            self.userid_id[userid].append(self.id)
        else:
            self.userid_id[userid] = [self.id]
        
        self.id_index[self.id] = len(self.list) - 1
        
        self.id += 1
        
    
    def delete(self,id):
        try:
            entry = super().find_val(id)
            super().delete(entry)
            del self.id_index[id]
            for id in range(id+1,len(self.db)+1):

                    self.id_index[id] -= 1
        except:
            pass
    
    def update(self , id, new_value , entity = 'client_name' ):
        
        entry = self.find_val(id)
        entry[entity] = new_value
        super().update(id, entry)
    
    def find_book(self,userid):
        try:
            entry_list = self.userid_id.get(userid) 
            return [self.find_val(id) for id in entry_list]
        except:
            return []
    