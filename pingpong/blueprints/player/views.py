from flask import Blueprint, request
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user )

from pingpong.blueprints.player.decorators import anonymous_required
from pingpong.blueprints.player.models import Player


player = Blueprint('player', __name__)


@player.route('/api/login', methods=['POST'])
@anonymous_required()
def login():
    u = User.find_by_identity(request.form.get('identity'))
    if u and u.authenticated(password=request.form.get('password')):
    	return 'OK'
    else:
        raise Exception('Identity or password is incorrect.')

@player.route('/api/logout')
@login_required
def logout():
    logout_user()
    return 'OK'


@player.route('/api/keepalive', methods=['PUT'])
@login_required
def welcome():
    if current_user.username:
        return 'OK'