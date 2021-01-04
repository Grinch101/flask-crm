
class Contact():
    def __init__(self,client_name, name, phone):
        self.client_name = client_name
        self.name = name
        self.phone = phone

        entries = {'client_name':client_name,
                    'name':name,
                    'phone': phone
                  }
        self.entries = entries
      
      def __repr__(self):

        

db = []