$(function() {
    $(document).on('click', '#addToCart', function(e) {
      var id =  $(this).attr("name")
      $.ajax({ 
        contentType: "charset=utf-8",
        url: '/addToCart', 
        type: 'POST', 
        data: {'id': id},
        success: function() {
          location.reload();
        }
      })
    });
});

$(function() {
    $(document).on('click', '#removeFromCart', function(e) {
      var id =  $(this).attr("name")
      $.ajax({ 
        contentType: "charset=utf-8",
        url: '/removeFromCart', 
        type: 'POST', 
        data: {'id': id},
        success: function() {
          location.reload();
        }
      })
    });
});
