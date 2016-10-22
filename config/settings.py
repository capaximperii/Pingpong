from datetime import timedelta

DEBUG = True

SERVER_NAME = 'localhost:8000'
SECRET_KEY = 'badpassword'


#	The players allowed along with, with ids as keys.

PLAYERS = 	{
				1: 'Joey', 2: 'Nick', 3: 'Russel', 
				4: 'Vivek', 5: 'Pritam', 6: 'Amit',
				7: 'Chandler', 8: 'Colwin' 
			}


#	These ids match the index within the defense array for each player
# 	The number is 0th place is a place holder to match 
DEFENSE = 	[ 0, 8, 8, 7, 7, 6, 6, 5, 5  ]

REMEMBER_COOKIE_DURATION = timedelta(days=90)