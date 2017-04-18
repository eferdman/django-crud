$(document).ready(function () {
    $("#create_button").click(function () {
        $("#popout_form").toggleClass("hidden");
    });
    $("#cancel-btn").click(function () {
        $("#popout_form").addClass("hidden");
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

        // the cell the user clicks inside of
        var $el = $(this);
        // The span containing the name
        var $span = $el.find('span');
        // form in the cell
        var $form = $el.find('form');

        var $input = $("<input />", {"placeholder": $span.text(), "name": "updated_value", "id": "dynamic-input"})
            .css("border", "none")
            .css("background-color", "transparent")
            .css("outline", "transparent");

        // check if form already contains the input before adding it
        // this should happen once
        if (!$form.has("#dynamic-input").length) {
            $form.prepend($input.focus());
            $span.hide();

        } else if ($form.has("#dynamic-input.hidden").length) {
            $input = $form.find("#dynamic-input");
            $input.toggleClass("hidden").focus();
            $span.hide();
        }

        var save = function () {
            $span.show();
            $input.addClass("hidden");
        };

        // the 'blur' event is sent to an element when it loses focus
        // the one() method-- the handler is unbound after first invocation
        $input = $form.find("#dynamic-input");
        $input.one('blur', save).focus();
    });

});

