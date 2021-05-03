import json


def extract(response):
    info = json.loads(response.data)['info']
    data = json.loads(response.data)['data']
    error = json.loads(response.data)['error']
    return info, data, error


def test_user_bp(client):

    # TEST USER SIGNUP
    rs1 = client.post('/auth/signup',
                      data={'inputEmail': 'SomeEmail@gmail.com',
                            'inputPassword': 'A',
                            'client_name': 'ForTest'})
    info, data, error = extract(rs1)
    assert error is None
    assert data is not None
    assert rs1.status_code == 201

    # TESTING USER LOGIN AND TOKEN GENERATION
    rs2 = client.post('/auth/login',
                      data={'inputEmail': 'SomeEmail@gmail.com',
                            'inputPassword': 'A'})
    info, TOKEN, error = extract(rs2)
    assert error is None
    assert TOKEN is not None
    assert rs2.status_code == 200

    # TESTING USER RETRIVE
    rs3 = client.get('/auth/current_user',
                     headers={'JWT': TOKEN})
    info, data, error = extract(rs3)
    assert error is None
    assert data['client_name'] == 'ForTest'
    assert data['email'] == 'SomeEmail@gmail.com'
    assert rs3.status_code == 200

    # TESTING UPDATE
    rs4 = client.put('/auth/user_update',
                     headers={'JWT': TOKEN},
                     data={'new_name': 'name_changed'})
    info, data, error = extract(rs4)
    assert error is None
    assert data['client_name'] == 'name_changed'
    assert data['email'] == 'SomeEmail@gmail.com'
    assert data["updated columns"] == ['new_name']
    assert rs4.status_code == 200
