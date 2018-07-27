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
            // Use a "/test" namespace.
            // An application can open a connection on multiple namespaces, and
            // Socket.IO will multiplex all those connections on a single
            // physical channel. If you don't care about multiple channels, you
            // can set the namespace to an empty string.
            namespace = '/test';

            // Connect to the Socket.IO server.
            // The connection URL has the following format:
            //     http[s]://<domain>:<port>[/<namespace>]
            var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

            // Event handler for new connections.
            // The callback function is invoked when a connection with the
            // server is established.
            socket.on('connect', function() {
                socket.emit('my_event', {data: 'I\'m connected!'});
            });

            // Event handler for server sent data.
            // The callback function is invoked whenever the server emits data
            // to the client. The data is then displayed in the "Received"
            // section of the page.
            socket.on('my_response', function(msg) {
                $('#game-space').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
            });

                    

            // Handlers for the different forms in the page.
            // These accept data from the user and send it to the server in a
            // variety of ways
            $('#testbtn').submit(function(event) {
                socket.emit('my_event', {data: 'test data'});
                return false;
            });
            $('form#broadcast').submit(function(event) {
                socket.emit('my_broadcast_event', {data: $('#broadcast_data').val()});
                return false;
            });
            $('form#join').submit(function(event) {
                socket.emit('join', {room: $('#join_room').val()});
                return false;
            });
            $('form#leave').submit(function(event) {
                socket.emit('leave', {room: $('#leave_room').val()});
                return false;
            });
            $('form#send_room').submit(function(event) {
                socket.emit('my_room_event', {room: $('#room_name').val(), data: $('#room_data').val()});
                return false;
            });
            $('form#close').submit(function(event) {
                socket.emit('close_room', {room: $('#close_room').val()});
                return false;
            });
            $('form#disconnect').submit(function(event) {
                socket.emit('disconnect_request');
                return false;
            });		 	
});

