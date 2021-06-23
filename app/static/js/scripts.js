/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function updateNav() {
  var x = document.getElementById("sidebar");
  if (x.className === "side-navbar") {
    x.className += " responsive";
  } else {
    x.className = "side-navbar";
  }
}

$("#roleSelect").change(function() {
  if ($(this).val() == "sponsor") {
    $('#sponsorid').hide();
    $('#sponsorid').removeAttr('required');
    $('#sponsorid').removeAttr('data-error');
    $('#title').show();
    $('#title').attr('required', '');
    $('#title').attr('data-error', 'This field is required.');
  }else if ($(this).val() == "driver") {
    $('#title').hide();
    $('#title').removeAttr('required');
    $('#title').removeAttr('data-error');
    $('#sponsorid').show();
  } else {
    $('#sponsorid').hide();
    $('#sponsorid').removeAttr('required');
    $('#sponsorid').removeAttr('data-error');
    $('#title').hide();
    $('#title').removeAttr('required');
    $('#title').removeAttr('data-error');
  }
});

// Suspend User
$(function() {
  $(document).on('click', '#suspend', function(e) {
    var user =  $(this).attr("name")
    $.ajax({ 
      contentType: "charset=utf-8",
      dataType: 'json',
      url: '/suspend', 
      type: 'POST', 
      data: user,
      success:finished
    })
  });
});

// Unsuspend User
$(function() {
  $(document).on('click', '#unsuspend', function(e) {
    var user =  $(this).attr("name")
    $.ajax({ 
      contentType: "charset=utf-8",
      url: '/unsuspend', 
      type: 'POST', 
      data: user
    })
  });
});

// Remove user
$(function() {
  $(document).on('click', '#remove', function(e) {
    var user =  $(this).attr("name")
    $.ajax({ 
      contentType: "charset=utf-8",
      url: '/remove', 
      type: 'POST', 
      data: user
    })
  });
});

// Reactivate user
$(function() {
  $(document).on('click', '#reactivate', function(e) {
    var user =  $(this).attr("name")
    $.ajax({ 
      contentType: "charset=utf-8",
      url: '/reactivate', 
      type: 'POST', 
      data: user
    })
  });
});

// Remove user from sponsor
$(function() {
  $(document).on('click', '#removeFromSponsor', function(e) {
    var user =  $(this).attr("name")
    var sponsor = $(this).attr('class');
    $.ajax({ 
      contentType: "charset=utf-8",
      url: '/removeFromSponsor', 
      type: 'POST', 
      data:{'user': user, 'sponsor': sponsor}
    })
  });
});

// Add points
$(function() {
  $(document).on('click', '#addpoints', function(e) {
    var user =  $(this).attr("name")
    var sponsor = $(this).attr('class');
    var points = document.getElementById("addpoints" + user + sponsor).value;
    $.ajax({ 
      contentType: "application/x-www-form-urlencoded",
      url: '/addpts', 
      type: 'POST', 
      data:{'user': user, 'points': points, 'sponsor': sponsor}
    })
  });
});

// Add points
$('.addpt').on('click', function(e) {
    console.log(this.dataset);
    var user =  $(this).attr("name");
    var sponsor = this.dataset.sponsor;
    var points = document.getElementById("addpoints" + user + sponsor).value;
    $.ajax({ 
      contentType: "application/x-www-form-urlencoded",
      url: '/addpts', 
      type: 'POST', 
      data:{'user': user, 'points': points, 'sponsor': sponsor},
      success: finished
    })
  });

// reject application
$(function() {
  $(document).on('click', '#rejectapp', function(e) {
    var user =  $(this).attr("name")
    var sponsor = $(this).attr('class');
    $.ajax({ 
      contentType: "application/x-www-form-urlencoded",
      url: '/rejectapp', 
      type: 'POST', 
      data:{'user': user, 'sponsor': sponsor}
    })
  });
});

// accept application
$(function() {
  $(document).on('click', '#acceptapp', function(e) {
    var user =  $(this).attr("name")
    var sponsor = $(this).attr('class');
    $.ajax({ 
      contentType: "application/x-www-form-urlencoded",
      url: '/acceptapp', 
      type: 'POST', 
      data:{'user': user, 'sponsor': sponsor}
    })
  });
});

// send message
$(function() {
  $(document).on('click', '#sendmessage', function(e) {
    var user =  $(this).attr("name")
    var sender = $(this).attr('class');
    var message = document.getElementById("sendmessage" + user + sender).value;
    $.ajax({ 
      contentType: "application/x-www-form-urlencoded",
      url: '/sendmessage', 
      type: 'POST', 
      data:{'user': user, 'sender': sender, 'message': message}
    })
  });
});

// cancel order
$(function() {
  $(document).on('click', '#cancelOrder', function(e) {
    var order =  $(this).attr("name")
    $.ajax({ 
      contentType: "charset=utf-8",
      url: '/cancelOrder', 
      type: 'POST', 
      data: order,
      success: finished
    })
  });
});

// Theme code
$("#themeSelect").change(function() {
  if ($(this).val() == "dark") {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme4');
    document.cookie = 'theme=dark'
  } else if ($(this).val() == "red") {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme4');
    document.cookie = 'theme=red'
  } else if ($(this).val() == "clemson") {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme4');
    document.cookie = 'theme=clemson'
    var aud = new Audio('/static/sounds/Tiger_Rag.mp3');
    aud.volume = 0.3;
    aud.play();
  } else if ($(this).val() == "seizure") {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme4');
    document.cookie = 'theme=seizure'
  } else {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme4');
    document.cookie = 'theme=light'
  }
  document.documentElement.style.setProperty('--main-theme1', color1);
  document.documentElement.style.setProperty('--main-theme2', color2);
  document.documentElement.style.setProperty('--main-theme3', color3);
  document.documentElement.style.setProperty('--main-theme4', color4);
});

