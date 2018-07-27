$(document).ready(function() {
    clientid = Math.floor(Math.random()*2);
    namespace = '/client' + clientid;
    console.log(namespace);    
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    console.log(socket);
    socket.on('connect', function() {
        message = 'Client' + namespace + 'connecting';
        socket.emit('establish connection', {data: message})
        console.log('trying to connect');
    });

    socket.on('game_started', function(msg) {
        a = createElement("div", "message", "message")
        attatchElement(a, "public")
        a.innerHTML = msg
    });

    socket.on('my_response', function(msg) {
        a = createElement("div", "message", "message")
        attatchElement(a, "public")
        a.innerHTML = msg
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

    $(document).on("click","#start-game",function(){
    	socket.emit('start game');
            return false;		
    });
        
});