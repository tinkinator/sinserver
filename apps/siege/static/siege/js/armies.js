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

    $('.mytable').on('click', '.delete', function(){
        var armyId = $(this).parent().parent().attr('id')
        $.ajax({
            url: "/siege/armies/"+armyId,
            type: 'DELETE',
            success: function(data, textStatus, xhr){
                console.log(textStatus);
                window.location.href=('/siege/armies');
            },
            error: function(error){
                console.log(error);
            }
        })
    })
});
