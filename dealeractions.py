import random
deck = []
suits = ["a", "b", "c", "d"]

gameId = 0
hands= {}
numberOfEntrants=3
Scoreboard = {
	"playerOne": 0,
	"playerTwo": 0,
	"playerThree": 0,
	"playerFour": 0,
	"playerFive": 0,
	"playerSix": 0,
}

def buildDeck():
	for i in range(1,14):
		for j in suits:
			card = str(i)+j
			deck.append(card)
	for i in range(4):
		deck.append("0J")
		deck.append("0w")



def setPlaces(players):
	for i in range(players):		
		hands['player_hand_{}'.format(i)]=[]

def dealCards(roundNumber):
	for i in range(roundNumber):
		for j in hands:
			nextCard = deck.pop(random.randint(0,len(deck)-1))
			hands[j].append(random.choice(deck))
	print hands

def clearHands():
	for i in hands:
		hands[i] = []


def playGame(entrants):
	currentRound = 1
	buildDeck()
	setPlaces(entrants)
	print "cards in deck" + str(len(deck))
	dealCards(currentRound)
	print "cards in deck" + str(len(deck))
	#need to add those cards back in to the deck somehow
	clearHands()
	currentRound += 1
	dealCards(currentRound)
	clearHands()
	currentRound += 1
	dealCards(currentRound)
	

playGame(numberOfEntrants)




