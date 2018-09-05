var user = localStorage.getItem('username');

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
            socket.emit('connect to game', {data: user});           
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
    //});


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
};

function updateEntrants(data) {	
	for (var i = 0; i < data['entrants'].length; i++){		
		pod1 = document.getElementById("pod"+i)
		if (data['entrants'][i] != null) {
			pod1.innerHTML = data['entrants'][i];
		};		
	};
};