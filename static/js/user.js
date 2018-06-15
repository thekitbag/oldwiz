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
					setToken(response);
					console.log(token);
				}
								
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

var token = "";

function setToken(serverToken) {
	token = serverToken;
}