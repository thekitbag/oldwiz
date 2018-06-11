deck = []
suits = ["a", "b", "c", "d"]

gameId = 0
hands= {
"playerOneHand": [],
"playerTwoHand": [],
"playerThreeHand": [],
"playerFourHand": [],
"playerFiveHand": [],
"playerSixHand": [],
}
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

print hands."playerOneHand"


def dealCards(gameRound,players):
	for i in range(gameRound):
		for j in range(players):
			hands[j].value = deck[0]



def playGame(players):
	buildDeck()
	dealCards(1,players)

playGame(4)


