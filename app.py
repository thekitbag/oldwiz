from flask import Flask, session, render_template, request, json, redirect, url_for, escape
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import sqlite3
import time

db = 'wizard.sqlite' 
app = Flask(__name__)
app.debug = True
app.secret_key = 'abc123'
socketio = SocketIO(app)


#-----------------------

@socketio.on('connect to lobby')
def handle_lobby_connection(data):
    """returns all active games"""    
    Messages.sendLobbyData(request.sid)   

@socketio.on('register request')
def handle_registration_request(data):
    #takes a tournament ID and tries to register the user to that game
    username = session['username']    
    game = int(data['gameID'])
    sid = request.sid
    Messages.sendRegistrationRequest(username, game, sid)  
    
@socketio.on('connect to game')
def handle_game_connection():
    """returns the game info for the users game"""
    #this needs to include seat positions
    playername = session['username']   
    player_object = Player.getPlayerByName(playername)
    player_sid = request.sid 
    player_object.sid = player_sid    
    game = player_object.game
    gamedata = Floorman.getGameInfo(game.game_id)
    emit('update username', playername, room=player_sid)
    emit('game data', json.dumps(gamedata), room=player_sid)

@socketio.on('game ready')
def sendHoleCards(data):
    """sends the user their hole cards"""
    game = Floorman.getGameById(int(data))
    game.status = "running"     
    Dealer.dealCards(game)
    time.sleep(5)    
    for player in game.entrants:                   
        emit('hole cards', json.dumps(str(player.hand)), room=player.sid)


#-----------------------


#-----------------------
@app.route("/")
def home():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])    
    return render_template('index.html')

@app.route("/lobby")
def showLobby():
    return render_template('lobby.html')

@app.route("/game")
def showGame():
    return render_template('game.html')
#-----------------------

#-----------------------
#routes for user management  
@app.route('/log-in',methods=['POST','GET'])
def logIn():
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("SELECT MEMBER_ID FROM USERS WHERE USERNAME = ? AND PASSWORD_HASH= ?;", (username, password))        
        results = c.fetchall()
        if len(results) > 0:
            session['username'] = username            
            return json.dumps({'username': username})
        else:
            return "Log in failed"
#-----------------------

import random
import collections
from flask import json


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
    players = set()
    member_id_count = 0
    def __init__(self, username):
        if Player.checkIfPlayerAlreadyExists(username) == False:
            self.member_id = self.member_id_count + 1
            Player.member_id_count += 1
            self.username = username
            self.auth_token = ""
            self.hand = []
            self.sid = ""   

    def __repr__(self):
        return self.username

    def register(self, game):
        if Floorman.validateRegistration(self, game) == True:
            self.game = game        
            game.scoreboard[self] = 0
            current_player_count = len(game.entrants)
            game.seats[current_player_count] = self
            game.entrants.append(self)
            game.trick_count[self] = 0
            if len(game.entrants) == game.size:
                game.status = "starting"                
                return "game full"
        else: return "Registration failed"  

    def playCard(self, card):       
        if Dealer.is_valid_move(card, self.game.pile, self.hand) ==  "first card":
            self.game.pile['valid_suit'] = card.suit
            self.game.pile[self] = card
            self.hand.remove(card)
        elif Dealer.is_valid_move(card, self.game.pile, self.hand) ==  True and card in self.hand:                      
            self.game.pile[self] = card
            self.hand.remove(card)
        else: 
            raise ValueError('invalid move')    

    @classmethod
    def getPlayerByName(cls, name):
        player = [player for player in Player.players if name == player.username]
        if len(player) > 0:
            return player[0]
        else:
            return "New player"

    @classmethod
    def checkIfPlayerAlreadyExists(cls, playername):
        existingplayers = []
        for i in Player.players:
            existingplayers.append(i.username)
        if playername in existingplayers:
            return True
        else: return False


    

    


