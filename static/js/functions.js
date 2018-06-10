$(function(){
	$('#homebtn').click(function(){
		location.href="showHomePage";		
	});

	$('#killserver').click(function(){
		
		$.ajax({
			url: '/shutdown',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response)
			},
			error: function(error){
				console.log(error);
			}
		});		
	});
	$('#skip-button').click(function(){
		location.href="showHomePage";		
	});

});