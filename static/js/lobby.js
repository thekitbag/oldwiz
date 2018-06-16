function populateLobby() {
	$.ajax({
			url: '/getActiveGames',
			type: 'GET',
			success: function(response){
				parsed_response = JSON.parse(response);
				addGamesToList(parsed_response)								
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
		console.log(gamedata);
		console.log("--");
		console.log(gamedata[0]);
		console.log("--");
		console.log(Object.keys(gamedata[0])[0]);
		console.log("--");
		for (var j = 0; j < number_of_data_points; j++){
			var gameboxinfo = document.createElement("div");
			gameboxinfo.setAttribute("class", "game-info");
			var key = (Object.keys(gamedata[i])[j]);
			gameboxinfo.setAttribute("id", "game-"+key);
			gamebox.appendChild(gameboxinfo);
			gameboxinfo.innerHTML=gamedata[i][key];
		}
	}	
}

$(document).ready(function() {
	populateLobby();	
});


