function successMessage(message){
  $("#alert_template_success").html(message);
  $('#alert_template_success').fadeIn('slow');
  $('#alert_template_success').delay(5000).fadeOut(400);
}

function errorMessage(message){
  $("#alert_template_error").html(message);
  $('#alert_template_error').fadeIn('slow');
  $('#alert_template_error').delay(8000).fadeOut(400);
}

function infoMessage(message){
  $("#alert_template_info").html(message);
  $('#alert_template_info').fadeIn('slow');
  $('#alert_template_info').delay(3000).fadeOut(400);
}

$(function() {
	$('.challenge').matchHeight();
});
