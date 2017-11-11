function login() {
	var req = new XMLHttpRequest();
	var callBack = function() {
		if (req.readyState === 4) {
			if (req.status != 200) {
				var loginDiv = document.getElementById("error_msg_div");
				loginDiv.innerHTML = "";
				var loginError = document.createElement("p");
				loginError.id = "login_error";
				loginError.class = "error";
				var errorList = JSON.parse(req.response).errors;
				for (var x = 0; x < errorList.length; x++) {
					loginError.innerHTML += errorList[x].message + "<br>";
				}
				loginDiv.appendChild(loginError);
			}
			else {
				var urlQuery = window.location.href.split("?")[1];
				if (urlQuery == "") {					
					window.location.assign(urlQuery);	
				}
				else {
					window.location.assign("/fcda9697ef8a4a3aac8d/pa3/");
				}
			}
		}
	};
