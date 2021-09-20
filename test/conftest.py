from src.factory import creat_app
from utility.helpers import conn_pool
from src.config import TestingConfig
from flask import g
import pytest
import json


@pytest.fixture(scope='session')
def _app_runner():
    app = creat_app(TestingConfig)
    return app


@pytest.fixture(scope='session')
def client(_app_runner):
    conns = conn_pool(1, 10)
    conn = conns.getconn()
    with _app_runner.app_context():
        g.conn = conn
        g.secret_key = _app_runner.config['SECRET_KEY']
        with _app_runner.test_client() as client:
            yield client
            conn = g.conn
            g.conn = None
            conn.rollback()
            conns.putconn(conn)


@pytest.fixture(scope='session')
def TOKEN(client):
    rs1 = client.post('/auth/signup',
                      data={'inputEmail': 'SomeEmail@gmail.com',
                            'inputPassword': 'A',
                            'client_name': 'ForTest'})
    rs2 = client.post('/auth/login',
                      data={'inputEmail': 'SomeEmail@gmail.com',
                            'inputPassword': 'A'})
    info, TOKEN, error = extract(rs2)
    return TOKEN


def extract(response):
    info = json.loads(response.data)['info']
    data = json.loads(response.data)['data']
    error = json.loads(response.data)['error']
    return info, data, error
