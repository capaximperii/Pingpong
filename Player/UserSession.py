import sys
import requests
import json
import time
import random

URL = "http://localhost:8000"

class UserSession:
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
