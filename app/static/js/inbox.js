$("#sendmessage").click(function(){
  //location.reload();
});

$("#showcompose").click(function(){
  $("#hide").toggle();
});

$("#report").click(function(){
  $("#hide2").toggle();
});

$('#sendTomessage').on('click', function(e) {
      var user =  $(this).attr("name")
      var recipient = document.getElementById("recipient").value;
      var message = document.getElementById("composeMessage").value;
      $.ajax({ 
        contentType: "charset=utf-8",
        url: '/sendto', 
        type: 'POST', 
        data: {'user': user, 'recipient': recipient, 'message': message},
        success: function(json) {
          if(!json.error) location.reload();
        }
      })
    });

$(document).ready( function () {
  $("div.msg-wrap").scrollTop($("div.msg-wrap").prop("scrollHeight"))
});