class Dealer():
    @classmethod
    def is_valid_move(cls, card, pile, hand):
        available_cards = []                
        if len(pile) == 0:
            return "first card"
        else:
            for i in hand:
                if i.suit == pile ['valid_suit']:
                    available_cards.append(i)
        if card.suit == pile['valid_suit']:
            return True
        elif len(available_cards) == 0:
            return True     
        else:
            return False

    @classmethod
    def declareWinner(cls, game):
        cards = []
        card_ranks = []
        valid_suit = game.pile['valid_suit']
        del game.pile['valid_suit']     
        for i in game.pile.values():
            if i.__class__ == Card and i.suit == valid_suit:
                cards.append(i)
        for i in cards:
            card_ranks.append(i.rank)
        for player in game.pile.keys():
            if game.pile[player].rank == max(card_ranks) and game.pile[player] in cards:
                print ""
                print "%s wins this trick" %(player)
                print ""
                game.trick_count[player] += 1
        game.pile.clear()       

    @classmethod
    def requestActions(cls, game):
        active_player = game.button_position
        for player in range(game.size):
            player = game.seats[active_player]
            print "%s's Cards %s" %(player, player.hand)
            chosen_card = int(raw_input("Pick Your Card Please %s :  " %player))            
            try:
                player.playCard(player.hand[chosen_card])
            except:
                print "%s's Cards %s" %(player, player.hand)
                chosen_card = int(raw_input("Invalid. Pick a different card please %s :  " %player))
                player.playCard(player.hand[chosen_card])
            print ""
            print "pile: %s" %(game.pile)
            print ""
            if active_player + 1 > game.size-1:
                active_player = 0
            else: active_player += 1

    @classmethod
    def requestPredictions(cls, game):
        active_player = game.button_position        
        for player in range(game.size):
            player = game.seats[active_player]
            chosen_card = int(raw_input("%s How many tricks do you think you'll win:  " %player))
            game.predictions[player] = chosen_card
            game.trick_count[player] = 0
            if active_player + 1 > game.size-1:
                active_player = 0
            else: active_player += 1
        print ""
        print "--Predictions--"
        print game.predictions
        print ""

    @classmethod
    def printGameState(cls, game):
        print "----------------------------------------------GAMEROUND %s----------------------------------------------" %(game.round-1)
        print ""
        print "---------------------subround %s---------------------"%(game.subround)
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
            game.subround += 1
            for player in game.entrants:
                card = game.deck.randomCard()
                player.hand.append(card)
        print game.__dict__
        game.round += 1

    @classmethod
    def updateLeaderboard(cls, game):
        for player in game.entrants:
            if game.predictions[player] == game.trick_count[player]:
                game.scoreboard[player] += game.predictions[player] * 10
            else: game.scoreboard[player] -= abs(game.predictions[player] - game.trick_count[player]) * 10

    @classmethod
    def start_game(cls, game):
        Dealer.decideButton(game)
        for i in range(game.length):                
            Dealer.dealCards(game)
            game.subround = 1
            Dealer.printGameState(game)
            #Dealer.requestPredictions(game)
            for i in range(game.round-1):
                #Dealer.requestActions(game)
                game.subround += 1
                Dealer.printGameState(game)
                Dealer.declareWinner(game)
                if game.button_position + 1 > game.size -1:
                    game.button_position = 0
                else: game.button_position += 1
            Dealer.updateLeaderboard(game)

    @classmethod
    def decideButton(cls, game):
        game.button_position = random.randint(0,game.size-1)

class Game():
    deck = Deck()
    def __init__(self, game_id, size, length):
        self.game_id= game_id
        self.status = "open"
        self.size = size
        self.length = length
        self.entrants = []
        self.scoreboard = {}
        self.pile = collections.OrderedDict()
        self.seats = {}
        self.round = 1
        self.subround = 1
        self.predictions = {}
        self.trick_count = {}
        self.button_position = 0
        self.clients_ready = 0

    def __repr__(self):
        #human readable representation of game object       
        return "Game ID:" + str(self.game_id)

    def updateClientsReady(self):
        self.clients_ready += 1
        if self.clients_ready == self.size:
            self.status = "started"
    

class Floorman():
    active_games = 0
    id_count = 0
    games = []

    @classmethod
    def addGame(cls, size, length):
        game = Game(Floorman.id_count+1, size, length)
        Floorman.games.append(game)
        Floorman.id_count += 1

    @classmethod
    def getGameById(cls, game_id):
        game = [game for game in Floorman.games if game_id == game.game_id]
        return game[0]

    @classmethod
    def getGameInfo(cls, game_id):
        game = [game for game in Floorman.games if game_id == game.game_id]
        gameobj = game[0]
        game_info = {"status":gameobj.status, "size": gameobj.size, "entrants":[]}
        for player in gameobj.entrants:
            game_info['entrants'].append(player.username)
        return json.dumps(game_info)

    @classmethod
    def getActiveGames(cls):
        active_games = [game for game in Floorman.games if game.status == 'open']
        jsonable_active_games = []
        number_of_games = len(active_games)
        for i in range(number_of_games):
            gamedata = {"id":0, "size":0, "entrants":[]}
            gamedata['id'] = active_games[i].game_id
            gamedata['size'] = active_games[i].size
            gamedata['status'] = active_games[i].status
            playernames = []
            for player in active_games[i].entrants:
                playernames.append(player.username)
            gamedata['entrants'] = playernames
            jsonable_active_games.append(gamedata)
        return json.dumps(jsonable_active_games)
        

    @classmethod
    def getEntrantList(cls, game):
        entrantlist = []
        for player in game.entrants:
            entrantlist.append(player.username)
        data ={"game": game.game_id, "entrants":entrantlist} 
        return json.dumps(data)

    @classmethod
    def validateRegistration(cls, player, game):
        """ checks if player is eligible to register for this game"""
        game_open = False
        Player_already_registered = True
        if player not in game.entrants:
            Player_already_registered = False
        if game.status == "open":
            game_open = True
        if game_open == True and Player_already_registered == False:
            return True
        else: return False

class Messages():
    @classmethod
    def sendLobbyData(cls, sid):
        games = Floorman.getActiveGames()
        emit('lobby data', games, room=sid)

    @classmethod
    def sendRegistrationRequest(cls, username, game_id, sid):             
        player = Player(username)
        game = Floorman.getGameById(game_id)
        Player.players.add(player)      
        player.register(game)
        playerlist = Floorman.getEntrantList(game)
        if player in game.entrants:
            session['active_game'] = game
            emit('registration succesful', room=sid)                       
            emit('lobby update', playerlist,  broadcast=True) 
        else: return "Registration Failed"  
        for player in game.entrants:
            emit('new player registered', playerlist, room=player.sid)
        if game.status == "starting":        
            for player in game.entrants:            
                emit('game started', game.game_id, room=player.sid)




        






        

    




Floorman.addGame(3,3)
Floorman.addGame(5,3)





if __name__ == "__main__":  
  socketio.run(app, host='0.0.0.0')

     