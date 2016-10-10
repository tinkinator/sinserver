$(document).ready(function(){

    $('#armyForm').validate({
        errorElement: "div",
        errorPlacement: function(error, element){
            var placement = $(element).data('error');
            if(placement){
                $(placement).append(error);
            }
            else {
                error.insertAfter(element);
            }
        },
        rules: {
            city: {
                required: true
            },
            troop_type: {
                required: true
            },
            troop_count: {
                required: true,
                min: 10
            },
            speed: {
                required: true,
                min: 5
            }
        },
        messages: {
            city: {
                required: "No city chosen!"
            },
            troop_type: {
                required: "Choose a troop type!"
            },
            troop_count: {
                required: "No troop count entered",
                min: "Mr. General, put at least 10 soldiers in your army!"
            },
            speed: {
                required: "No speed entered!",
                min: "Are you kidding? Even slugs go 5 sq/hour!"
            }
        }
    });

});
