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
    player_sid = request.sid
    if gamelogic.Player.getPlayerByName(data['data']) == "New player":
        player_object = gamelogic.Player()
        player_object.username = data['data']
        player_object.sid = player_sid
        gamelogic.Player.players.add(player_object)
        print gamelogic.Player.players
    else:
        player = gamelogic.Player.getPlayerByName(data['data'])
        player.sid = player_sid
        print gamelogic.Player.players
    emit('player joined', len(gamelogic.Player.players), broadcast=True)
    active_games = [game for game in gamelogic.Floorman.games if game.status == 'open']    
    jsonable_active_games = []
    for i in range(len(active_games)):
        game = {"id":0, "size": 0, "entrants": [], "status": ""}
        players = []
        game["id"] = active_games[i].game_id
        game["size"] = active_games[i].size
        for player in active_games[i].entrants:
            players.append(player.username)
        game["entrants"] = players
        game["status"] = active_games[i].status
        jsonable_active_games.append(game)
    emit('lobby data', json.dumps(jsonable_active_games), room=player_sid)    

@socketio.on('register request')
def handle_registration_request(data):
    jsonData = data       
    username = str(jsonData['username'])
    game = gamelogic.Floorman.getGameById(int(jsonData['gameID']))[0]        
    player = gamelogic.Player.getPlayerByName(username)    
    player.register(game)
    if player in game.entrants:
        emit('registration succesful', {'game': json.dumps(game.game_id)}, room=player.sid)
    else: return "Registration Failed"   
    
@socketio.on('connect to game')
def handle_game_connection(data):
    pass
    #return game data to that user


@socketio.on('x event')
def handle_establish_connection(data):
    player_sid = request.sid    
    game = gamelogic.Floorman.getGameAndPlayerByPlayerName(data['data'])['game']
    player =  gamelogic.Floorman.getGameAndPlayerByPlayerName(data['data'])['name']
    player.sid = player_sid 
    gamedata = gamelogic.Floorman.getGameInfo(game.game_id)   
    emit('confirm_connection', "Player Connected", broadcast=True)
    emit('game_data', json.dumps(gamedata), broadcast=True)

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

     