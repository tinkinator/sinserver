$(document).ready(function() {
    var topTenTable = $('#topTen').DataTable({"pageLength": 5});
    $('[data-toggle="tooltip"]').tooltip({container: 'body'});
    $('#topTen_wrapper > .row:nth-child(odd) > div').removeClass('col-sm-6').addClass('col-sm-3');
    // var plStatsEl = ;
    // console.log(plStatsEl);
    addSkulls()
    $('#topTen').on('draw.dt', function(){
        addSkulls()
    });

    function addSkulls() {
        $('#topTen').find('.pl-name').next().each(function () {
            var killed = parseInt($(this).find('.killed').text());
            var total = parseInt($(this).find('.total').text());
            if (total - killed == 0) {
                if($(this).parent().find('.skull-pic').length == 0) {
                    $('<div class="skull-pic"></div>').appendTo($(this).prev());
                }
            }
        })
    }


});