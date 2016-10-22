from flask import Blueprint, request, jsonify
from flask_login import (
	login_required,
	login_user,
	current_user,
	logout_user )

from pingpong.blueprints.player.decorators import anonymous_required
from pingpong.blueprints.player.models import Player


player = Blueprint('player', __name__)

# TODO: validate form
@player.route('/api/authentication', methods=['POST'])
@anonymous_required()
def login_do():
	resp = jsonify(error="Unauthorized",message="Authentication failed")
	status = 401
	username = request.form.get('username')
	password = request.form.get('password')
	u = Player.find_by_username(username=username)

	if u and u.authenticated(password=password):
		if login_user(u):
			resp = jsonify(message="Player logged in")
			status = 200
	resp.status_code = status
	return resp

@player.route('/api/logout')
@login_required
def logout_do():
	logout_user()
	return 'OK'

@player.route('/api/keepalive', methods=['PUT'])
@login_required
def keepalive_do():
	print "#######################"
	return 'OK'
	#if current_user.username:
	#	return 'OK'