var user = localStorage.getItem('username');
var game_data = {}
var game_started = false

function createElement(type, className, id){
	a = document.createElement(type);
	a.setAttribute("class", className);
	a.setAttribute("id", id);
	return a
}

function attatchElement(element, target){
	return document.getElementById(target).appendChild(element);
}

var socket = io.connect('http://' + document.domain + ':' + location.port);
        socket.on('connect', function() {
            socket.emit('connect event', {data: user});
        });

socket.on('confirm_connection', function() {
            console.log("Connection established");
        });

socket.on('game_data', function(data) {
            console.log("Game data received");
            console.log(data)
        });


/*
function getGameInfo() {
	game = {'member_id': 1001}
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

function displayGameInfoOnLoad() {
	for (var i = 0; i < game_data['players']; i++){
		var pod = createElement("div", "pod", "pod"+i);
		pod.innerHTML="empty"
		attatchElement(pod, "game-space");
		pod1 = document.getElementById("pod"+i)
		if (game_data['entrants'][i] != null) {
			pod1.innerHTML = game_data['entrants'][i];
		};		
	};
};

function pollForUpdates() {
	for (var i = 0; i < game_data['players']; i++){
		pod1 = document.getElementById("pod"+i)
		if (game_data['entrants'][i] != null) {
			pod1.innerHTML = game_data['entrants'][i];
		};		
	};
}


$(document).ready(function() {
	getGameInfo();
	window.setTimeout(function(){
		displayGameInfoOnLoad();
	}, 500);	
	window.setInterval(function(){
		getGameInfo();
		window.setTimeout(function(){
		pollForUpdates();
	}, 500);		
}, 5000);
*/
           