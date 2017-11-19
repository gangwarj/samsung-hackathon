$(document).ready(function(){
	
	function validateEmail(email) {
	    var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
	    if (filter.test(email)) {
	        return true;
	    }
	    else {
	        return false;
	    }
	};
	/* CHECK SESSION*/
	$.ajax({
		type: 'POST',
		url: './utils/checkSessionNull.php',
		success: function (data) {
			console.log(data);
			if(data == true)
			{
				console.log('no');
			}else
			{
				$.confirm({
					closeIcon: false,
					title:'You are already Logged In.',
					columnClass: 'medium',
				    content: ' Please Logout first to login as a different user.',
				    theme:'supervan',
				    opacity:1,
				    buttons: {
				        Activate: {
				        	btnClass:'btn-green',
				            text: 'Take me to Dashboard',
				            action: function () {
				                location.href = 'dashboard.html';
				            }
				        },
				        Cancel: {
				        	btnClass:'btn-red',
				            text: 'Log Out',
				            action: function () {
				                $.ajax({
									type:'POST',
									url:'./utils/logout.php',
									success:function(){
										location.href = 'index.html';
									}
								});
				            }
				        }
				    }
				});
			}
			
		}        
	});
	
	

	$(document.body).on('click', '#loginBtn', function(){		
		var email = $('#email').val();
		var password = $('#password').val();
		// console.log(phone);
		// console.log(password);
		
		if(email == '')
		{
			$.alert("Please enter email."); 
		}  
		else if(!validateEmail(email))  
		{  
			$.alert("Please enter correct email.");  
						
		}  
		else if( password == '') 
		{  
			$.alert("Please enter password.");  
			$('#password').val('');		
		}else{
			$.ajax({
				type: 'POST',
				url: './utils/login.php',
				data: {email:email,password:password},
				success: function (data) {	
					console.log(data);				
					window.location="dashboard.html";
				},
				statusCode:{
					403: function() {
						$.alert('Invalid Credentials');
					},
					401: function() {
						$.alert('Unauthorized User');
					} 
				}         
			});
		}	
		
	})
})
