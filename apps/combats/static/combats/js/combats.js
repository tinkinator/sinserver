/**
 * Created by aclawson on 1/12/17.
 */
$(document).ready(function(){
    var topTenTable = $('#topTen').DataTable({"pageLength": 5});
    $('[data-toggle="tooltip"]').tooltip({container: 'body'});
    $('#topTen_wrapper > .row:nth-child(odd) > div').removeClass('col-sm-6').addClass('col-sm-3');
    var plStatsEl = $('#topTen .player .pl-name').next();
    console.log(plStatsEl);
    plStatsEl.each(function(){
        var killed = parseInt($(this).find('.killed').text());
        var total = parseInt($(this).find('.total').text());
        if(total - killed == 0){
            $('<div class="skull-pic"></div>').appendTo($(this).prev());
        }
    })

});