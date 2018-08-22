var user = localStorage.getItem('username');

var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function() {
            socket.emit('connect to lobby', {data: user});
        });

socket.on('player joined', function(number) {
	document.getElementById('welcome').innerHTML = "Welcome to the lobby " + user
	document.getElementById('players').innerHTML = "Active players = " + number
});

socket.on('lobby data', function(data) {	
        parsed_response = JSON.parse(data);
		addGamesToList(parsed_response);
    });

socket.on('registration succesful', function(data) {	
	localStorage.setItem('active_game',data['game']);
	window.location.href='/game';
})

function createElement(type, className, id){
	a = document.createElement(type);
	a.setAttribute("class", className);
	a.setAttribute("id", id);
	return a
}

function attatchElement(element, target){
	return document.getElementById(target).appendChild(element);
}


//[{"Id": 0, "entrants": [], "id": 2, "size": 5, "status": "open"}]
function addGamesToList(gamedata){
	var number_of_games = gamedata.length
	for (var i = 0; i < number_of_games; i++) {
		var game = createElement("div", "game", "game"+i)
		attatchElement(game,"games-list");		
		for (var j = 0; j < 4; j++){
			titles = ["Game Id", "No. of Players", "Entrants", "Status"]
			keys = 	["id", "size", "entrants", "status"]		
			var gameboxinfo = createElement("div", "game-info", "game-"+j);
			var infotitle = createElement("div", "title", "info-"+j);
			var infovalue = createElement("div", "value", "value-"+j);
			attatchElement(gameboxinfo, "game"+i)
			gameboxinfo.appendChild(infotitle);
			gameboxinfo.appendChild(infovalue);
			infotitle.innerHTML = titles[j]
			infovalue.innerHTML = gamedata[i][keys[j]]			
		}		
		var regbutton = createElement("div", "btn reg", "reg"+gamedata[i]['id']);
		regbutton.innerHTML = "Register";
		attatchElement(regbutton, "game"+i)
	}	
}


$(document).on("click",".reg",function(){
	buttonid = this.id;
	tournamentid = buttonid[3];
	socket.emit('register request', {"username": user, 'gameID':tournamentid})			
});

