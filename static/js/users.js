var user = localStorage.getItem('username');

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
					document.cookie = "username=John Doe";
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

// Get the input field
var input = document.getElementById("log-in-btn");
// Execute a function when the user releases a key on the keyboard
input.addEventListener("keyup", function(event) {
  // Cancel the default action, if needed
  event.preventDefault();
  // Number 13 is the "Enter" key on the keyboard
  if (event.keyCode === 13) {
    // Trigger the button element with a click
    document.getElementById("log-in-btn").click();
  }
});