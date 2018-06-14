$(function(){
	$('#choosePlayersubmit').click(function(){
		$.ajax({
			url: '/choosePlayers',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				var parsedCards = JSON.parse(response);
				var response_keys = Object.keys(parsedCards);
				var num_of_player = response_keys.length;
				console.log(num_of_player);
				displayPods(num_of_player);				
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

function parseReponse(json) {
	
}

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