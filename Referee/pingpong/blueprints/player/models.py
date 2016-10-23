from enum import Enum
from flask_login import UserMixin

class State (Enum):
	 __order__ = 'notarrived waiting playing won lost'
	 notarrived = 1
	 waiting = 2
	 playing = 3
	 won = 4
	 lost = 5


class Player(UserMixin):
	"""
		Store all registered players in a  static list.
		This simulates sqlalchemy behavior if we needed a DB.
	"""
	Db = []
	
	def __init__(self, uid, username, password, **kwargs):
		# Call  constructor.
		super(Player, self).__init__(**kwargs)
		self.uid = uid
		self.username = username
		self.password = password
		self.state = State.notarrived
		self.current_game = None
		Player.Db.append(self)

	@classmethod
	def find_by_username(cls, username):
		"""
		Find a player by username.

		:param identity: username
		:type identity: str
		:return: Player instance
		"""
		for player in Player.Db:
			if player.username == username:
				return player
		return None

	@classmethod
	def find_by_uid(cls, uid):
		"""
		Find a player by uid.

		:param identity: uid
		:type identity: int
		:return: Player instance
		"""
		for player in Player.Db:
			if player.uid == int(uid):
				return player
		return None


	def is_active(self):
		"""
		Return whether or not the user account is active, this satisfies
		Flask-Login by overwriting the default value.

		:return: bool
		"""
		return True

	def authenticated(self, password):
		"""
		Authenticate by checking their password.

		:param password:  password for the user
		:type password: str
		:return: bool
		"""
		return self.password == password

	def get_id(self):
		"""
		Overrides flask_login get_id method

		:return: int
		"""
		return self.uid

	def set_state_lost(self):
		"""
		Disable a player once he loses

		"""
		self.state = State.lost

	def set_waiting_state(self):
		"""
		Set a player to waiting

		"""
		self.state = State.waiting


	def has_lost(self):
		"""
		Has a player lost

		"""
		return self.state == State.lost