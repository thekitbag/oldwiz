import random
import collections

class Card():
	suits = ["none","A","B","C","D"]
	ranks = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13"]

	def __init__(self,suit_index,rank):
		self.suit_index = suit_index
		self.rank = rank
		self.suit = Card.suits[suit_index]

	def __repr__(self):
		return '%s%s' %(Card.ranks[self.rank],Card.suits[self.suit_index])



class Deck():
	def __init__(self):
		self.cards = []
		for suit in range(1,5):
			for rank in range (1,14):
				card = Card(suit,rank)
				self.cards.append(card)
		random.shuffle(self.cards)

	def __str__(self):
		res = []
		for card in self.cards:
			res.append(str(card))
		return '\n'.join(res)
	
	def randomCard(self):
		#deals a card to each player based on what round it is		
		self.card = self.cards.pop()
		return self.card

class Player():
	member_id_count = 0
	def __init__(self):
		self.member_id = self.member_id_count + 1
		Player.member_id_count += 1
		self.username = ""
		self.auth_token = ""
		self.hand = []	

	def register(self, game):
		self.game = game		
		game.scoreboard[self.username] = 0
		current_player_count = len(game.entrants)
		game.seats[current_player_count] = self
		game.entrants.append(self)
	

	def playCard(self, card):		
		if Dealer.is_valid_move(card, self.game.pile, self.hand) ==  "first card":
			self.game.pile['valid_suit'] = card.suit
			self.game.pile[self] = card
			self.hand.remove(card)
		elif Dealer.is_valid_move(card, self.game.pile, self.hand) ==  True and card in self.hand:						
			self.game.pile[self] = card
			self.hand.remove(card)
		else: raise ValueError('INVALID MOVE')

	def __repr__(self):
		return self.username

class Dealer():
	@classmethod
	def is_valid_move(cls, card, pile, hand):
		available_cards = []				
		if len(pile) == 0:
			return "first card"
		else:
			for card in hand:
				if card.suit == pile ['valid_suit']:
					available_cards.append(card)
		if card.suit == pile['valid_suit']:
			return True
		elif len(available_cards) == 0:
			return True		
		else: 
			return False

	@classmethod
	def declareWinner(cls, game):
		game.pile.clear()
		

	@classmethod
	def requestActions(cls, game):
		active_player = 0
		for player in range(game.size):
			player = game.seats[active_player]
			print "%s's Cards %s" %(player, player.hand)
			chosen_card = int(raw_input("Pick Your Card Please %s :  " %player))			
			player.playCard(player.hand[chosen_card])
			print ""
			print "pile: %s" %(game.pile)
			print ""
			active_player += 1

	@classmethod
	def printGameState(cls, game):
		print "-----------------------GAMEROUND %s-----------------------" %(game.round-1)
		print ""
		print "---PLAYERS---"
		print ""
		for player in game.entrants:
			print player.__dict__			
		print ""
		print "---GAME---"
		print ""		
		print game.__dict__
		print ""
		print "----GAME---"
		print ""
		print ""

	@classmethod
	def dealCards(cls, game):
		for i in range(game.round):
			for player in game.entrants:
				card = game.deck.randomCard()
				player.hand.append(card)
		game.round += 1

	@classmethod
	def start_game(cls, game):
		for i in range(game.length):
		#single method that runs the whole game			
			Dealer.dealCards(game)
			Dealer.printGameState(game)
			for i in range(game.round-1):
				Dealer.requestActions(game)
				Dealer.printGameState(game)
				Dealer.declareWinner(game)

class Game():
	deck = Deck()
	def __init__(self, game_id, size, length):
		self.game_id= game_id
		self.status = ""
		self.size = size
		self.length = length
		self.entrants = []
		self.scoreboard = {}
		self.pile = collections.OrderedDict()
		self.seats = {}
		self.round = 1

	def __repr__(self):
		#human readable representation of game object		
		return "Game ID:" + str(self.game_id)
	

class Floorman():
	active_games = 0
	id_count = 0
	games = []

	@classmethod
	def addGame(cls, size, length):
		game = Game(Floorman.id_count+1, size, length)
		Floorman.games.append(game)




Floorman.addGame(4,3)
Floorman.addGame(5,3)	

mark = Player()
mark.username = "Mark"
mark.auth_token = "abc"

shannon = Player()
shannon.username = "Shannon"
shannon.auth_token = "def"

mike = Player()
mike.username = "Mike"
mike.auth_token = "ghi"

de = Player()
de.username = "Deanne"
de.auth_token = "jkl"

test_game = Floorman.games[0]
test_game.status = "running"
mark.register(test_game)
shannon.register(test_game)
de.register(test_game)
mike.register(test_game)


Dealer.start_game(test_game)



"""
test_game.dealCards(5)
print " "
print " "
print "Mark:" + str(mark.__dict__)
print "Shannon:" + str(shannon.__dict__)
print "Game:" + str(test_game.__dict__)


Dealer.requestAction(mark) 

print " "
print "Mark:" + str(mark.__dict__)
print "Shannon:" + str(shannon.__dict__)
print "Game:" + str(test_game.__dict__)




	
print " "
print "MARK PLAYS FOURTH CARD IN HAND"
print " "
print "Mark:" + str(mark.__dict__)
print "Shannon:" + str(shannon.__dict__)
print "Game:" + str(test_game.__dict__)
choice2 = int(raw_input("pick a card by index  "))
shannon.playCard(shannon.hand[choice2])
print " "
print "SHANNON PLAYS FIRST CARD IN HAND"
print " "
print "Mark:" + str(mark.__dict__)
print "Shannon:" + str(shannon.__dict__)
print "Game:" + str(test_game.__dict__)

Dealer.declareWinner(test_game.pile)
"""





#need card objects to remain card objects, not become strings