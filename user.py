class User():
    def __init__(self):
        self.email_password = {}
        # self.email_IDname = {}

    def validate(self ,email,password):
        
        if self.email_password.get(email) == password:
            # username = self.email_IDname[email]
            # flash(f'Welcome {username}')
            Logged_in = True

            return Logged_in
        
        else:
            self.register( email, password)
            # flash(f'{IDname} your account has been created')
            return False

    def register(self, email, password):
            self.email_password[email] = password
            # self.email_IDname[email] = IDname
    

    
