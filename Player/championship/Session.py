import sys
import requests
import json
import time
import random

URL = "http://localhost:8000"

class Player:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.session = requests.session()
		self.payload = self.session.get(URL)

	def authenticate(self):
		self.payload = self.session.post(URL + "/api/authentication",
							data={	"username": 	self.username ,
									"password":	self.password}
							)
		if self.payload.status_code != 200:
			print "Failed to authenticate"
			raise Exception("Wrong credentials, failed to authenticate")

		print "Authenticated to the server."
		return self.payload.json()

	def keepalive(self):
		self.payload = self.session.get(URL + "/api/keepalive")
		if self.payload.status_code != 200:
			return None
		return self.payload.json()

	def checkgame(self):
		self.payload = self.session.get(URL + "/api/checkgame")
		if self.payload.status_code != 200:
			return False
		return self.payload.json()

	def attack(self, gid):
		number_picked = random.randrange(1, 11)
		self.payload = self.session.put(URL + "/api/attack/" + str(gid),
					data={	"number_picked": 	number_picked })
		return self.payload.json()

	def defend (self, gid, n):
		number_picked = []
		for i in range(0, n):
			number_picked.append(random.randrange(1, 11))

		self.payload = self.session.put(URL + "/api/defend/" + str(gid),
					data={	"number_picked": 	json.dumps(number_picked) })
		return self.payload.json()

	def logout(self):
		self.payload = self.session.get(URL + "/api/logout")
		return self.payload.json()

	
	def play(self):
		response = self.authenticate()

		while True:
			print response
			command = response['cmd']
			if command  == 'keepalive':
				response = self.keepalive()
			elif command == 'checkgame':
				response = self.checkgame()
			elif command == 'attack':
				gid = response['gid']
				response = self.attack(gid)
			elif command == 'defend':
				defense = response['defense']
				gid = response['gid']
				response = self.defend(gid, defense)
			elif command == 'logout':
				response = self.logout()
				break
			else:
				break
			time.sleep(1)
