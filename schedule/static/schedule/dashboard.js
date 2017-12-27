$(document).ready(function () {
    console.log('ready!'); //Sanity check
    $('#day_view').click(function () {
        console.log('we clicked!');
        $('#days').show("fast");
        $('#by-cart').hide("fast");
    });
    $('#cart_view').click(function () {
        $('#days').hide("fast");
        $('#by-cart').show("fast");
    });
    $body = $("body");

    $(document).on({
        ajaxStart: function () {
            console.log('loading')
            $body.addClass("loading");
        },
        ajaxStop: function () {
            $body.removeClass("loading");
        }
    });

});
