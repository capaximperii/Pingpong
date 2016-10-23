import sys
import requests
import json
import time
import random


class Player:
		
	def __init__(self, username, password, defense, url):
		self.username = username
		self.password = password
		self.defense = int(defense)
		self.session = requests.session()
		self.url = url
		self.payload = self.session.get(url)

	def authenticate(self):
		self.payload = self.session.post(self.url + "/api/authentication",
							data={	"username": 	self.username ,
									"password":	self.password}
							)
		if self.payload.status_code != 200:
			print "Failed to authenticate"
			raise Exception("Wrong credentials, failed to authenticate")

		print "Authenticated to the server."
		return self.payload.json()

	def keepalive(self):
		self.payload = self.session.get(self.url + "/api/keepalive")
		if self.payload.status_code != 200:
			return None
		return self.payload.json()

	def checkgame(self):
		self.payload = self.session.get(self.url + "/api/checkgame")
		if self.payload.status_code != 200:
			return False
		return self.payload.json()

	def attack(self, gid):
		number_picked = random.randrange(1, 11)
		self.payload = self.session.put(self.url + "/api/attack/" + str(gid),
					data={	"number_picked": 	number_picked })
		return self.payload.json()

	def defend (self, gid):
		number_picked = []
		for i in range(0, self.defense):
			# Game rules mention nothing about duplicate numbers in defense.
			number_picked.append(random.randrange(1, 11))

		self.payload = self.session.put(self.url + "/api/defend/" + str(gid),
					data={	"number_picked": 	json.dumps(number_picked) })
		return self.payload.json()

	def logout(self):
		self.payload = self.session.get(self.url + "/api/logout")
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
				gid = response['gid']
				response = self.defend(gid)
			elif command == 'logout':
				response = self.logout()
				break
			else:
				break
			time.sleep(1)
