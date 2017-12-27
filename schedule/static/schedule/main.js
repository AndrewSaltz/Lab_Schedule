
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
$( document ).ready(function() {
      var count = 0;
      console.log( 'ready!' + count ); //Sanity check
      $( 'button' ).click(function() {
        console.log( 'we clicked!' ); // Sanity Check II
        var pk = this.id
        var button = $(this)
        var user = $( 'button' ).attr("user")
        var user_name = document.getElementById("username").innerHTML
        console.log( pk, user) // Sanity Check III
        console.log("user name ", user_name)
        $.ajax({
            url: "/reserve/",
            type: "POST",       //Send the info to reserve view
            data: { pk : pk},
            success: function(data) {
                var number = JSON.parse(data);
                console.log(number, number.result)
                if (number.result == 1 ) {
                    $(button).toggleClass( "free reserved")
                    $(button).children("div.tchr").html(user_name);   //Send user info to button, reverts on refresh
                    $.toast({
                        heading: "Reservation Clear!",
                        icon: 'success',
                        stack: 4,
                        hideAfter: 2000,
                        bgColor: '#003366'
                            });
            }
        if (number.result == 2) {
             console.log(user)
             $(button).toggleClass( "free reserved")
             $(button).children("div.tchr").html(user_name);   //Send user info to button, reverts on refresh
                $.toast({
                    heading: "Reservation Complete!",
                    icon: 'success',
                    stack: 4,
                    hideAfter: 2000
                });
            }
        if (number.result == 3) {
            alert("Sorry! This has already been reserved (maybe refresh your browser)")
                    }


        count++;
        console.log(count)
        if (count > 3) {
               location.reload();
               };
}
           }); // End AJAX
        });
});




  $(document).ready(function () {
    console.log('ready!'); //Sanity check
    $('#toggle').click(function () {
        var $this = $(this);
        console.log('we clicked!');
        $('#main_view').toggle('500');
        $('#my_view').toggle('500');
        $this.toggleClass('one');
        if ($this.hasClass('one')) {
            $this.text('My Reservations');
        } else {
            $this.text('Today');
            }
    });
});