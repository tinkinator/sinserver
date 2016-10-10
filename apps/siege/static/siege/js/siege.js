$(document).ready(function(){

    $('.table-paginated').DataTable();
    /*Time offset regex*/ 
    var offsetRegex = /-?[\d]{2,}:[0-5][0-9]:[0-5][0-9]/;
    /*Adding army row to the siege table*/  
    $(document.body).on('click', 'button.addsiege', function(event){
        var id = sliceAfterDash($(this).attr('id'));
        console.log("ID: ", id);
        var error = false;
        var payLoad = {};
        var $headers = $(this).closest('table').find('th');
        $('#'+id).find('td').each(function(idx){
            if(idx == 6){
                offsetVal = ($(this).find('input').val());
                if (offsetVal == null){
                    error = true;
                console.log("Time offset is empty!");
                $(this).find('input').addClass("input-error");    
                }
                else if (!offsetVal.match(offsetRegex) ){
                    error = true;
                    $(this).find('input').addClass("input-error");
                    console.log("Wrong time format!");
                }
                else {
                    if($(this).find('input').hasClass('error')){
                        $(this).find('input').removeClass('input-error');
                    }
                    
                    error = false;
                    payLoad["Offset"] = offsetVal;
                }
            }
            else if (idx == 7 || idx == 8){
                payLoad[$($headers[idx]).text()] = $(this).find('select').val();
            }
            else{
                payLoad[$($headers[idx]).text()] = $(this).text();   
            }
            payLoad["armyId"] = id;
        });
        console.log(payLoad);
        
        if(!error){
        $.post(window.location.href+"/addarmy", payLoad, function(data, textStatus, xhr) {
            console.log("success");
            $('#'+id).remove();
            return false;
        });
    }
    });

    /*Helper function to parse ID with a dash*/ 
    function sliceAfterDash(str){
            return str.slice(str.lastIndexOf("-")+1);
        }

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
});


});
