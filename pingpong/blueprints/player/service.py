import math
import random

from pingpong.blueprints.player.models import Player, State
from pingpong.blueprints.game.models import Game


def is_everyone_here():
	"""
	Checks if all players have logged in.

	"""
	for player in Player.Db:
		if player.state == 	State.notarrived:
			return False
	return True


def draw_next_round(round_num):
	"""
		Update player states to the next round.
	"""
	max_rounds = int(math.log(len(Player.Db), 2))
	winning_players = []
	for player in Player.Db:
		if player.state != State.lost:
			player.state = State.playing
			winning_players.append(player)

	print '##############################################',max_rounds, 'round_num', round_num
	if max_rounds >= round_num:
		assert len(winning_players) > 1
		random.shuffle(winning_players)
		# select using zip players in even index with odd
		draws = zip(winning_players[::2], winning_players[1::2])
		for d in draws:
			print "Game draws", d[0].username, d[1].username
			game = Game( round_num, d[0], d[1])		
		return len(draws)
		
	# Generate report here
	return 0

