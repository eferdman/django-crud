$(document).ready(function () {
    $("#create_button").click(function () {
        $("#popout_form").toggleClass("hidden");
    });
    $("#cancel-btn").click(function () {
        $("#popout_form").hide();
    });

    // Edit on hover
    $('td[data-editable]').hover(function () {
        var $el = $(this);
        var $button = $el.find('button');
        $button.removeClass("hidden");
    }, function () {
        var $el = $(this);
        var $button = $el.find('button');
        $button.addClass("hidden");
    });

    $('body').on('click', 'td[data-editable]', function () {

        var $el = $(this);
        var $span = $el.find('span');
        var $input = $("<input />", {"placeholder": $span.text(), "name": "updated_table" })
            .css("border", "none")
            .css("background-color", "transparent")
            .css("outline", "transparent");
        replaced = $span.replaceWith($input.focus());

        var save = function () {
            $input.addClass("hidden");
            $el.find('form').prepend(replaced);
        };

        // the 'blur' event is sent to an element when it loses focus
        // the one() method-- the handler is unbound after first invocation
        $input.one('blur', save).focus();
    });

});

