var user = localStorage.getItem('username');

var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function() {
            socket.emit('connect to lobby', {data: user});
        });


socket.on('lobby data', function(data) {
		document.getElementById('welcome').innerHTML = "Welcome to the lobby " + user	
        parsed_response = JSON.parse(data);
		addGamesToList(parsed_response);	
    });

socket.on('lobby update', function(data) {
		parsed_data = JSON.parse(data)
		var game = parsed_data['game']
		console.log(game);
		var elementid = 'game' + game + 'valueEntrants'
		document.getElementById(elementid).innerHTML = parsed_data['entrants']
    });

socket.on('registration succesful', function(data) {
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
		var gameid = i+1		
		var game = createElement("div", "game", "game"+gameid)
		attatchElement(game,"games-list");			
		for (var j = 0; j < 4; j++){
			titles = ["Game Id", "No. of Players", "Entrants", "Status"]
			keys = 	["id", "size", "entrants", "status"]		
			//this id naming is fucked			
			var gameboxinfo = createElement("div", "game-info", "game"+gameid+"box"+j);
			var infotitle = createElement("div", "title", "game"+gameid+"title"+titles[j]);
			var infovalue = createElement("div", "value", "game"+gameid+"value"+titles[j]);
			attatchElement(gameboxinfo, "game"+gameid)
			gameboxinfo.appendChild(infotitle);
			gameboxinfo.appendChild(infovalue);
			infotitle.innerHTML = titles[j]
			infovalue.innerHTML = gamedata[i][keys[j]]			
		}		
		var regbutton = createElement("div", "btn reg", "reg"+gamedata[i]['id']);
		regbutton.innerHTML = "Register";
		attatchElement(regbutton, "game"+gameid)
	}	
}


$(document).on("click",".reg",function(){
	buttonid = this.id;
	tournamentid = buttonid[3];
	socket.emit('register request', {"username": user, 'gameID':tournamentid})			
});

