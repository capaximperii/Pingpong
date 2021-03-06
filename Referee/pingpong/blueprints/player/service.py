# -*- coding: utf-8 -*-
""" Player service handler

This module provides the player services for the business logic to be used by
model and views.
 
"""
import math
import random

from pingpong.blueprints.player.models import Player, State
from pingpong.blueprints.game.models import Game


def is_everyone_here():
	"""
	Checks if all players have logged in.

	:return: bool
	"""
	for player in Player.Db:
		if player.state == 	State.notarrived:
			return False
	return True


def draw_next_round(round_num):
	"""
	Update player states to the next round.

	:param round_num: round number in the tournament
	:type identity: int
	:return: size of next draw	
	"""
	max_rounds = int(math.log(len(Player.Db), 2))
	winning_players = []
	for player in Player.Db:
		if player.state != State.lost:
			player.state = State.playing
			winning_players.append(player)

	if len(winning_players) and max_rounds >= round_num:
		random.shuffle(winning_players)
		# select using zip players in even index with odd
		draws = zip(winning_players[::2], winning_players[1::2])
		for d in draws:
			# print "Game draws", d[0].username, d[1].username
			game = Game( round_num, d[0], d[1])		
		return len(draws)
		
	# Generate report here
	return 0

