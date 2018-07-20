from flask import Flask, render_template, request, json
import sqlite3

import gamelogic
import usermanager


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
        active_games = gamelogic.floorman.listOpenGames()        
        return json.dumps(active_games)
        

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
        jsonData = request.get_json()          
        username = str(jsonData['username'])
        game = int(jsonData['gameID'])
        player = gamelogic.Player(1001)
        player.name = username
        player.authtoken = "abcdefg"
        player.joinPool()
        gamelogic.floorman.addPlayerToGame(player.member_id, game)
        registered = False
        if username in gamelogic.Floorman.games[game]['entrants']:
            registered = True
        if registered == True:
            return "Registration Succesful"
        else: return "Registration Failed"
        



@app.route('/getGameInfo', methods=['POST', 'GET'])
def getGameInfo():
    data = request.get_json()
    user = data['member_id']
    user_game_id = gamelogic.Floorman.players[user]['active game']
    if gamelogic.Floorman.games[user_game_id]['status'] == 'open':
        return json.dumps(gamelogic.Floorman.games[user_game_id])
    elif gamelogic.Floorman.games[user_game_id]['status'] == 'started':
        game = gamelogic.Game(user_game_id)
        game.status == 'running'
        game.size = gamelogic.Floorman.games[user_game_id]['players']
        dealer = gamelogic.Dealer()
        dealer.buildDeck()
        game.deck = dealer.deck
        return json.dumps(game.deck)
        

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

