# -*- coding: utf-8 -*-
""" PlayPingPing script

This module provides the player script to play pingpong with Referee webapp.
 
"""

from championship import Player
from ConfigParser import ConfigParser
import getopt
import sys
import os

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:],"u:",["username="])
	for opt, arg in opts:

		if opt in ("-u", "--username"):
			u = arg.strip().lower()
			cfg = ConfigParser()
			cfg.read(os.path.join("config", "players.ini"))
			# Check if the player has a configuration
			if u in cfg.sections():
				username = cfg.get(u, 'username')
				password = cfg.get(u, 'password')
				defense = cfg.get(u, 'defense')
				url = cfg.get(u, 'url')
				player = Player(username, password, defense, url)
				player.play()
			else:
				print u, 'not in ', cfg.sections()
