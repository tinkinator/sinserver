$(document).ready(function() {

    $('.sieges').on('click', '.delete', function () {
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
    });


    $('.sieges').on('click', '.edit', function () {
            window.location.href = "/siege/" + $(this).attr('id')
        });


});