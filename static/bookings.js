$( document ).on("blur, change", "#ref, #mod", function() {
    // grab value
    var email = $("#ref").val();
    var mod = $("#mod").val();
		var dataString = $("#retrieveCaseForm").serialize();

    // send value via POST to URL /<department_id>
    var get_request = $.ajax({
      type: 'GET',
			data: dataString,
      url: '/coursesfor/' + email + '&' + mod + '/'
    });

    // handle response
    get_request.done(function(data){

    // data
    // add values to list 
    var option_list = [["", "<Select a course>"]].concat(data);
    $("#course_select").empty();
      for (var i = 0; i < option_list.length; i++) {
        $("#course_select").append(
          $("<option></option>").attr("value", option_list[i][0]).text(option_list[i][1]));
      }
      $("#course_select").show();
    });
});
