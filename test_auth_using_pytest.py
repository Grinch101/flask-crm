from app import app, connections
from src.config import TestingConfig
import pytest
import json
from flask import g, current_app, Response



@pytest.fixture
def app_runner():
    global app
    global TestingConfig
    app.config.from_object(TestingConfig)
    return app


@pytest.fixture
def app_with_g_ctx(app_runner):
    with app.app_context():
        yield app


@pytest.fixture
def client(app_runner):
    with app.test_client() as client:
        yield client

##########################
def test_g_contents(app_with_g_ctx):
    with app.test_request_context():
        app.preprocess_request()
        assert g.conn is not None
        app.process_response(Response()) 
        # An empty response was passed to make the process_response work!
        assert g.conn is None


def test_signup(client):
    rs = client.post('/auth/signup',
                     data={'inputEmail':'SomeEmail@gmail.com',
                           'inputPassword':'A',
                           'client_name':'NedaForTest'}
                           )
    data = json.loads(rs.data)['data']
    assert rs.status_code == 201

