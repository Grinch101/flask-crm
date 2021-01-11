class User():
    def __init__(self):

        self.users_list = []
        self.userid_password = {}
        self.email_userid = {}
        self.userid_username = {}
        self.userid = 0

    def validate(self,email,password):
        
        userid = self.email_userid[email]

        return self.userid_password[userid] == password


    def old_user(self, email):
        return email in self.email_userid.keys()

    def register(self,client_name, email, password):
        
        entry = {'client_name' : client_name,
                'email': email,
                'password':password,
                'userid': self.userid }
        
        self.users_list.append(entry)
        self.email_userid[email] = self.userid
        self.userid_username[self.userid] = client_name
        self.userid_password[self.userid] = password

        self.userid  = self.userid + 1

    

    
