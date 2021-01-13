class User():
    def __init__(self):

        self.users_list = []
        # self.userid_password = {}
        self.email_userid = {}
        # self.userid_username = {}
        self.userid = 0
        self.userid_index = {}

    def register(self,client_name, email, password):
        
        entry = {'client_name' : client_name,
                'email': email,
                'password':password,
                'userid': self.userid }
        
        self.users_list.append(entry)
        self.userid_index[self.userid] = len(self.users_list) - 1
        self.email_userid[email] = self.userid
        # self.userid_username[self.userid] = client_name
        # self.userid_password[self.userid] = password

        self.userid  = self.userid + 1


    def find_index(self,userid):
        
        return self.userid_index.get(userid)


    def find_val(self,userid):

        return self.users_list[self.find_index(userid)] # returns entry dictionary created in register()
    

    def validate(self,email,password):
        if email in self.email_userid.keys():
            userid = self.email_userid[email]
            entry = self.find_val(userid)
            return entry.get('password') == password
        else: False


    def old_user(self, email): # returns True if the entered email is already in our database

        email_lists = list(self.email_userid.keys())
        return email in email_lists


    def delete(self,userid):

        entry = self.find_val(userid)
        self.users_list.remove(entry)
        del self.userid_index[userid]
        
        for userid in range(userid+1 , len(self.users_list)):
            self.userid_index[userid] -= 1 
            # now, index of entries after the deleted entry are shorter by 1 than before
        
        # edit email/userid dic:
        email = entry.get('email')
        del self.email_userid[email]


    def update(self, userid, new_value , entity = 'email'):
        
            old_entry = self.find_val(userid) # find the previous value
            new_entry = old_entry               # copy the previous value
            # self.delete(userid)               # delete the previous one
            new_entry[entity] = new_value       # update the given entity with the given value
            index = self.find_index(userid)     # find the index of the entry
            self.users_list[index] = new_entry  # set the new entry in the previous index
            
            # edit email/userid dic:
            if entity == 'email':
                email = old_entry['email']
                del self.email_userid[email]
                self.email_userid[new_value] = userid
            
    def find_userid_by_email(self,email):
        return self.email_userid.get(email)
        

    
