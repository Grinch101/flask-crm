from flask import Flask
from src.apps.user.views import user
from src.apps.activity.views import activity
from src.apps.contacts.views import contact


def creat_app(config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config)

    app.register_blueprint(user)
    app.register_blueprint(activity)
    app.register_blueprint(contact)

    return app
