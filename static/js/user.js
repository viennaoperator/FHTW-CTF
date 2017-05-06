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
      url: '/listMyAvailableChallenges', //this is the submit URL
      type: 'GET',
      dataType: 'json',
      success: function(data){
        successMessage("Sucessfully loaded challenges");
        availableChallenges = data;
        loadStartedChallenges();
      },
      error: function (xhr, ajaxOptions, thrownError){
        errorMessage(thrownError);
      }
  });
}

function loadStartedChallenges(){
  $.ajax({
      url: '/listMyRunningChallenges', //this is the submit URL
      type: 'GET',
      dataType: 'json',
      success: function(data){
        startedChallenges = data;
        //after successfully loaded the challenges --> display them
        displayChallenges();
      },
      error: function (xhr, ajaxOptions, thrownError){
        errorMessage(thrownError);
      }
  });
}

//check if the challenge is available for pentesting
function checkAvailablity(){
  $( ".starting" ).each(function() {
    //extract id from div
    checkAvailabe($(this).attr('id'));
  });
}

function displayChallenges(){
  $("#challengesRow").html("");

  //display all available challenges
  for (var i = 0, len = availableChallenges.length; i < len; i++) {
      displayChallenge(availableChallenges[i]);
  }

  //look for already started challenges and mark them as started within the GUI
  for (var i = 0, len = startedChallenges.length; i < len; i++) {
    markChallengeAsStarted(startedChallenges[i]);
  }

  //checks availability of every started challenge
  checkAvailablity();
  //when everything is finished we add jquery functions
  $('.challenge').matchHeight();
}

function giveButtonsFunction(){
  $( ".btn-outlined" ).click(function(){
    var challenge = $(this).parent().parent();
    var challengeClass = challenge.attr("class");
    var challengeId = challenge.attr("id");

    console.log(challengeClass);
    if (challengeClass.includes("stopped")){
      startChallenge(challengeId);
    }
    else if (challengeClass.includes("starting")){
      stopChallenge(challengeId);
    }
    else if (challengeClass.includes("started")){
      stopChallenge(challengeId);
    }
    else {
      console.log("No proper class found!");
    }
  });
}

function displayChallenge(challenge){
  var html = "<div id='"+challenge.challengeid+"'class='col-sm-4 text-center challenge stopped'>" +
             "<p><h3>" + challenge.name + "</h3></p>" +
             "<p>" + challenge.description + "</p>" +
             "<p><button class='btn-outlined'>Start</button></p>" +
             "</div>";
  $("#challengesRow").append(html);
  giveButtonsFunction();
}

function markChallengeAsStarted(challenge){
  $("#" + challenge.chal).html("");
  var html = "<p><h3>" + challenge.name + "</h3></p>" +
             "<p>" + challenge.description + "</p>" +
             "<p><span class='glyphicon glyphicon-refresh glyphicon-spin'></span> Waiting for startup</p>" +
             "<p><button class='btn-outlined'>Terminate</button></p>";
  $("#" + challenge.chal).removeClass("stopped");
  $("#" + challenge.chal).addClass("starting");
  $("#" + challenge.chal).html(html);
  giveButtonsFunction();
}

function markChallengesAsAvailable(challenge){
    $("#" + challenge.chal).html("");
    var html = "<p><h3>" + challenge.name + "</h3></p>" +
               "<p>" + challenge.description + "</p>" +
               "<a href='http://"+urlFromPythonConfig+":" + challenge.port + "' " +
               "target='_blank'> GO TO CHALLENGE</a></p>" +
               "<p><button class='btn-outlined'>Stop</button></p>";
    $("#" + challenge.chal).removeClass("starting");
    $("#" + challenge.chal).removeClass("stopped");
    $("#" + challenge.chal).addClass("started");
    $("#" + challenge.chal).html(html);
    giveButtonsFunction();
}

function startChallenge(id){
  infoMessage("Starting challenge...")
  $.ajax({
      url: '/startChallenge/' + id, //this is the submit URL
      type: 'GET',
      success: function(data){
        successMessage("Successful started...");
        refreshChallenges();
      },
      error: function (xhr, ajaxOptions, thrownError){
        errorMessage(thrownError);
      }
  });
}

function stopChallenge(id){
  infoMessage("Stopping challenge...")
  $.ajax({
      url:'/stopChallenge/' + id, //this is the submit URL
      type: 'GET',
      success: function(data){
        successMessage("Successful stopped...");
        refreshChallenges();
      },
      error: function (xhr, ajaxOptions, thrownError){
        errorMessage(thrownError);
      }
  });
}

//service, checks availability of container and then marks them as available in GUI
function checkAvailabe(runningchallengeid){
  $.ajax({
      url: '/checkAvailable/' + runningchallengeid, //this is the submit URL
      type: 'GET',
      dataType: 'json',
      success: function(data){
        markChallengesAsAvailable(data);
      }
  });
}

//on body load
$(function() {
  refreshChallenges();

  $("#refresh").click(function(){
    refreshChallenges();
  });
});

//Constantly check, if there's an update
setInterval(function() {
  checkAvailablity();
}, 15000);
