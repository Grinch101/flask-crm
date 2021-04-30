from app import app
from app.src.config import TestingConfig
import pytest
from flask import g, Response


@pytest.fixture
def app_runner():
    global app
    global TestingConfigpp
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
        app.process_response(Response('This is an empty response!')) 
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

