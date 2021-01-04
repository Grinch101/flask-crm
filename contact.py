
class Contact():
    def __init__(self,client_name):
        mylist = []
        self.client_name = client_name
        self.mylist = mylist

    def saver(self,new_item): # new item is a tuple
        mylist=self.mylist
        mylist.append(new_item)

    def reporter(self):
         return self.mylist

    def __repr__(self):
        return f" {self.client_name} has saved {len(self.mylist)} contact(s)"
