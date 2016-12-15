$(document).ready(function() {

    $('.sieges').on('click', '.delete', function () {
        if(confirm("Are you sure you want to delete this siege?")){
             $.ajax({
            url: "/siege/" + $(this).attr('id'),
            type: 'DELETE',
            success: function (data, textStatus, xhr) {
                console.log(textStatus);
                window.location.href = ("/siege/");
            },
            error: function (error) {
                console.log(error);
            }
        });
        }
        else{
            $(this).blur();
        }
    });


    $('.sieges').on('click', '.edit', function () {
            window.location.href = "/siege/" + $(this).attr('id')
        });


});