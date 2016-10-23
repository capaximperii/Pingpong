# -*- coding: utf-8 -*-
""" Game Model

This module provides the Game model as used in the application.
 
"""

from enum import Enum
from flask import current_app

class State (Enum):
	 __order__ = 'defensive offensive finished'
	 defensive = 1
	 offensive = 2
	 finished = 3

class Game():
	"""
		Store all registered players in a  static list.
		This simulates sqlalchemy behavior if we needed a DB.
	"""
	Db = []
	
	def __init__(self, current_round, player1, player2):
		# Call  constructor.
		self.state = State.offensive
		self.gid = id(self)
		self.players = []
		self.roles = [State.offensive, State.defensive]
		self.scores = [0, 0]
		self.players.append(player1)
		self.players.append(player2)
		self.round = current_round
		self.offensive_move = None
		self.defensive_move = None
		self.winner = None
		self.loser = None
		Game.Db.append(self)

	@classmethod
	def find_by_gid(cls, gid):
		"""
		Find a game by gid.

		:param identity: uid
		:type identity: int
		:return: Game instance
		"""
		for game in Game.Db:
			if game.gid == int(gid):
				return game
		return None

	def user_can_play(self, player):
		"""
		Checks if user allowed to play.

		:param player: object
		:type identity: Player
		:return: bool
		"""
		return player in self.players and self.state != State.finished

	def can_attack(self, player):
		"""
		Checks if user allowed to attack.

		:param player: object
		:type identity: Player
		:return: bool
		"""

		index = 0
		for p in self.players:
			if player.uid == p.uid:
				if self.roles[index] == State.offensive: 
					return self.state == State.offensive
			index += 1
		return False

	def can_defend(self, player):
		"""
		Checks if user allowed to defend.

		:param player: object
		:type identity: Player
		:return: bool
		"""
		index = 0
		for p in self.players:
			if player.uid == p.uid:
				if self.roles[index] == State.defensive:
					return self.state == State.defensive
			index += 1
		return False

	def get_round_winner(self):
		"""
		Gets winner of the current round at max score reached.

		:return: player or None
		:type player: Player
		"""
		max_score = current_app.config['MAX_SCORE']
		if max_score in self.scores:
			index = self.scores.index(max_score)
			self.winner = self.players[index]
			self.loser = self.players[0]
			if index == 0:
				self.loser = self.players[1]
			self.loser.set_state_lost()
			return self.winner
		return None

	@classmethod
	def get_tournament_winner(cls):
		"""
		Gets the final winner
			to be called after tournament is finished

		:return: player
		:type:	Player
		"""
		finalgame = Game.Db[-1]
		return finalgame.winner

	def set_state_finished(self):
		"""
		Sets state of current game to finished

		:return: void
		"""
		self.state = State.finished

	def set_state_defensive(self):
		"""
		Sets state of current game to defensive

		:return: void
		"""
		self.state = State.defensive

	def set_state_offensive(self):
		"""
		Sets state of current game to offensive

		:return: void
		"""
		self.state = State.offensive

	def set_offense_move(self, move):
		"""
		Sets offense move of current game
		
		:param move: object
		:type move: int
		:return: void
		"""
		self.offensive_move = move
		self.set_state_defensive()

	def set_defense_move(self, move):
		"""
		Sets defense move of current game
		
		:param move: object
		:type move: list of int
		:return: void
		"""
		self.defensive_move = move
		offensive_player_index = self.roles.index(State.offensive)
		defensive_player_index = self.roles.index(State.defensive)
		if self.offensive_move in self.defensive_move:
			self.scores[offensive_player_index] += 1
		else:
			self.scores[defensive_player_index] += 1
			self.roles[defensive_player_index] = State.offensive
			self.roles[offensive_player_index] = State.defensive
		self.set_state_offensive

	def get_id(self):
		"""
		Overrides flask_login get_id method

		:return: int
		"""
		return self.gid
