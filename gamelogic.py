class Player():
	def __init__(self,member_id):
		self.member_id = member_id
		self.name = ""
		self.authtoken = ""
		self.active_games = []

	def joinGame(self, game_id):
		self.game_id = game_id
		floorman.games[game_id]['entrants'].append(self.name)

	def playCard(self, card, game_id):
		self.card = card
		self.game_id = game_id
		print "foo"

	def declare(self,declaration, game_id):
		self.declaration = declaration
		self.game_id = game_id
		print "bar"

class Game():
	def __init__(self,game_id):
		self.game_id= game_id
		self.status = ""
		self.size = 0
		self.scoreboard = {}
		self.pile = []
		self.hands = {}
		self.deck = []

class Dealer():
	def __init__(self):
		self.suits = ["a","b","c","d"]


	def validatePlayer(self, player, token):
		self.player = player
		self.token = token
		if 1 > 0:
			return True
		else:
			return False

	def buildDeck(self, game_id):
		self.game_id = game_id
		for i in range(1,14):
			for j in self.suits:
				card = str(i)+j
				game_id.deck.append(card)
		for i in range(4):
			game_id.deck.append("0J")
			game_id.deck.append("0W")

	def validateMove(self, game_id, card, pile):
		self.game_id = game_id
		self.card = card
		self.pile = pile
		if 1 > 0:
			return True
		else:
			return False

class Floorman():
	def __init__(self):
		self.leaderboard = {}
		self.games = {0:
			{
			'id': 0,
			'players':4,
	        'entrants':["test1","test2","test3"],	        
			'status': 'test'
	        }	    
		}	

	def createGame(self, size):
		self.size = size		
		self.games[max(self.games)+1] = {
		'id': max(self.games)+1,
		'players': size,
		'entrants': [],
		'status': 'open'
		}

	def cancelGame(self, game_id):
		self.game_id= game_id
		self.games[game_id]['status'] = "cancelled"

	def updateLeaderboard(self):
		pass


a = 3

mark = Player(a)
mark.name = "Mark"
dealer = Dealer()
floorman = Floorman()
floorman.createGame(4)

print mark.name
print mark.member_id
print"-----"
print floorman.leaderboard
print floorman.games
print"-----"
print dealer.suits
mark.joinGame(1)
print floorman.games


