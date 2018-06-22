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
        allGames = gamesmanager.games
        activeGames = {}
        for i in allGames:
            if allGames[i]['status'] == 'open':
                activeGames[i]=allGames[i]
        return json.dumps(activeGames)
        

@app.route('/registerUser',methods=['POST','GET'])
def registerUser():
        jsonData = request.get_json()          
        username = str(jsonData['username'])
        game = int(jsonData['gameID'])
        gamesmanager.registerPlayer(game,username)
        registered = False
        for i in gamesmanager.games:
            if username in gamesmanager.games[i]['entrants']:
                registered = True
        if registered == True:
            return "Registration Succesful"
        else: return "Registration Failed"



@app.route('/getGameInfo', methods=['POST', 'GET'])
def getGameInfo():
    data = request.get_json()
    user = str(data['player_name'])
    user_game_id = gamesmanager.findUserGame(user)
    print user_game_id
    status = gamesmanager.games[user_game_id]['status']
    gamesize = gamesmanager.games[user_game_id]['players']
    entrants = gamesmanager.games[user_game_id]['entrants']
    gameFull = False
    if len(entrants) == gamesize:
        gamesmanager.startGame(user_game_id)
        return json.dumps(gamesmanager.games[user_game_id]['gameInfo'])
    else:
        return json.dumps(entrants)


        

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

