var user = localStorage.getItem('username');

function populateLobby() {
	$.ajax({
			url: '/getActiveGames',
			type: 'GET',
			success: function(response){
				parsed_response = JSON.parse(response);
				addGamesToList(parsed_response);
			},
			error: function(error){
				console.log(error);
			}
		});
}

function createElement(type, className, id){
	a = document.createElement(type);
	a.setAttribute("class", className);
	a.setAttribute("id", id);
	return a
}

function attatchElement(element, target){
	return document.getElementById(target).appendChild(element);
}


//[{"entrants": ["Mark"], "id": 1, "players": 4, "status": "open"}, {"entrants": ["Mark"], "id": 2, "players": 5, "status": "open"}]
function addGamesToList(gamedata){
	var number_of_games = gamedata.length	
	for (var i = 0; i < number_of_games; i++) {
		var game = createElement("div", "game", "game"+i)
		attatchElement(game,"games-list");	
		number_of_data_points = Object.keys(gamedata[i]).length;		
		for (var j = 0; j < number_of_data_points; j++){
			var key = Object.keys(gamedata[i])[j];
			var value = gamedata[i][key];
			var gameboxinfo = createElement("div", "game-info", "game-"+key);
			var infotitle = createElement("div", "title", "info-"+key);
			var infovalue = createElement("div", "value-"+value);
			attatchElement(gameboxinfo, "game"+i)
			gameboxinfo.appendChild(infotitle);
			gameboxinfo.appendChild(infovalue);
			infotitle.innerHTML = key;
			infovalue.innerHTML = value;
		}
		var regbutton = createElement("div", "btn reg", "reg"+gamedata[i]['id']);
		regbutton.innerHTML = "Register";
		attatchElement(regbutton, "game"+i)
	}	
}

function registerUser(tournament){
	var reg_details = {'username': user, 'gameID':tournament};	
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url: '/registerUser',
		data: JSON.stringify(reg_details),		
		success: function(response){
			if (response == "Registration Succesful"){
				location.href="/game";
			} else {
				console.log(response);				
			}
		},
		error: function(error){
			console.log(error);
		}
	});
};

function clearLobby() {
	var listToClear = document.getElementById("games-list")
	while (listToClear.childNodes.length > 0) {
		listToClear.removeChild(listToClear.lastChild);
	}
}

function refresh() {
	clearLobby();
    populateLobby();
    setTimeout(refresh, 10000);    
}

$(document).on("click",".reg",function(){
	buttonid = this.id;
	tournamentid = buttonid[3];
	registerUser(tournamentid);			
});

$(document).ready(function() {
    refresh();    
});
