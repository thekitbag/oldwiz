class Player():
	def __init__(self,member_id):
		self.member_id = member_id
		self.name = ""
		self.authtoken = ""
		self.active_game = -1

	def joinPool(self):
		Floorman.players[self.member_id]={'name':self.name, 'authtoken':self.authtoken, 'active game':self.active_game}

	def playCard(self, card, game_id):
		self.card = card
		self.game_id = game_id
		print "foo"

	def declare(self,declaration, game_id):
		self.declaration = declaration
		self.game_id = game_id
		print "bar"

	def findActiveGames(self):
		for i in Floorman.games:
			if self.name in Floorman.games[i]['players']:
				print i

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
	suits = ["a","b","c","d"]
	deck = []

	def validatePlayer(self, player, token):
		self.player = player
		self.token = token
		if 1 > 0:
			return True
		else:
			return False

	def buildDeck(self):
		for i in range(1,14):
			for j in self.suits:
				card = str(i)+j
				self.deck.append(card)
		for i in range(4):
			self.deck.append("0J")
			self.deck.append("0W")

	def validateMove(self, game_id, card, pile):
		self.game_id = game_id
		self.card = card
		self.pile = pile
		if 1 > 0:
			return True
		else:
			return False

class Floorman():
	games = {0:
		{
		'id': 0,
		'players':4,
        'entrants':["test1","test2","test3"],	        
		'status': 'test'
        }	    
	}

	game_objects = []

	players = {}

	leaderboard = {}			

	def createGame(self, size):
		self.size = size		
		Floorman.games[max(Floorman.games)+1] = {
		'id': max(Floorman.games)+1,
		'players': size,
		'entrants': [],
		'status': 'open'
		}
		game = Game(10)
		game.status = 'open'
		game.size = size
		Floorman.game_objects.append(game)

	def listOpenGames(self):
		open_games = []
		for i in Floorman.games:
			if Floorman.games[i]['status'] == 'open':
				open_games.append(Floorman.games[i])
		return open_games

	def cancelGame(self, game_id):
		self.game_id= game_id
		Floorman.games[game_id]['status'] = "cancelled"

	def updateLeaderboard(self):
		pass

	def addPlayerToGame(self, player, game):
		self.player = player
		self.game = game		
		self.games[game]['entrants'].append(self.players[player]['name'])
		self.players[player]['active game'] = game
		if len(self.games[game]['entrants']) == self.games[game]['players']:
			self.games[game]['status'] = 'started'


	
	


dealer = Dealer()
floorman = Floorman()
floorman.createGame(4)
floorman.createGame(6)


"""
floorman.listOpenGames()
test_player = Player(1001)
test_player.name = "Mark"
test_player.authtoken = "abcdefg"
test_player.joinPool()


print floorman.players
print floorman.games
print " ----- "
floorman.addPlayerToGame(1001,1)
print floorman.players
print floorman.games



name = getattr(Floorman.games[1]['entrants'][0], 'name')
print name






floorman.listOpenGames()

userID = 1001
username = "Mark"
authtoken = "abcdefg"

player = Player(userID)
player.name = username
player.authtoken = authtoken

player.joinGame(1)

floorman.listOpenGames()


secondUserID = 1002
secondUsername = "Shan"
secondAuthtoken = "hijklmno"

second_player = Player(secondUserID)
second_player.name = secondUsername
second_player.authtoken = secondAuthtoken

second_player.joinGame(1)

floorman.listOpenGames()
"""

