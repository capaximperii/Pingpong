# -*- coding: utf-8 -*-
""" Game service handler

This module provides the common business logic used by game and game view.
 
"""
import os
from pingpong.blueprints.game.models import Game, State
import datetime

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

def dump_game_data():
	"""
	Returns the current game db for this tournament
	
	:return: games or empty list
	:type game: list
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
	return data

def build_report():
	"""
	Write report to a file.
	
	:return:
	"""
	timenow = datetime.datetime.now().strftime("%Y-%m-%d@%H:%M")
	filename = os.path.join('reports', timenow + ".txt")

	with open(filename, 'w') as f:
		games = dump_game_data()
		f.write("Tournament ended " + timenow + '\n\n')
		round_num = 1
		for game in games:
			if game['round'] > round_num:
				f.write("\n\n")
				round_num = game['round']
			f.write( 'Game-id: ' + str(game['gid']) )
			f.write( '  Round: ' + str(game['round']) )
			f.write( '  Players: ' + str(game['p0']) + ' vs ' + str(game['p1']) )
			f.write( '  Scores: ' + str(game['s0']) + ' ' + str(game['s1']) )
			f.write( '  Winner: ' + game['winner'])
			f.write("\n")
	