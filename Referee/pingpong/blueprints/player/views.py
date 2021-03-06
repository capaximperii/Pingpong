# -*- coding: utf-8 -*-
""" Player views handler

This module provides the API endpoints for the player module API endpoints
to be accessed by the Players to log in and to check their status between 
game play.

"""

from flask import Blueprint, request, jsonify
from flask_login import (
	login_required,
	login_user,
	current_user,
	logout_user )

from pingpong.blueprints.player.decorators import anonymous_required
from pingpong.blueprints.player.models import Player, State
from pingpong.blueprints.game.models import Game

from pingpong.blueprints.player.service import is_everyone_here
from pingpong.blueprints.player.service import draw_next_round
from pingpong.blueprints.game.service import are_games_pending
from pingpong.blueprints.game.service import build_report

player = Blueprint('player', __name__)

round_number = 1

@player.route('/api/authentication', methods=['POST'])
@anonymous_required()
def login_do():
	"""
	API for authentication
	
	:return: 200 on success
	"""

	resp = jsonify(error="Unauthorized",message="Authentication failed", cmd="authentication"), 401
	username = request.form.get('username')
	password = request.form.get('password')
	u = Player.find_by_username(username=username)

	if u and u.authenticated(password=password) == True:
		if login_user(u):
			u.set_waiting_state()
			resp = jsonify(message="Player logged in", cmd = "keepalive"), 200
	return resp

@player.route('/api/logout')
@login_required
def logout_do():
	"""
	API for logging out
	
	:return: 200 on success
	"""

	logout_user()
	return jsonify (message="Logged out", cmd='finished'), 200

@player.route('/api/keepalive', methods=['GET'])
@login_required
def keepalive_do():
	"""
	API for polling while waiting for game state to change 
	or other users to log in
	
	:return: 200 on success
	"""
	global round_number

	if not is_everyone_here() == True:
		resp = jsonify(message="Waiting for others", cmd='keepalive'), 200

	elif current_user.has_lost():
		resp = jsonify(message="You have lost", cmd="logout"), 200

	elif are_games_pending() == True:
		resp = jsonify(message="Games in progress", cmd="checkgame"), 200

	else:
	 	n = draw_next_round(round_number)
	 	if n == 0:
	 		winner = Game.get_tournament_winner()
			resp = jsonify(message="Tournament winner " + winner.username, cmd="logout"), 200
			build_report()
		else:
			round_number += 1
			resp = jsonify(message="New rounds drawn", cmd="checkgame"), 200
	
	return resp