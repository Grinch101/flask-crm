from src.factory import creat_app
from utility.helpers import conn_pool
from src.config import TestingConfig
from flask import g
import pytest
import json


@pytest.fixture(autouse=True, scope='module')
def _app_runner():
    app = creat_app(TestingConfig)
    yield app


@pytest.fixture(autouse=True, scope='module')
def client(_app_runner):
    conns = conn_pool(1,10)
    conn = conns.getconn()
    with _app_runner.app_context():
        g.conn = conn
        g.secret_key = _app_runner.config['SECRET_KEY']
        with _app_runner.test_client() as client:
            yield client
            conn.rollback()
            conns.putconn(conn)


def extract(response):
    info = json.loads(response.data)['info']
    data = json.loads(response.data)['data']
    error = json.loads(response.data)['error']
    return info, data, error
