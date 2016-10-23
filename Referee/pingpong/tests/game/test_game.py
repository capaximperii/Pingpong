from pingpong.blueprints.game.models import Game, State
from pingpong.blueprints.player.models import Player
from pingpong.blueprints.player.service import draw_next_round
import pytest

@pytest.mark.order1
def test_find_by_gid(client):
	assert Game.find_by_gid(1) == None
	joey = Player.find_by_username('Joey')
	nick = Player.find_by_username('Nick')
	g = Game(1, nick, joey)
	game_from_db =Game.find_by_gid(g.get_id()) 	
	assert g != None
	assert g.get_id() == game_from_db.get_id()
	# we set it to hard value for tests
	g.gid = 100

@pytest.mark.order2
def test_user_can_play(client):
	joey = Player.find_by_username('Joey')
	nick = Player.find_by_username('Nick')
	g = Game.find_by_gid(100)
	assert g.user_can_play(nick) == True
	assert g.user_can_play(joey) == True

@pytest.mark.order3
def test_user_can_defend_attack(client):
	joey = Player.find_by_username('Joey')
	nick = Player.find_by_username('Nick')
	g = Game.find_by_gid(100)
	assert g.can_attack(joey) == False
	assert g.can_defend(nick) == False

	# Joey can't defend unless nick plays offense move
	assert g.can_defend(joey) == False
	assert g.can_attack(nick) == True

	# nick attacks with 1
	g.set_offense_move(1)
	assert g.can_defend(joey) == True
	assert g.can_attack(nick) == False

	# joey defends with 1 2 3 4, 
	# joey loses point
	g.set_defense_move([1, 2, 3, 4])
	assert g.can_defend(joey) == False
	assert g.can_attack(nick) == True
	assert g.can_attack(joey) == False

	# nick attacks with 1
	g.set_offense_move(1)
	assert g.can_defend(joey) == True
	assert g.can_defend(nick) == False

	# joey defends with 0, 2, 3 ,4, joey now wins
	g.set_defense_move([0, 2, 3, 4])
	# nick cant attack
	assert g.can_defend(joey) == False
	assert g.can_attack(nick) == False
	assert g.can_attack(joey) == True

	# nick attacks with 1
	g.set_offense_move(1)
	g.set_defense_move([1, 2, 3, 4])
	# nick gets winning point
	assert g.can_defend(nick) == False
	assert g.can_attack(joey) == True

@pytest.mark.order4
def test_get_round_winner(client):
	joey = Player.find_by_username('Joey')
	nick = Player.find_by_username('Nick')
	g = Game.find_by_gid(100)
	assert g.get_round_winner().get_id() == joey.get_id()

@pytest.mark.order5
def test_get_tournament_winner(client):
	joey = Player.find_by_username('Joey')
	nick = Player.find_by_username('Nick')
	g = Game.find_by_gid(100)
	assert Game.get_tournament_winner() != None	