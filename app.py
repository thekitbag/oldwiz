from flask import Flask, render_template, request, json
import sqlite3

import dealeractions
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

#routes for getting player actions
@app.route('/choosePlayers',methods=['POST','GET'])
def choosePlayers():
        numberOfPlayers = int(request.form['choosePlayers'])
        dealeractions.buildDeck()
        dealeractions.setPlaces(numberOfPlayers)
        dealeractions.dealCards(1)        
        allHands = json.dumps(dealeractions.hands)
        return allHands 

#routes for user management  
@app.route('/log-in',methods=['POST','GET'])
def logIn():
        username = request.form['inputUsername']
        password = request.form['inputPassword']
        print username
        print password 
        conn = sqlite3.connect(db)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("SELECT MEMBER_ID FROM USERS WHERE USERNAME = ? AND PASSWORD_HASH= ?;", (username, password))        
        results = c.fetchall()
        print results
        if len(results) > 0:
            token = usermanager.createToken()
            return token       
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

