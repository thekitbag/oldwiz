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


function addGamesToList(gamedata){
	var number_of_games = (Object.keys(gamedata).length);
	for (var i = 0; i < number_of_games; i++) {
		var game = document.createElement("div");
		game.setAttribute("class", "game");
		game.setAttribute("id", "game"+i);
		document.getElementById("games-list").appendChild(game);		
		var gamebox = document.getElementById("game"+i);
		var number_of_data_points = (Object.keys(gamedata[i]).length);		
		for (var j = 0; j < number_of_data_points; j++){
			var gameboxinfo = document.createElement("div");
			var infotitle = document.createElement("div");
			var infovalue = document.createElement("div");						
			var key = (Object.keys(gamedata[i])[j]);
			var value = gamedata[i][key];
			gameboxinfo.setAttribute("class", "game-info");
			infotitle.setAttribute("class", "title");
			infovalue.setAttribute("class", "value");
			gameboxinfo.setAttribute("id", "game-"+key);			
			gamebox.appendChild(gameboxinfo);
			gameboxinfo.appendChild(infotitle);
			gameboxinfo.appendChild(infovalue);
			infotitle.innerHTML = key;
			infovalue.innerHTML = value;
		}
		var regbutton = document.createElement("div");
		regbutton.setAttribute("class", "btn reg");
		regbutton.setAttribute("id", "reg"+i);
		regbutton.innerHTML = "Register";
		gamebox.appendChild(regbutton);
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
