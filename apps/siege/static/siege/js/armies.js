$(document).ready(function(){
    var editing = false;
    var mytable = $('.mytable').DataTable({
        "paging": false
    });
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

    $('.mytable').on('click', '.edit', function() {
        var form = $('#armyForm');
        var row = $(this).parent().parent();
        var id = row.attr('id');
        var troop_type = row.find('.troop_type').attr('info');
        form.find('#id_city').val(row.find('.city').attr('data'));
        form.find('#id_troop_type option[value="'+troop_type+'"]').prop('selected', true);
        form.find('#id_troop_count').val(parseInt(row.find('.troop_count').text()));
        form.find('#id_speed').val(parseFloat(row.find('.speed').text()));
        form.find('#id_siege_engines').val(row.find('.siege_engines').text());
        form.find('#id_wall_engines').val(row.find('.wall_engines').text());
        form.find('#id_elite_type').val(row.find('.elite_type').text());
        form.find('#id_elite_divs_number').val(row.find('.elite_divs_number').text());
        form.find('#army-button').text("Save army");
        form.attr('action', "/siege/armies/" + id);
        if (!editing) {
            form.append('<button class="btn btn-warning clear">Clear form</button>');
            editing = true;
        }
    })

    $('#armyForm').on('click', '.clear', function(){
        $("#armyForm").find('input:text, input[type=number], select').not(":hidden").val("");
        $("#armyForm").attr('action', '/siege/armies/new');
        $("#armyForm").find('#army-button').text('Add Army');
        $(this).remove();
        editing = false;
    })
});
