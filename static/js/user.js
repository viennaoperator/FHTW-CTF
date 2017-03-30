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

var availableChallenges = [], startedChallenges = [];

function refreshChallenges(){
  infoMessage("loading challenges...")
  $.ajax({
      url: 'http://localhost:5000/listMyAvailableChallenges', //this is the submit URL
      type: 'GET',
      dataType: 'json',
      success: function(data){
        successMessage("Sucessfully loaded challenges");
        availableChallenges = data;
        loadStartedChallenges();
        displayAvailableChallenges();
      },
      error: function (xhr, ajaxOptions, thrownError){
        console.log(xhr);
        console.log(ajaxOptions);
        console.log(thrownError);
        errorMessage(thrownError);
      }
  });
}

function loadStartedChallenges(){
  $.ajax({
      url: 'http://localhost:5000/listMyRunningChallenges', //this is the submit URL
      type: 'GET',
      dataType: 'json',
      success: function(data){
        startedChallenges = data;
        console.log(startedChallenges);
      },
      error: function (xhr, ajaxOptions, thrownError){
        console.log(xhr);
        console.log(ajaxOptions);
        console.log(thrownError);
        errorMessage(thrownError);
      }
  });
}

function displayAvailableChallenges(){
  $("#challengesRow").html("");
  for (var i = 0, len = availableChallenges.length; i < len; i++) {
    var html = "<div id='"+availableChallenges[i].challengeid+"'class='col-sm-4 text-center challenge stopped'>" +
               "<p><h3>" + availableChallenges[i].name + "</h3></p>" +
               "<p>" + availableChallenges[i].description + "</p>" +
               "<p><button class='btn-outlined'>Start</button></p>" +
               "</div>";
    $("#challengesRow").append(html);
  }

  $( ".btn-outlined" ).click(function(){
    console.log($(this).parent().parent());
  });
}

function startChallenge(id){
  infoMessage("Starting challenge...")
  $.ajax({
      url: 'http://localhost:5000/startChallenge/' + id, //this is the submit URL
      type: 'GET',
      dataType: 'json',
      success: function(data){
        infoMessage("Successful started...");
      },
      error: function (xhr, ajaxOptions, thrownError){
        console.log(xhr);
        console.log(ajaxOptions);
        console.log(thrownError);
        errorMessage(thrownError);
      }
  });
}

$(function() {
  refreshChallenges();
  $('.challenge').matchHeight();

  $("#refresh").click(function(){
    refreshChallenges();
    $('.challenge').matchHeight();
  });
});
