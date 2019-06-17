
$('#login-form').on('submit',function(event){
	event.preventDefault();

	var username=$('#username').val();
	var password=$('#password').val();

	$.ajax({
		url: '/login',
		method: 'POST',
		contentType: 'application/json',
		data: JSON.stringify({
			username:username,
			password:password
		}),
		success: function(res){
			if (res.err1.length>0){
				$('#err1').show();
				$('#err1').html(res.err1);
			}else{
				window.location=res.redirect;
			},
			error: function(err){
				console.log(err);
			}
		}
	})
});