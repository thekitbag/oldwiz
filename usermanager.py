from random import randint

def createToken():
	characters = ["b", "c", "d", "f", "g", "h", "j","k","l","m",0,1,3,4,5,8]
	picks = []
	token = ""
	for i in range(20):
		picks.append(str(characters[randint(0,len(characters)-1)]))
	token = "".join(picks)
	return token
