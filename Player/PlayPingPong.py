from UserSession import UserSession
import getopt
import sys
import time

def startPlaying(user):
		response = user.authenticate()

		while True:
			print response
			command = response['cmd']
			if command  == 'keepalive':
				response = user.keepalive()
			elif command == 'checkgame':
				response = user.checkgame()
			elif command == 'attack':
				gid = response['gid']
				response = user.attack(gid)
			elif command == 'defend':
				defense = response['defense']
				gid = response['gid']
				response = user.defend(gid, defense)
			elif command == 'logout':
				response = user.logout()
				break
			else:
				break
			time.sleep(1)

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:],"u:",["username="])
	for opt, arg in opts:
		if opt in ("-u", "--username"):
			u = arg
			user = UserSession(u.strip(), u.strip())
			startPlaying(user)
