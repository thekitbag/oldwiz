import dealeractions

games = {0:
			{
			'id': 0,
			'players':4,
			'status': 'open',
	        'entrants':["Shannon","Steve","Elaine"]
	        }	    
}

def addGame(players):
	games[max(games)+1] = {
	'id': max(games)+1,
	'players': players,
	'entrants': [],
	'status': 'open'
	}


def registerPlayer(game, player):
	games[game]['entrants'].append(player)

def findUserGame(name):
	for i in games:
		if name in games[i]['entrants']:
			return i

def startGame(gameId):
	a = dealeractions.GameInstance(gameId)
	a.players = games[gameId]['entrants']
	a.setScoreboard()
	a.buildDeck()
	a.setPlaces(a.players)
	a.dealCards(1)
	games[gameId]['gameInfo'] = a.__dict__


"""test_game = GameInstance()
test_game.gameId = 1
test_game.players = ["Mark","Shannon","Ant","Gabby"]
test_game.setScoreboard()
test_game.buildDeck()
test_game.setPlaces(test_game.players)
test_game.dealCards(1)

print test_game.__dict__

second_test_game = GameInstance()
second_test_game.gameId = 2
second_test_game.players = ["Mike","De","Steve","Elaine"]
second_test_game.setScoreboard()
second_test_game.buildDeck()
second_test_game.setPlaces(second_test_game.players)
second_test_game.dealCards(4)"""




			