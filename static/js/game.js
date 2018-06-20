var game_id = -1;
var user = localStorage.getItem('username');
var game_data = {}



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
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url: '/getTournamentInfo',
		data: JSON.stringify({'user': user}),		
		success: function(response){
			game_data = JSON.parse(response);
		},
		error: function(error){
			console.log(error);
		}
	});
}

$(document).ready(function() {
	getGameInfo();			
});

$(document).on("click","#choosePlayersubmit",function(){
	displayPods(game_data['players']);			
});