function setThemeFromCookie() {
  if (document.cookie.match(/theme=dark/i) != null) {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--dark-theme4');
  } else if (document.cookie.match(/theme=red/i) != null) {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--red-theme4');
  } else if (document.cookie.match(/theme=clemson/i) != null) {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--clemson-theme4');
  } else if (document.cookie.match(/theme=seizure/i) != null) {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme1');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--seizure-theme4');
  } else {
    var color1 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme');
    var color2 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme2');
    var color3 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme3');
    var color4 = getComputedStyle(document.documentElement).getPropertyValue('--blue-theme4');
  }
  document.documentElement.style.setProperty('--main-theme1', color1);
  document.documentElement.style.setProperty('--main-theme2', color2);
  document.documentElement.style.setProperty('--main-theme3', color3);
  document.documentElement.style.setProperty('--main-theme4', color4);
}

jQuery(function() {
  jQuery('#sponsorSelect').change(function() {
      this.form.submit();
  });
});

// Fix URL and add theme
$(document).ready(function(){
	var uri = window.location.toString();
	if (uri.indexOf("?") > 0) {
	    var clean_uri = uri.substring(0, uri.indexOf("?"));
	    window.history.replaceState({}, document.title, clean_uri);
  }
  setThemeFromCookie()
});




// updateAccount JS
var finished = function(response) {
    console.log("Hot dog");
    console.log(response);
    window.location.reload();
};
var accUpdatePath = "/updateAccount/";
$('#update-email').on('click', function(e) {
        var driver = document.getElementById("username").innerText;
        var email = document.getElementById("email").value;
        var arr = {'email': email};
        var aj = $.ajax({
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            url: accUpdatePath + driver,
            type: 'POST',
            data: JSON.stringify(arr),
            success: finished
        });
});
// Update user names
$('#update-names').on('click', function(e) {
        var driver = document.getElementById("username").innerText;
        var first_name = document.getElementById("first_name").value;
        var mid_name = document.getElementById("mid_name").value;
        var last_name = document.getElementById("last_name").value;
        var arr = {'first_name': first_name, 'mid_name': mid_name,
                   'last_name': last_name};
        $.ajax({
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            url: accUpdatePath + driver,
            type: 'POST',
            data: JSON.stringify(arr),
            success: finished
        })
});
// Update address
$('#update-address').on('click', function(e) {
        var driver = document.getElementById("username").innerText;
        var address = document.getElementById("address").value;
        var arr = {'address': address};
        $.ajax({
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            url: accUpdatePath + driver,
            type: 'POST',
            data: JSON.stringify(arr),
            success: finished
        })
});
// Update phone number
$('#update-phone').on('click', function(e) {
        var driver = document.getElementById("username").innerText;
        var phone = document.getElementById("phone").value;
        var arr = {'phone': phone};
        $.ajax({
            contentType: "application/json; charset=utf-8",
            dataType: 'json',
            url: accUpdatePath + driver,
            type: 'POST',
            data: JSON.stringify(arr),
            success: finished
        })
});
// Update user password
$("#update-password").click(function() {
    var driver = document.getElementById("username").innerText;
    var pwd = document.getElementById("pwd").value;
    var conf = document.getElementById("confirm").value;
    var arr = {'pwd': pwd};
    if( pwd !== conf ) {
        console.log("Passwords do not match!");
        return;
    }

    $.ajax({
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: accUpdatePath + driver,
        type: 'POST',
        data: JSON.stringify(arr),
        success: finished
    });
});
// Add to sponsor
$("#add-sponsor").click(function() {
  var driver = document.getElementById("username").innerText;
  var sponsor = document.getElementById("sponsor").value;
  var arr = {'sponsor': sponsor};
  $.ajax({
      contentType: "application/json; charset=utf-8",
      dataType: 'json',
      url: accUpdatePath + driver,
      type: 'POST',
      data: JSON.stringify(arr),
      success: document.getElementById('sponsor').value = ''
  })
});
// Admin and sponsor sorting routines
var sort_by_name = (a,b) => {
        return $(a).attr('name').localeCompare($(b).attr('name'));
};
var sort_by_price = (a,b) => {
    var ap = $(a).data('price');
    var bp = $(b).data('price');
    return (ap > bp) ? 1 : (ap == bp) ? 0 : -1;
};

// Sort items
$("#sort").on('input',() => {
    var type = $("#sort option:selected").text();
    var list = $(".row .one-third .card");
    if (type == 'Price') {
        list.sort(sort_by_price);
    }
    else if (type == 'Name') {
        list.sort(sort_by_name);
    }
    else {
        
    }
    var results = $('#results');
    var i = 0;
    results.children().each((index, elem) => {
        $(elem).children('.one-third').each((index, e) => {
            $(e).append(list[i++]);
        });
    });
});

function searchAccs() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchaccs");
  filter = input.value.toUpperCase();
  table = document.getElementById("accounts");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[2];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i-1].style.display = "";
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
    else {
      tr[i].style.display = "none";
    }
  }
}
