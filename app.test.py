
import names
import random
from models.BaseModel import BaseModel


def tester(Model):

    myobject = Model()
    my_counter = 0
    # create data:

    for i in range(100):
        client_name = names.get_first_name() + "$" + str(my_counter)
        name = names.get_full_name() + "$" + str(my_counter)


        entry = {"client_name": client_name,
                 "name": name
                 }
        my_counter += 1  # mimic the id
        myobject.add(entry)


# Checking delete functionality

    delete_random_ids = []
    while len(delete_random_ids) <= 20:
        r = random.randint(1, 99)
        if r not in delete_random_ids:
            # generate 20 non-repeating random numbers
            delete_random_ids.append(r)

    for id in delete_random_ids:
        myobject.delete(id)

    entry_list = myobject.get_all()

    # get the ids and check with the originals
    acquired_ids = []
    set_ids = []
    for item in entry_list:

        my_counter_value = int((item['client_name']).split("$")[-1])
        acquired_ids.append(my_counter_value)
        set_ids.append(item['id'])

    assert set_ids == acquired_ids, "id do not match, delete failed"


# Checking find_val() functionality:
    remained_ids = list(myobject.id_index.keys())
    random_findval_list = []

    while len(random_findval_list) < 50:
        j = random.choice(remained_ids)
        if j not in random_findval_list:
            random_findval_list.append(j)

    for id in random_findval_list:
        item = myobject.find_val(id)
        assigned_id = item['id']
        name_value = int(item['client_name'].split("$")[-1])

        assert name_value == assigned_id, "id does not match, find_val failed"


# Checking update() functionality:
    random_update_list = []

    while len(random_update_list) < 50:
        j = random.choice(remained_ids)
        if j not in random_update_list:
            random_update_list.append(j)

    for id in random_update_list:
        new_client_name = f"TEST ${id}"     # new signature implemented
        name = myobject.find_val(id)['name']  # untouched since add()

        new_entry = {'client_name': new_client_name,
                     'name': name
                     }

        old_id = myobject.find_val(id)['id']

        myobject.update(id, new_entry)

        searched_value = myobject.find_val(id)

        assert int(searched_value['client_name'].split(
            '$')[-1]) == int(searched_value['name'].split('$')[-1]), "id doesn't match, update failed"

    return "*** EVERYTHING'S FINE ***"


if __name__ == "__main__":
    print(tester(BaseModel))
    