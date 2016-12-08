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
            name: {
                required: true
            },
            x_coord: {
                required: true
            },
            y_coord: {
                required: true
            },
            region: {
                required: true
            }
        },
        messages: {
            name: {
                required: "City name cannot be blank"
            },
            x_coord: {
                required: "No X coordinate entered"
            },
            y_coord: {
                required: "No Y coordinate entered"
            },
            region: {
                required: "No region entered"
            }
        }
    });

     $('.mytable').on('click', '.delete', function(){
        var cityId = $(this).parent().parent().attr('id');
        $.ajax({
            url: "/siege/cities/"+cityId,
            type: 'DELETE',
            success: function(data, textStatus, xhr){
                console.log(textStatus);
                window.location.href=('/siege/cities');
            },
            error: function(error){
                console.log(error);
            }
        })

    });
});

