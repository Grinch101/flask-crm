import json
import random
import pytest
from test.conftest import extract


def test_contact_insert(client, TOKEN):
    # TESTING CONTACTS INSERT
    rs3 = client.post('contacts/add',
                      headers={'JWT': TOKEN},
                      data={'Name': f'contact name',
                            'Number': str(999)})
    info, data, error = extract(rs3)
    assert error is None
    assert data is not None
    assert rs3.status_code == 201


def test_contact_getall(client, TOKEN):
    # TESTING CONTACTS RETRIVE
    rs4 = client.get('contacts/all',
                     headers={'JWT': TOKEN})
    info, data, error = extract(rs4)
    assert error is None
    assert rs4.status_code == 200
    assert data is not None
    assert data != []


@pytest.fixture(scope='module')
def CONTACTS(client, TOKEN):
    rs5 = client.get('contacts/all',
                     headers={'JWT': TOKEN})
    info, CONTACTS, error = extract(rs5)
    yield CONTACTS


def test_contact_update(client, TOKEN, CONTACTS):
    # TESTING CONTACT UPDATE
    assert type(CONTACTS) is list
    assert len(CONTACTS) == 1
    ID = CONTACTS[0]['id']
    assert type(ID) is int
    rs5 = client.put(f'contacts/update/{ID}',
                     headers={'JWT': TOKEN},
                     data={'new_name': 'name updated',
                           'new_phone': str(999)})
    info, data, error = extract(rs5)
    assert rs5.status_code == 200
    assert error is None


def test_postupdate_status(client, TOKEN):
    # CHECK RESULTS AFTER UPDATE
    rs6 = client.get('contacts/all',
                     headers={'JWT': TOKEN})
    info, data, error = extract(rs6)
    assert error is None
    assert rs6.status_code == 200

    name = data[0]['name']
    phone = data[0]['phone']
    assert name == 'name updated'
    assert phone == '999'


@pytest.mark.run(order=-2)
def test_delete_contacts(client, TOKEN, CONTACTS):
    ID = CONTACTS[0]['id']
    rs7 = client.delete(f'contacts/delete/{ID}',
                        headers={'JWT': TOKEN})
    info, data, error = extract(rs7)
    assert error is None
    assert rs7.status_code == 200


@pytest.mark.run(order=-1)
def test_postdelete(client, TOKEN, CONTACTS):
    ID = CONTACTS[0]['id']
    rs8 = client.get('/contacts/all',
                     headers={'JWT': TOKEN})
    info, data, error = extract(rs8)
    assert data is None
    assert error == 'No contacts was found!'
    assert rs8.status_code == 404
