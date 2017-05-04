//Design Functions
$("#stop").hide();

$(".admin-menu").click(function(){
  $("#stop").hide()
  $('#resultTable').bootstrapTable('destroy');
  $(".admin-menu").removeClass( "admin-menu-hover");
  $(this).addClass( "admin-menu-hover" );
})

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

//Design Functions END

//ADD Functionality
$(function(){
    $('#challenge-form').on('submit', function(e){
        e.preventDefault();
        infoMessage("Trying to add your challenge...");
        $.ajax({
            url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig +  '/addChallenge', //this is the submit URL
            type: 'GET', //or POST
            data: $('#challenge-form').serialize(),
            success: function(data){
              successMessage("Sucessfully added challenge");
              $('#myModal').modal('hide');
              $("#myModal .modal-body input").val("");
              $("#myModal .modal-body textarea").val("");
            },
            error: function (xhr, ajaxOptions, thrownError){
              console.log(xhr);
              console.log(ajaxOptions);
              console.log(thrownError);
              errorMessage(thrownError);
            }
        });
    });
});

//check if name is alphanumeric
$("#challengeName").keyup(function(){
  if (/^[a-z0-9]+$/i.test($(this).val())) {
    $("#challengeNameDiv").removeClass("has-error");
  }
  else {
    $("#challengeNameDiv").addClass("has-error");
  }
});

//ADD Function END
$("#listAllDockerChallenges").click(function(){
    $.ajax({
      url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig + '/listAllDockerChallenges',
      dataType: 'json',
      success: function(result){
        $('#resultTable').bootstrapTable('destroy');
        $('#resultTable').bootstrapTable({
            columns: [{
                field: 'id',
                title: 'ID'
            }, {
                field: 'name',
                title: 'Challenge Name'
            }, {
                field: 'description',
                title: 'Description'
            }, {
                field: 'value',
                title: 'Value'
            },{
                field: 'hidden',
                title: 'Hidden'
            },{
                field: 'path',
                title: 'Path'
            },{
                field: 'operate',
                title: 'Item Operate',
                align: 'center',
                events: operateEvents,
                formatter: operateFormatter
            }
            ],
            data: result
        });

    }});
});

function operateFormatter(value, row, index) {
        return [
            '<a class="start" href="javascript:void(0)" title="Start">',
            '<i class="glyphicon glyphicon-play"></i>',
            '</a>  ',
            '<a class="remove" href="javascript:void(0)" title="Remove">',
            '<i class="glyphicon glyphicon-remove"></i>',
            '</a>'
        ].join('');
    }
    window.operateEvents = {
        'click .start': function(e, value, row, index){
          bootbox.confirm("Do you really want to start this challenge?",
          function(result){ /* your callback code */
            if(result) startChallenge(row.id); // confirmed
          });
        },
        'click .remove': function (e, value, row, index) {
          bootbox.confirm("Do you really want to remove this challenge?",
          function(result){
            if(result){
              removeChallenge(row.dockerchallengeID);
              $("#resultTable").bootstrapTable('remove', {
                    field: 'id',
                    values: [row.id]
              });
            }
          });
        }
    };

function startChallenge(id){
  infoMessage("Trying to start challenge " + id);
  $.ajax({
    url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig + '/startChallenge/' + id,
    dataType: 'json',
    success: function(result){
      successMessage("started one container on port: " + result.port);
    },
    error: function (xhr, ajaxOptions, thrownError){
      errorMessage("container couldn't be started");
    }
    });
}

function removeChallenge(id){
  infoMessage("Trying to remove challenge " + id)
  $.ajax({
    url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig + '/removeDockerChallenge/' + id,
    success: function(result){
      successMessage("challenge removed");
    },
    error: function (xhr, ajaxOptions, thrownError){
      errorMessage("container couldn't be removed");
    }
    });
}

$("#listAllRunningContainer").click(function(){
    $.ajax({
      url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig + '/listAllRunningContainer',
      dataType: 'json',
      success: function(result){
        console.log(result);
        $("#stop").show()
        $('#resultTable').bootstrapTable('destroy');
        $('#resultTable').bootstrapTable({
            columns: [
              {
                field : 'state',
                checkbox: true
              },
            {
                field: 'id',
                title: 'Challenge ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'name',
                title: 'Challenge Name',
                align: 'center',
                valign: 'middle',
                sortable: true,
            }, {
                field: 'port',
                title: 'Port',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'teamid',
                title: 'Team ID',
                align: 'center',
                valign: 'middle',
                sortable: true,
            },{
                field: 'flag',
                title: 'Flag'
            },{
                field: 'startDate',
                title: 'Container Start'
            },
            {
                field: 'path',
                title: 'OS Path'
            }
            ],
            data: result
        });
    }});
});

//stop selected containers
$("#stop").click(function () {
  infoMessage("Trying to stop selected challenges...");
  var ids = getIdSelections();
  console.log(ids);
  for (var id in ids){
    $.ajax({
      url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig + '/stopChallengeContainer/' + ids[id],
      success: function(result){
        successMessage("Challenge stopped");
        console.log("Challenge stopped");
      }
      });
  }

  $("#resultTable").bootstrapTable('remove', {
                      field: 'id',
                      values: ids
           });
  $("#stop").prop('disabled', true);
});

//get selected items from table
function getIdSelections() {
  return $.map($('#resultTable').bootstrapTable('getSelections'), function (row) {
    return row.id
  });
}

$("#stopAndRemoveAllContainer").click(function (){
  bootbox.confirm("Do you really want to stop and remove all challenges?",
  function(result){ /* your callback code */
    if(result) {
      infoMessage("Trying to stop and remove all challenges ");
      $.ajax({
        url: 'http://' + urlFromPythonConfig + ':' + portFromPythonConfig + '/stopAndRemoveAllContainer',
        success: function(result){
          successMessage("All Container stopped & removed!");
        },
        error: function (xhr, ajaxOptions, thrownError){
          console.log(xhr);
          console.log(ajaxOptions);
          console.log(thrownError);
          errorMessage("container couldn't be stopped & removed");
        }
      });
    }
  });
});
