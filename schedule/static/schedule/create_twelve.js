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
    console.log('ready!'); //Sanity check
    $('#create_twelve').click(function () {
        console.log('create twelve');
        var r = confirm("Are you sure you want to create twelve weeks?")
        if (r == true) {
            $.ajax({
                url: /create_twelve/,
                type: "POST",
                dataType: "json",
                success: function (data) {
                    alert('Created ' + data.total + ' entries, starting on ' + data.start + ', ending on ' + data.end);
                    console.log('dupes' + data.dupe_list)
                }
            });
        } else {
            return;
        }
    });
});
