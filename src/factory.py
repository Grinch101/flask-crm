from flask import Flask
from src.apps.user.views import user
from src.apps.activity.views import activity
from src.apps.contacts.views import contact


def creat_app(config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)
    app.register_blueprint(user, url_prefix='/auth/')
    app.register_blueprint(contact, url_prefix='/contact-management')
    app.register_blueprint(activity, url_prefix='/log-activity/')

    return app
