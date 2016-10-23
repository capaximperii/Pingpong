# -*- coding: utf-8 -*-
""" Game views handler

This module provides the API endpoints for the game module API endpoints
to be accessed by the Players as well as dashboard status data.

TODO:
	Check when a tournament is actually completed? 
"""

import json
from flask import Blueprint, request, jsonify
from flask_login import (
	login_required,
	current_user )

from pingpong.blueprints.game.models import Game, State
from pingpong.blueprints.game.service import get_game_for_user

game = Blueprint('game', __name__)

@game.route('/api/attack/<gid>', methods=['PUT'])
@login_required
def attack_do(gid):
	"""
	API for registering an attack move
	
	:param gid: game id
	:type gid: int
	:return: 200 on success
	"""
	num = request.form.get('number_picked')
	game = Game.find_by_gid(gid)
	if game.can_attack(current_user):
		game.set_offense_move(int(num))
		resp = (jsonify(message='Wait for defender', cmd='keepalive'), 200)
	else:
		resp = (jsonify(message='Invalid game or not your turn'), 400)
	return resp

@game.route('/api/defend/<gid>', methods=['PUT'])
@login_required
def defend_do(gid):
	"""
	API for registering a defense move
	
	:param gid: game id
	:type gid: int
	:return: 200 on success
	"""
	data = json.loads(str(request.form.get('number_picked')))
	game = Game.find_by_gid(gid)
	if game.can_defend(current_user):
		game.set_defense_move(data)
		winner = game.get_round_winner()
		if winner != None:
			game.set_state_finished()
			if winner.get_id() != current_user.get_id():
				resp = (jsonify(message='You have lost', cmd='logout'), 200)
			else:
				resp = (jsonify(message='You won this round', cmd='keepalive'), 200)
		else:
			resp = (jsonify(message='Wait for offense', cmd='keepalive'), 200)
	else:		
		resp = (jsonify(message='Invalid game or not your turn'), 400)
	return resp

	
@game.route('/api/checkgame', methods=['GET'])
@login_required
def checkgame_do():
	"""
	API for players to get their next move instruction
	
	:return: 200 on success
	"""
	game = get_game_for_user(current_user)

	if current_user.has_lost():
		resp = jsonify(message="You lost", cmd="logout"), 200
	elif not game:
		resp = jsonify(message="You won this round", cmd="keepalive"), 200
	else:
		if not game.user_can_play(current_user):
			resp = (jsonify(message='Invalid game', cmd='keepalive'), 400)			
		elif game.can_defend(current_user):
			resp = jsonify(message="Defend", cmd="defend", gid=game.get_id()), 200
		elif game.can_attack(current_user):
			resp = jsonify(message="Attack", cmd="attack", gid=game.get_id()), 200
		else:
			resp = (jsonify(message='Wait for turn', cmd='keepalive'), 200)
	return resp


@game.route('/api/gamestatus', methods=['GET'])
def gamestatus_do():
	"""
	API for getting game stats for dashboard

	:return: 200 on success
	"""
	games = Game.Db
	data = []
	for g in games:
		p0 = g.players[0].username
		p1 = g.players[1].username

		s0 = g.scores[0]
		s1 = g.scores[1]

		gdata = {'gid': g.gid, 'state': g.state == State.finished, 'round': g.round,
			'p0': p0, 'p1': p1, 's0': s0, 's1': s1}
		if g.winner != None:
			gdata['winner'] = g.winner.username
		data.append(gdata) 
	resp = jsonify(data=data)
	return resp, 200


