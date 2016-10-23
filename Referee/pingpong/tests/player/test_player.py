from pingpong.blueprints.player.models import Player, State
from pingpong.blueprints.player.service import is_everyone_here
from pingpong.blueprints.player.service import draw_next_round

def test_find_by_username(client):
	assert Player.find_by_username('Joey').get_id() == 1
	assert Player.find_by_username('oey') == None

def test_find_by_uid(client):
	assert Player.find_by_uid(1).username == 'Joey'
	assert Player.find_by_uid(100) == None

def test_authenticated(client):
	assert Player.find_by_username('Joey').authenticated('Joey') == True
	assert Player.find_by_username('Joey').authenticated('oey') == False

def test_state_lost(client):
	Player.find_by_username('Joey').set_state_lost()
	assert Player.find_by_username('Joey').state == State.lost

def test_has_lost(client):
	Player.find_by_username('Joey').set_state_lost()
	assert Player.find_by_username('Joey').has_lost() == True

def test_is_everyone_here(client):
	joey = Player.find_by_username('Joey')
	nick = Player.find_by_username('Nick')

	assert is_everyone_here() == False
	joey.state = State.waiting
	assert is_everyone_here() == False
	nick.state = State.waiting
	assert is_everyone_here() == True

def test_draw_next_round(client):
	assert draw_next_round(1) == 1
	assert draw_next_round(2) == 0
	joey = Player.find_by_username('Joey')
	joey.state = State.lost
	assert draw_next_round(1) == 0