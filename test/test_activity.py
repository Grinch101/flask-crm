import json
import pytest
from test.conftest import extract


@pytest.fixture(scope='module')
def CONTACTS(client, TOKEN):
    # TESTING CONTACTS INSERT
    rs3 = client.post('contacts/add',
                      headers={'JWT': TOKEN},
                      data=json{'Name': 'contact for testing activity',
                            'Number': str(999)})

    rs4 = client.get('contacts/all',
                     headers={'JWT': TOKEN})
    info, data, error = extract(rs4)
    yield data
    ID = data[0]['id']
    rs5 = client.delete(f'contacts/delete/{ID}',
                        headers={'JWT': TOKEN})


def test_add_activity(client, TOKEN, CONTACTS):
    ID = CONTACTS[0]['id']
    rs = client.post(f'/activity/{ID}',
                     headers={'JWT':TOKEN},
                     data={'action':'TEST_ACTION',
                            'description':'TEST_DESC',
                            'time':'12:12',
                            'date':'2020-01-01'})
    info, data, error = extract(rs)
    assert rs.status_code == 201
    assert error is None
    assert data is not None


def test_activity_retrieve(client, TOKEN, CONTACTS):
    ID = CONTACTS[0]['id']
    rs = client.get(f'/activity/{ID}',
                     headers={'JWT':TOKEN})
    info, data, error = extract(rs)
    assert rs.status_code == 200
    assert error is None
    assert data is not None
    
    activity_id = data[0]['id']
    with open('activity_id.txt', 'w') as f:
        f.write(str(activity_id))
    


def test_delete_activity(client, TOKEN, CONTACTS):
    ID = CONTACTS[0]['id']
    with open('activity_id.txt', 'r') as f:
        activity_id = f.read()
    rs = client.delete(f'/activity/{ID}/delete/{activity_id}',
                       headers={'JWT':TOKEN})
    info, data, error = extract(rs)
    assert rs.status_code == 200
    assert error is None
    assert data is not None
