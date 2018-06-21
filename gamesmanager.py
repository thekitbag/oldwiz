games = {0:
			{
			'id': 0,
			'players':4,
			'status': 'open',
	        'entrants':["Shannon"]
	        },
	    1:
	        {
	        'id': 1,
	        'players':3,
	        'status': 'open',
	        'entrants':["Steven", "Elaine", "Michael"]
	        },
	    2:
	        {
	        'id': 2,
	        'players':4,
	        'status': 'running',
	        'entrants':["x", "y"]
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


		




			