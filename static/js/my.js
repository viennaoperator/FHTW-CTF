//Design Functions
$("#stop").hide()

$(".admin-menu").click(function(){
  $("#stop").hide()
  $('#resultTable').bootstrapTable('destroy');
  $(".admin-menu").removeClass( "admin-menu-hover");
  $(this).addClass( "admin-menu-hover" );
})

function successMessage(message){
  $("#alert_template_success").html(message);
  $('#alert_template_success').fadeIn('slow');
  $('#alert_template_success').delay(4000).fadeOut(400);
}

function errorMessage(message){
  $("#alert_template_error").html(message);
  $('#alert_template_error').fadeIn('slow');
  $('#alert_template_error').delay(8000).fadeOut(400);
}
//Design Functions END

//ADD Functionality
$(function(){
    $('#challenge-form').on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: 'http://localhost:5000/addChallenge', //this is the submit URL
            type: 'GET', //or POST
            data: $('#challenge-form').serialize(),
            success: function(data){
              successMessage("Sucessfully added challenge");
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

$("#listAllDockerChallenges").click(function(){
    $.ajax({
      url: "http://localhost:5000/listAllDockerChallenges",
      dataType: 'json',
      success: function(result){
        $('#resultTable').bootstrapTable('destroy');
        $('#resultTable').bootstrapTable({
            columns: [{
                field: 'dockerchallengeID',
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
            if(result) startChallenge(row.dockerchallengeID); // confirmed
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
  $.ajax({
    url: "http://localhost:5000/startChallenge/" + id,
    dataType: 'json',
    success: function(result){
      successMessage("started one container on port: " + result.port);
    }
    });
}

function removeChallenge(id){
  $.ajax({
    url: "http://localhost:5000/removeDockerChallenge/" + id,
    dataType: 'json',
    success: function(result){
      successMessage("started one container on port: " + result.port);
    }
    });
}

$("#listAllRunningContainer").click(function(){
    $.ajax({
      url: "http://localhost:5000/listAllRunningContainer",
      dataType: 'json',
      success: function(result){
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
  var ids = getIdSelections();
  console.log(ids);
  for (var id in ids){
    $.ajax({
      url: "http://localhost:5000/stopChallengeContainer/" + ids[id],
      success: function(result){
        successMessage("Challenge with id: " + id + "stopped");
        console.log("Challenge with id: " + id + "stopped");
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
    $.ajax({
      url: "http://localhost:5000/stopAndRemoveAllContainer",
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
});
