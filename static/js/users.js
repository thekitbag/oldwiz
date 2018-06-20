$(function(){
	$('#log-in-btn').click(function(){
		$.ajax({
			url: '/log-in',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				if (response == "Log in failed") {
					alert("Log in failed, try again");
				} else {
					var parsed_response = JSON.parse(response);
					localStorage.setItem('username',parsed_response['username']);
					localStorage.setItem('token',parsed_response['token']);
					window.location.href='/lobby';
				}
								
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

