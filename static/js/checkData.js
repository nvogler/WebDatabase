"use strict";
function callJScript(){
	$(document).ready(function() {
		$("new_user").submit(function(e){
			e.preventDefault(e);
		});
    });
	var userInfo = {
		username: document.getElementById("new_username_input").value,
		password1: document.getElementById("new_password1_input").value,
		password2: document.getElementById("new_password2_input").value,
		firstname: document.getElementById("new_firstname_input").value,
		lastname: document.getElementById("new_lastname_input").value,
		email: document.getElementById("new_email_input").value
	};
		
	checkData(userInfo);
	return false;
	}

function checkData(userInfo) {
	var called = 0;
	document.getElementById("errors").innerHTML = "";
	var clientVer = userInfo;
	var userInfo = JSON.stringify(userInfo);
	//Client-Side Validation
	var username = clientVer.username;
	var firstname = clientVer.firstname;
	var lastname = clientVer.lastname;
	var password1 = clientVer.password1;
	var password2 = clientVer.password2;
	var email = clientVer.email;
	
	var clientErrors = [];
	if (username.length < 3){
		clientErrors.push("Usernames must be at least 3 characters long");
	}
	var regAll = /^[A-Za-z0-9-_]+$/;
	if(username.search(regAll) == -1 && username.length != 0){
	clientErrors.push("Usernames may only contain letters, digits, and underscores");
	}
	if (password1.length < 8){
		clientErrors.push("Passwords must be at least 8 characters long");
	}
	var regLet = /^[A-Za-z]+$/;
	var regNum = /^[0-9]+$/;
	if (password1.search(regLet) == false || password1.search(regNum) == false || password1.length == 0){
		clientErrors.push("Passwords must contain at least one letter and one number");
	}
	if (regAll.test(password1) == false && password1.length != 0){
		clientErrors.push("Passwords may only contain letters, digits, and underscores");
	}
	if (password1 != password2){
		clientErrors.push("Passwords do not match");
	}
	var regEmail = /[A-Za-z0-9-_%+-]+@[A-Za-z0-9.-]+.[A-Z]{2,10}/igm;
	if(regEmail.test(email) == false || email.length == 0){
		clientErrors.push("Email address must be valid");
	}
	if(username.length > 20){
		clientErrors.push("Username must be no longer than 20 characters");
	}
	if(password1.length > 20){
		clientErrors.push("Password must be no longer than 20 characters");
	}
	if(firstname.length > 20){
		clientErrors.push("Firstname must be no longer than 20 characters");
	}
	if(lastname.length > 20){
		clientErrors.push("Lastname must be no longer than 20 characters");
	}
	if(email.length > 40){
		clientErrors.push("Email must be no longer than 40 characters");
	}
	var div = document.getElementById("errors");
	if (clientErrors.length > 0){
			var error1 = document.createElement("p");
			error1.class = "error";
			error1.id = "error1";
			for(var i = 0; i < clientErrors.length; i++)
			{
				error1.innerHTML += clientErrors[i] + "<br><br>";
			}
			div.appendChild(error1);
	}
	else{
	var req = new XMLHttpRequest();
	req.open("POST", '/api/v1/user', true);
	req.setRequestHeader("Content-type", "application/json");
	
	var show_errors = function() {
		if (called == 0){
			var errorList = JSON.parse(req.response);
			var errText = errorList.errors;
			var errLength = errText.length;
			
			if (errLength ==  0) {
				window.location="http://localhost:3000/fcda9697ef8a4a3aac8d/pa3/login";
			}
			else{
				var error2 = document.createElement("p");
				error2.class = "error";
				error2.id = "error2";
				for(var i = 0; i < errLength; i++)
				{
					error2.innerHTML += errText[i].message + "<br><br>";
				}
				called = 1;
				div.appendChild(error2);
			}
		}

		
	}//end show errors
	req.onreadystatechange = show_errors;
	req.send(userInfo);
	}	
}


