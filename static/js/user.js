$(function(){
	$('#log-in-btn').click(function(){
		$.ajax({
			url: '/log-in',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				if (response == "Log in failed") {
					console.log(response);
				} else {
					var parsed_response = JSON.parse(response)
					setToken(parsed_response['token']);
					setUsername(parsed_response['username'])
					console.log(token);
					console.log(username)
				}
								
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

var token = "";
var username = ""

function setToken(serverToken) {
	token = serverToken;
}

function setUsername(dbname) {
	username = dbname;
}