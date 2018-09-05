from flask import Flask, render_template, request, json
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import sqlite3
import time


import gamelogic

db = 'wizard.sqlite' 
app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)


#-----------------------

@socketio.on('connect to lobby')
def handle_lobby_connection(data):     
    games = gamelogic.Floorman.getActiveGames()    
    emit('lobby data', games, room=request.sid)    

@socketio.on('register request')
def handle_registration_request(data):      
    username = str(data['username'])
    game = gamelogic.Floorman.getGameById(int(data['gameID']))[0]        
    player = gamelogic.Player(username)
    gamelogic.Player.players.add(player)      
    player.register(game)
    playerlist = gamelogic.Floorman.getEntrantList(game)
    if player in game.entrants:
        emit('registration succesful', room=request.sid)                       
        emit('lobby update', playerlist,  broadcast=True) 
    else: return "Registration Failed"  
    for player in game.entrants:
        emit('new player registered', playerlist, room=player.sid)

    
@socketio.on('connect to game')
def handle_game_connection(data):
    playername = data['data']    
    player_object = gamelogic.Player.getPlayerByName(playername)
    player_sid = request.sid 
    player_object.sid = player_sid    
    game = player_object.game
    gamedata = gamelogic.Floorman.getGameInfo(game.game_id)
    emit('game data', json.dumps(gamedata), room=player_sid)    
    
@socketio.on('start game')
def handle_start_game():
    print "game started"
    time.sleep(5)
    emit('game_started', "The game has begun", broadcast=True)

#-----------------------



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/lobby")
def showLobby():
    return render_template('lobby.html')

@app.route("/game")
def showGame():
    return render_template('game.html')

@app.route("/game1")
def showWSGame():
    return render_template('game1.html')



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
            return json.dumps({'username': username})      
        else:
            return "Log in failed"


#routes for getting available games


@app.route('/registerUser',methods=['POST','GET'])
def registerUser():        
        jsonData = request.get_json()          
        username = str(jsonData['username'])
        game = gamelogic.Floorman.getGameById(int(jsonData['gameID']))[0]        
        player = gamelogic.Player.getPlayerByName(username)    
        player.register(game)
        if player in game.entrants:
            gamedata = gamelogic.Floorman.getGameInfo(game.game_id)
            emit('registration succesful', {'game': game}, room=player.sid)
        else: return "Registration Failed"
       

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


if __name__ == "__main__":
  #app.run()
  socketio.run(app)

     