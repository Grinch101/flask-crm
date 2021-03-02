from flask import Flask
from src.views.user import user
from src.views.activity import activity
from src.views.contact import contact


def creat_app(config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    app.register_blueprint(user, url_prefix='/auth/')
    app.register_blueprint(contact, url_prefix='/contact/')
    app.register_blueprint(activity, url_prefix='/activity/')

    return app
