$(document).ready(function(){
            $("#popout_form").hide();
            $("#create_button").click(function(){
                $("#popout_form").toggle();
            });
            $("#cancel-btn").click(function(){
                $("#popout_form").hide();
            });
});

