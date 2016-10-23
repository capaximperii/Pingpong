from championship import Player
import getopt
import sys

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:],"u:",["username="])
	for opt, arg in opts:
		if opt in ("-u", "--username"):
			u = arg
			player = Player(u.strip(), u.strip())
			player.play()