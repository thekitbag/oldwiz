import random

class GameInstance():
	def __init__(self, gameId):
		self.gameId= gameId
		self.deck = []
		self.suits = ["a","b","c","d"]		
		self.pile = []
		self.hands= {}
		self.players =[]
		self.scoreboard = {

			}

	def buildDeck(self):
		for i in range(1,14):
			for j in self.suits:
				card = str(i)+j
				self.deck.append(card)
		for i in range(4):
			self.deck.append("0J")
			self.deck.append("0W")
	

	def setPlaces(self, players):
		for i in players:		
			self.hands[i]=[]

	def setScoreboard(self):
		for i in self.players:		
			self.scoreboard[i]=0

	def dealCards(self, roundNumber):
		for i in range(roundNumber):
			for j in self.hands:
				nextCard = self.deck.pop(random.randint(0,len(self.deck)-1))
				self.hands[j].append(nextCard)

	def clearHands(self):
		for i in range(len(self.hands[self.players[0]])):
			for j in self.hands:
				cards = self.hands[j].pop()
				self.deck.append(cards)
		


