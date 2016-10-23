# -*- coding: utf-8 -*-
""" Game service handler

This module provides the common business logic used by game and game view.
 
"""

from pingpong.blueprints.game.models import Game, State

def are_games_pending():
	"""
	Check if a game is going on

	:return bool
	"""
	for g in Game.Db:
		if g.state != State.finished:
			return True
	return False

def get_game_for_user(user):
	"""
	Returns the current running game for the user
	
	:param user: object
	:type user: Player
	:return: game or None
	:type game: Game
	"""
	games = []
	for g in Game.Db:
		if g.state != State.finished:
			games.append(g)
	for g in games:
		for p in g.players:
			if p.get_id() == user.get_id():
				return g
	return None