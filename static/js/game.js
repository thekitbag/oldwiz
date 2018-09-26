var username = ""
var my_pod_id = ""


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
            socket.emit('connect to game');           
        });

socket.on('update username', function(data) {
	username = data;
});

socket.on('game data', function(data) {			
        parsed_response = JSON.parse(data);
        truedata = JSON.parse(parsed_response);
		displayGameInfo(truedata);
		socket.emit('data received');
    });

socket.on('new player registered', function(update_data) {
		data = JSON.parse(update_data);
		updateEntrants(data);
		});

socket.on('game started', function(data) {
		//layout the game space
		layoutGameSpace();		
		setTimeout(function(){ socket.emit('game ready', data); }, 3000);		
		});

socket.on('hole cards', function(data) {
		layoutGameSpace();
		card = createElement("div", "card", "card1")
		attatchElement(card, my_pod_id);
		card.innerHTML = data;
		});



function createElement(type, className, id){
	a = document.createElement(type);
	a.setAttribute("class", className);
	a.setAttribute("id", id);
	return a
}

function attatchElement(element, target){
	return document.getElementById(target).appendChild(element);
}

function displayGameInfo(game_data) {	
	for (var i = 0; i < game_data['size']; i++){
		var pod = createElement("div", "pod", "pod"+i);
		pod.innerHTML="empty"
		attatchElement(pod, "game-space");
	};
	for (var i = 0; i < game_data['entrants'].length; i++){	
		pod1 = document.getElementById("pod"+i)
		if (game_data['entrants'][i] != null) {
			pod1.innerHTML = game_data['entrants'][i];
		};		
	};
	for (var i = 0; i < game_data['entrants'].length; i++){	
		pod1 = document.getElementById("pod"+i)
		if (pod1.innerHTML == username) {
			pod1.style.backgroundColor  = "pink";
			my_pod_id = pod1.id;
			console.log(my_pod_id);
		};
	};
};

function updateEntrants(data) {	
	for (var i = 0; i < data['entrants'].length; i++){		
		pod1 = document.getElementById("pod"+i)
		if (data['entrants'][i] != null) {
			pod1.innerHTML = data['entrants'][i];
		};		
	};
};

function layoutGameSpace() {
	document.getElementById("game-space").style.backgroundColor  = "green";
	var pods = document.getElementsByClassName("pod");
}