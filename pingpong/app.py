from flask import Flask
from pingpong.blueprints.page import page
from pingpong.blueprints.player import player
from pingpong.blueprints.game import game
from pingpong.blueprints.player.models import Player
from itsdangerous import URLSafeTimedSerializer
from pingpong.extensions import login_manager
import math

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)
    app.register_blueprint(player)
    app.register_blueprint(game)

    extensions(app)
    authentication(app, Player)

    return app

def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    # Initialize the players db from settings list
    players = app.config['PLAYERS']
    # The number of players have to be a power of 2.
    assert math.log(len(players), 2).is_integer()

    for uid, username in players.iteritems():
        defense = app.config['DEFENSE'][uid]
        p = Player(username=username, password=username, uid=uid, defense=10 )

    login_manager.init_app(app)

    return None


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: DB model, which in our case is in application memory
    :return: None
    """
    # login_manager.login_view = '/'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.find_by_uid(uid)

    @login_manager.token_loader
    def load_token(token):
        print "##################################"
        duration = app.config['REMEMBER_COOKIE_DURATION'].total_seconds()
        serializer = URLSafeTimedSerializer(app.secret_key)

        data = serializer.loads(token, max_age=duration)
        user_uid = data[0]

        return user_model.find_by_uid(user_uid)