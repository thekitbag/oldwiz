from flask import Flask, render_template, request, json
import sqlite3

import dealeractions
import usermanager
import gamesmanager

db = 'wizard.sqlite' 
app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/lobby")
def showLobby():
    return render_template('lobby.html')

@app.route("/game")
def showGame():
    return render_template('game.html')


#routes for getting available games
@app.route('/getActiveGames',methods=['GET'])
def getActiveGames():          
        games = json.dumps(gamesmanager.games)
        return games

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
        jsonData = request.get_json()          
        username = str(jsonData['username'])
        game = int(jsonData['gameID'])
        gamesmanager.registerPlayer(game,username)
        return "Registration Succesful"

@app.route('/getTournamentInfo',methods=['POST','GET'])
def getTournamentInfo():
        jsonData = request.get_json()          
        user = str(jsonData['user'])
        game_details = gamesmanager.getTournamentInfo(user)
        return json.dumps(game_details)


#routes for getting player actions
"""@app.route('/startGame',methods=['POST','GET'])
def startGame():
        numberOfPlayers = int(request.form['choosePlayers'])
        dealeractions.buildDeck()
        dealeractions.setPlaces(numberOfPlayers)
        dealeractions.dealCards(1)        
        allHands = json.dumps(dealeractions.hands)
        return allHands """

def startGame():
    #create an instance of a game in dealeractions with all the necessary bits, set the leaderboard, seats, gameID, using data from the gamesmanager 
    abc = dealeractions.GameInstance()
    abc.gameId=2
    print abc.__dict__

        

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
            token = usermanager.createToken()
            return json.dumps({'username': username, 'token':token})      
        else:
            return "Log in failed"

#route for shutting down the sserver
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

#route to start the app

if __name__ == "__main__":
  app.run()

startGame()