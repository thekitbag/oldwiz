var user = localStorage.getItem('username');
var game_data = {}
var game_started = false



function displayCards(cards) {
	var parsedCards = JSON.parse(cards)
	console.log(parsedCards);					
}

function displayPods(players) {
	for (var i = 0 ; i < players; i++){
		var createPod = document.createElement("div");
		var pod_id	= "pod" + i;
		createPod.setAttribute("class", "game-pod");
		createPod.setAttribute("id", pod_id);
		document.getElementById("game-space").appendChild(createPod);
	}
}

function getGameInfo() {
	game = {'player_name': user}
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url: '/getGameInfo',
		data: JSON.stringify(game),		
		success: function(response){
			game_data = JSON.parse(response);
		},
		error: function(error){
			console.log(error);
		}
	});
}

function displayPreGameInfo() {
	//will display the names of the current regustrants and how many players we're waititng for
	console.log("waiting")
}

function displayGameInfo() {
	//will display all of the players and their cards
	console.log("started")
}

function refresh() {
	getGameInfo()
	displayPreGameInfo()
    setTimeout(refresh, 10000);    
}


$(document).ready(function() {
	while (game_started == true) {
		refresh();
	}
	if (game_started == false) {
		displayGameInfo();
	}
});

