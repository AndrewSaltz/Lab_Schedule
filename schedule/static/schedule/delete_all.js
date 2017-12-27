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
    beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
$(document).ready(function () {
    console.log('delete ready!'); //Sanity check
    $('#delete_all').click(function () {
        var r = confirm("Are you sure you delete ALL slots?")
        if (r == true) {
            var s = confirm("No really! You're deleting everything except users. That's what you want?")
            if (r == true) {
                $.ajax({
                    url: /delete_all/,
                    type: "POST",
                    success: function () {
                        alert('All objects deleted!')
                    }
                });
            } else {
                return;
            }
        } else {
            return;
        }
    });
});
