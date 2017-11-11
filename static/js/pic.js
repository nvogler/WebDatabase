"use strict";

function picGet(picid) {
	var req = new XMLHttpRequest();
	var callBack = function() {
		if (req.readyState === 4) {
			var div = document.getElementById("content");
			if (req.status == 200) {
				// talking to user_api
				var userBack = false;
				var albumBack = false;
				var albumid = JSON.parse(req.response).albumid;
				var user;
				var userReq = new XMLHttpRequest();
				userReq.onreadystatechange = function() {
					if (userReq.readyState === 4) {
						if (userReq.status == 200) {
							user = JSON.parse(userReq.response).username;
						}
						userBack = true;
					}
				}
				userReq.open("GET", '/api/v1/user/', true);
				userReq.setRequestHeader("Content-type", "application/json");
				userReq.send();
				// talking to album api
				var owner;
				var albumReq = new XMLHttpRequest();
				albumReq.onreadystatechange = function() {
					if (albumReq.readyState === 4) {
						if (albumReq.status == 200) {
							owner = JSON.parse(albumReq.response).username;
						}
						albumBack = true;
					}
				}
				albumReq.open("GET", '/api/v1/album/'+albumid, true);
				albumReq.setRequestHeader("Content-type", "application/json");
				albumReq.send();
				
				// if the request returned, edit the DOM of HTML
				if (userBack && albumBack) {
					
					div.innerHTML = "";
					var img = document.createElement("img");
					var picid = JSON.parse(req.response).picid;
					var format = JSON.parse(req.response).format;
					var caption = JSON.parse(req.response).caption;
					var next = JSON.parse(req.response).next;
					var prev = JSON.parse(req.response).prev;
					img.src = "/static/images/" + picid + "." + format;
					img.align = "center";
					if (user === owner && user != undefined) {
						var cap = document.createElement("form");
						cap.value = caption;
						cap.onkeypress = function(e) {
							// user press enter
							if (e.keyCode == 13) {
								// picPut(picid)
							}
						}
					}
					else {
						var cap = document.createElement("p");
						cap.innerHTML = caption;
					}
					cap.align = "center";
					cap.id = "pic_"+picid+"_caption";
					var navBar = document.createElement("nav");
					navBar.class = "navbar navbar-default navbar-fixed-bottom";
					navBar.align = "center";
					var prevBtn = document.createElement("button");
					prevBtn.type = "button";
					prevBtn.class = "btn btn-info";
					prevBtn.id = "prev_pic";
					prevBtn.onkeypress = "picGet("+prev+")";
					var nextBtn = document.createElement("button");
					nextBtn.type = "button";
					nextBtn.class = "btn btn-info";
					nextBtn.id = "next_pic";
					nextBtn.onkeypress = "picGet("+next+")";
					navBar.appendChild(prevBtn);
					navBar.appendChild(nextBtn);
					
					div.appendChild(img);
					div.appendChild(cap);
					div.appendChild(navBar);
				}
			}
			else {
				div.innerHTML = "";
				var errorP = document.createElement("p");
				errorP.class = "error";
				var errorObj = JSON.parse(req.response).errors[0];
				console.log(errorObj['message']);
				errorP.innerHTML = errorObj['message'];
				div.appendChild(errorP);
		}
	};
	var picid = window.location.href.split("id=")[1];
	req.onreadystatechange = callBack;
	req.open("GET", '/api/v1/pic/'+picid, true);
	req.setRequestHeader("Content-type", "application/json");
	req.send();
}

function picPut(jsonObj) {
	var req = new XMLHttpRequest();
	var callBack = function() {
		if (req.readyState === 4) {
			if (req.status != 200) {
				var div = document.getElementById("content");
				var errorP = document.createElement("p");
				errorP.class = "error";
				var errorObj = JSON.parse(req.response).errors[0];
				console.log(errorObj['message']);
				errorP.innerHTML = errorObj['message'];
				div.appendChild(errorP);
			}
		}
	}
	req.onreadystatechange = callBack;
	req.open("PUT", '/api/v1/pic/'+picid, true);
	req.setRequestHeader("Content-type", "application/json");
	req.send(jsonObj);
}