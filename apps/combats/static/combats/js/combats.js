/**
 * Created by aclawson on 1/12/17.
 */
$(document).ready(function(){
    var topTenTable = $('#topTen').DataTable({"pageLength": 5});
    $('[data-toggle="tooltip"]').tooltip({container: 'body'});
    $('#topTen_wrapper > .row:nth-child(odd) > div').removeClass('col-sm-6').addClass('col-sm-3');
})