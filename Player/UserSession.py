import sys
import requests
import json
import time

URL = "http://localhost:8000"

class UserSession:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.session = requests.session()
		self.payload = self.session.get(URL)
		self.objectiveId = None
		self.quizId = None
		self.level = None

	def authenticate(self):
		self.payload = self.session.post(URL + "/api/authentication",
							data={	"username": 	self.username ,
									"password":	self.password}
							)
		if self.payload.status_code != 200:
			print "Failed to authenticate"
			return False
		print self.payload
		return True

	def keepalive(self):
		data = {}
		self.payload = self.session.put(URL + "/api/keepalive",
			data = json.dumps(data),
			headers={"Content-Type": "application/json;charset=UTF-8"})
		if self.payload.status_code != 200:
			return False
		return True

	def getObjectiveId(self):
		objectiveId = None
		self.payload = self.session.get("http://localhost:8082/api/objectives")
		dashboard = self.payload.json()
		for objective in dashboard:
			if objective['name'] == 'African capitals':
				objectiveId =  objective['id']
				break
		self.objectiveId = objectiveId
		return objectiveId

	def getFirstObjectiveLevelForQuiz(self, objectiveId):
		firstLevel = None
		self.payload = self.session.get(URL + "/api/objectives/" + str(objectiveId))
		levels = self.payload.json()['objectiveLevels']
		firstLevel = 0
		for l in levels:
			firstLevel = l['id']
			break
		self.level = firstLevel
		return firstLevel

	def startQuiz(self, objectiveId, level):
		data = {"objective":{"id": str(objectiveId)},"objectiveLevel":{"id":str(level)}}
		self.payload = self.session.post( URL + "/api/quizs",
			data = json.dumps(data),
			headers={"Referer": URL, "Content-Type": "application/json;charset=UTF-8"})
		quiz = self.payload.json()
		quizId = quiz['id'];
		self.quizId = quizId
		return quizId

	def simulateQuizResponse(self, quizId):
		counter = 0
		while True:
			self.payload = self.session.get(URL + "/api/quizs/" + str(quizId))
			if self.payload.status_code != 200:
				print "ERROR: Quiz: ", str(quizId), "RETURNED: ",self.payload.status_code,"DETAIL: ", self.payload.text
				break
			quizSteps = self.payload.json()['quizSteps']
			step = quizSteps[0]
			objectiveQuestion = step['objectiveQuestion']
			startTime = step['startTime']
			quizType = step['type']
			rank = step['rank']
			quizForm = step['quizForm']
			data = { "quizForm": None,"id": step['id'],
					 "type": quizType, "rank": rank,
					 "startTime": startTime,
					 "endTime": startTime,
					 "objectiveQuestion": objectiveQuestion }

			if step['type'] == "PRESENTATION":
				pass # This is a presentation step
			elif step['type'] == "TESTING":
				answerInput = quizForm['answerInput']
				choices = answerInput['choices']
				answerInput["selectedChoice"] = choices[0]
				answerInput["@type"] = "com.henoida.business.object.quiz.testing.answer.MultipleChoicesInput"
				answerInput["testMethod"] = "MULTIPLE_CHOICE"
				answerdata = { 
						 	"answerInput":  answerInput,
						 	"submitted": True,
						 }
				self.payload = self.session.put(URL + '/api/quizForms',
					data = json.dumps(answerdata),
					headers={"Referer": URL, "Content-Type": "application/json;charset=UTF-8"})
					#print self.payload.text
			elif step['type'] == "CONGRATULATIONS":
				print "SUCCESS: ",step['type'],"for user", self.username
				break
			else:
				print "ERROR: Quiz: ", str(quizId), "RETURNED: ",self.payload.status_code,"DETAIL: ", self.payload.text
				break
			self.payload = self.session.put(URL + '/api/quizSteps',
				data = json.dumps(data),
				headers={"Referer": URL, "Content-Type": "application/json;charset=UTF-8"})
			if self.payload.status_code == 404:
				print "ERROR: Quiz: ", str(quizId), "RETURNED: ",self.payload.status_code,"DETAIL: ", self.payload.text
			elif self.payload.status_code != 201:
				print "ERROR: Quiz: ", str(quizId), "RETURNED: ",self.payload.status_code,"DETAIL: ", self.payload.text
			 	break
			time.sleep(1)
	
