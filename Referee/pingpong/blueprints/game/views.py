import json
from flask import Blueprint, request, jsonify
from flask_login import (
	login_required,
	current_user )

from pingpong.blueprints.game.models import Game
from pingpong.blueprints.game.service import get_game_for_user

game = Blueprint('game', __name__)

@game.route('/api/attack/<gid>', methods=['PUT'])
@login_required
def attack_do(gid):
	num = request.form.get('number_picked')
	game = Game.find_by_gid(gid)
	if game.can_attack(current_user):
		game.set_offense_move(int(num))
		game.set_state_defensive()
		resp = (jsonify(message='Wait for defender', cmd='keepalive'), 200)
	else:
		resp = (jsonify(message='Invalid game or not your turn'), 400)
	return resp

@game.route('/api/defend/<gid>', methods=['PUT'])
@login_required
def defend_do(gid):
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
			game.set_state_offensive()
			resp = (jsonify(message='Wait for offense', cmd='keepalive'), 200)
	else:		
		resp = (jsonify(message='Invalid game or not your turn'), 400)
	return resp

	
@game.route('/api/checkgame', methods=['GET'])
@login_required
def checkgame_do():
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


