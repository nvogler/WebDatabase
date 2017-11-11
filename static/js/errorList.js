function errorList(data){
	$.post(
		"/api/v1/user",
		{ data: $("input").val() },
		function(error, status){
			$("#errors").text(error);
			}
		);
}
