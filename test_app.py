import unittest
from models.BaseModel import BaseModel
import names
import random


class TestBaseModel(unittest.TestCase):
    def setUp(self):
        self.app = BaseModel()

    def test_add(self):
        added_entry = {'name':'Asghar',
                       'number':666}
        self.app.add(added_entry)
        entities = self.app.get_all()
        len_entities = len(entities)
        self.assertEqual(1,len_entities)

    def test_find_index(self):
        self.app.clear_all()
        entry = {'name':'Asghar',
                       'number':666}
        self.app.add(entry)
        reported_index = self.app.find_index(0)
        index = 0
        self.assertEqual(reported_index, index)
    
    def test_findval(self):
        self.app.clear_all()
        entry = {'name':'Asghar',
                       'number':666}
        self.app.add(entry)
        
        found_val = self.app.find_val(0)
        val = {'name':'Asghar',
               'number':666,
               'id':0}
        self.assertEqual(found_val,val)
    
    def test_get_all(self):
        self.app.clear_all()
        entry = {'name':'Asghar',
                       'number':666}
        self.app.add(entry)

        got_val = self.app.get_all()
        val = {'name':'Asghar',
                'number':666,
                'id':0}
        self.assertEqual(got_val , [val])
    
    def test_delete(self):
        self.app.clear_all()

        enum_list = []
        database = []
        for i in range(5):
            name = names.get_first_name()
            number = random.randint(1,100)
            entry = {'name':name,
                    'number':number}
            self.app.add(entry)
            enum_list.append(i)
            database.append(entry)

        for i in enum_list:
            deleted_entry = self.app.delete(i)
            del deleted_entry['id']

            self.assertEqual(deleted_entry , database[i])
    
    def test_update(self):
        self.app.clear_all()

        enum_list = []
        database = []
        for i in range(5):
            name = names.get_first_name()
            number = random.randint(1,100)
            entry = {'name':name,
                    'number':number}
            self.app.add(entry)
            enum_list.append(i)
            database.append(entry)
        
        for i in enum_list:
            self.app.update(i , {'test':'update','token':i} )

            self.assertEqual(self.app.find_val(i) , {'test':'update','token':i})


if __name__ == "__main__":
    unittest.main()





