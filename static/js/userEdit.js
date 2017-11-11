"use strict";
function pullData(){
	var req = new XMLHttpRequest();
	var updateFields = function() {
		if(req.readyState == 4) {
			var infoList = JSON.parse(req.response);
			var firstname = infoList.firstname;
			var lastname = infoList.lastname;
			var email = infoList.email;
			document.getElementById("update_firstname_input").value = firstname;
			document.getElementById("update_lastname_input").value = lastname;
			document.getElementById("update_email_input").value = email;
			}
	}
	req.onreadystatechange = updateFields;
	req.open("GET", '/api/v1/user', true);
	req.setRequestHeader("Content-type", "application/json");
	req.send();
}

function checkData(userInfo) {
	var div = document.getElementById("errors");
	div.innerHTML = "";
	var clientVer = userInfo;
	var userInfo = JSON.stringify(userInfo);
	
	//Client-Side Validation
	var firstname = clientVer.firstname;
	var lastname = clientVer.lastname;
	var password1 = clientVer.password1;
	var password2 = clientVer.password2;
	var email = clientVer.email;
	
	var clientErrors = [];
	
	var regAll = /^[A-Za-z0-9-_]+$/;
	var regLet = /^[A-Za-z]+$/;
	var regNum = /^[0-9]+$/;
	
	if (password1.length != 0 || password2.length != 0){
	
		if (password1.length < 8){
			clientErrors.push("Passwords must be at least 8 characters long");
		}
		if (password1.search(regLet) == false || password1.search(regNum) == false){
			clientErrors.push("Passwords must contain at least one letter and one number");
		}
		if (regAll.test(password1) == false){
			clientErrors.push("Passwords may only contain letters, digits, and underscores");
		}
		if (password1 != password2){
			clientErrors.push("Passwords do not match");
		}
	}
	var regEmail = /[A-Za-z0-9-_%+-]+@[A-Za-z0-9.-]+.[A-Z]{2,10}/igm;
	if(regEmail.test(email) == false || email.length == 0){
		clientErrors.push("Email address must be valid");
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
	//end client error checks
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
	req.open("PUT", '/api/v1/user', true);
	req.setRequestHeader("Content-type", "application/json");
	
	var show_errors = function() {
		if (req.readyState == 4){
			var errorList = JSON.parse(req.response);
			var errText = errorList.errors;
			var errLength = errText.length;
			if (errLength > 0) {
				var error2 = document.createElement("p");
				error2.class = "error";
				error2.id = "error2";
				for(var i = 0; i < errLength; i++)
				{
					error2.innerHTML += errText[i] + "<br><br>";
				}
				div.appendChild(error2);
			}
		}
	}//end show errors
	req.onreadystatechange = show_errors;
	req.send(userInfo);
	}	
}


