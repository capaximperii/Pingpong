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
	games = []
	for g in Game.Db:
		if g.state != State.finished:
			games.append(g)
	for g in games:
		for p in g.players:
			if p.get_id() == user.get_id():
				return g
	return None