import json
import random
from test.conftest import extract


def test_contact_bp(client):

    # First we need a user.
    # User registration
    rs1 = client.post('/auth/signup',
                      data={'inputEmail': 'SomeEmail@gmail.com',
                            'inputPassword': 'A',
                            'client_name': 'ForTest'})
    info, data, error = extract(rs1)
    assert error is None
    assert data is not None
    assert rs1.status_code == 201

    # TOKEN generation using login
    rs2 = client.post('/auth/login',
                      data={'inputEmail': 'SomeEmail@gmail.com',
                            'inputPassword': 'A'})
    info, TOKEN, error = extract(rs2)
    assert error is None
    assert TOKEN is not None
    assert rs2.status_code == 200

    # TESTING CONTACTS INSERT
    rs3 = client.post('contacts/add',
                        headers={'JWT':TOKEN},
                        data={'Name':f'contact name',
                            'Number':str(999)})
    info, data, error = extract(rs3)
    assert error is None
    assert data is not None
    assert rs3.status_code == 201
    
    # TESTING CONTACTS RETRIVE
    rs4 = client.get('contacts/all',
                     headers={'JWT':TOKEN})
    info, data, error = extract(rs4)
    assert error is None
    assert rs4.status_code == 200
    assert data is not None
    CONTACT_IDS = [contact['id'] for contact in data]
    assert CONTACT_IDS is not []
    
    # TESTING CONTACT UPDATE
    
