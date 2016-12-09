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

    $('.mytable').on('click', '.edit', function(){
        var form = $('#armyForm');
        var row = $(this).parent().parent();
        var id = row.attr('id');
        form.find('#id_name').val(row.find('.name').text());
        form.find('#id_region').val(row.find('.region').text());
        form.find('#id_x_coord').val(parseInt(row.find('.x_coord').text()));
        form.find('#id_y_coord').val(parseInt(row.find('.y_coord').text()));
        form.find('#army-button').text("Save city");
        form.append('<button class="btn btn-warning clear">Clear form</button>');
        form.attr('action', "/siege/cities/" + id);
    })

    $('#armyForm').on('click', '.clear', function(){
        $("#armyForm").find('input:text, input[type=number]').not(":hidden").val("");
        $("#armyForm").attr('action', '/siege/cities/new');
        $("#armyForm").find('#army-button').text('Add City');
        $(this).remove();
    })
});

