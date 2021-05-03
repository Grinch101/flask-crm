import pytest
import json

def test_login(client):
    rs1 = client.post('/auth/signup',
                    data={'inputEmail': 'SomeEmail@gmail.com',
                        'inputPassword': 'A',
                        'client_name': 'ForTest'})
    data = json.loads(rs1.data)['data']
    error = json.loads(rs1.data)['error']
    assert error is None
    assert data is not None
    assert rs1.status_code == 201

    rs2 = client.post('/auth/login',
                    data={'inputEmail': 'SomeEmail@gmail.com',
                        'inputPassword': 'A'})
    data = json.loads(rs2.data)['data']
    error = json.loads(rs2.data)['error']
    assert error is None
    assert data is not None
    assert rs2.status_code == 200
