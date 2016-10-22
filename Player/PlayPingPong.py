from UserSession import UserSession
import getopt
import sys
import time

def startPlaying(user):
		assert user.authenticate() == True
		while True:
			assert user.keepalive() == True
			time.sleep(5)
	#while True:
		# assert user.cloneTopic() != None
		# objectiveId = user.getObjectiveId()
		# assert objectiveId != None
		# level = user.getFirstObjectiveLevelForQuiz(objectiveId)
		# assert level != None
		# quizId = user.startQuiz(objectiveId, level)
		# assert quizId != None
		# user.simulateQuizResponse(quizId)


if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:],"u:",["username="])
	print opts
	for opt, arg in opts:
		if opt in ("-u", "--username"):
			u = arg
			user = UserSession(u.strip(), u.strip())
			startPlaying(user)
