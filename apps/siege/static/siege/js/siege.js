$(document).ready(function(){

    $('.table-paginated').DataTable();
    /*Time offset regex*/ 
    var offsetRegex = /(-?)([\d]{2,}):([0-5][0-9]):([0-5][0-9])/;
    /*Datetime format regex*/
    var dateRegex = /(\d{2})\-(\d{2})\-(\d{4})\s(\d{2}):(\d{2}):(\d{2})/;
    var siegeLandTime = dateFromTableCell($('#sieges').find('.landing').text());
    var editing = false;

    /*Adding army row to the siege table*/  
    $(document.body).on('click', '.addsiege', function(event) {
        var id = sliceAfterDash($(this).attr('id'));
        console.log("ID: ", id);
        var error = false;
        var payLoad = {};
        var $headers = $(this).closest('table').find('th');
        /*add all the cell contents from the row to payload*/
        $('#'+id).find('td').each(function(idx) {
            if(idx == 7) {
                offsetVal = ($(this).find('input').val());
                error = !validateOffset(offsetVal);
                if(error) {
                $(this).find('input').addClass("input-error");
                }
                else {
                        if($(this).find('input').hasClass('input-error')) {
                        $(this).find('input').removeClass('input-error');
                    }
                    payLoad["Offset"] = offsetVal;
                }
            }
            else if (idx == 8 || idx == 9){
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

    /*save speed of an army in the unassigned table*/
    $('#unassignedArmies').on('click', '.saveArmy', function(){
        var row = $(this).parent().parent();
        var payload = {};
        var id = row.attr('id');
        payload["speed"] = row.find('.speed').text().trim();
        payload["ajax"] = "true";
        console.log(payload);
        $.post("/siege/armies/"+id, payload, function(data, textStatus, xhr){
            console.log(data);
            return false;
        })
    });

    /*show the edit-siege form*/
    $('#sieges').on('click', '.edit', function(){
        if(!editing){
            var id = $(this).attr('id');
            var row = $(this).parent().parent();
            var form = $('#edit-siege');
            form.attr('action', '/siege/'+id);
            form.find('#id_target_player').val(row.find('.player').text());
            form.find('#id_target_city').val(row.find('.city').text());
            form.find('#id_x_coord').val(row.find('.x').text());
            form.find('#id_y_coord').val(row.find('.y').text());
            form.find('#id_landing_time').val(row.find('.landing').text());
            $('.form-row').show();
            $(this).text('Cancel').removeClass('btn-success').addClass('btn-warning');

            editing = true;
        }
        else if(editing){
            $('.form-row').hide();
            $(this).text('Edit').removeClass('btn-warning').addClass('btn-success');
            editing = false;
        }
    })

    /*save everything about army and siege in the assigned table*/
    $('#assigned').on('click', '.saveArmy', function(){
        var row = $(this).parent().parent();
        var army = {};
        var siege = {};
        var speed = row.find('.speed').text().trim();
        var offset = row.find('.offsetInput').val();
        var valid = validateOffset(offset) && validateSpeed(speed);
        if(valid)
        {
            var id = row.attr('id');
            var siegeArmyId = row.attr('data');
            army["speed"] = speed;
            army["troop_count"] = row.find(".troop_count").text();
            army["ajax"] = "true";
            siege["offset"] = offset;
            siege["siege_square"] = row.find(".square").text();
            siege["orders"] = row.find(".orders").text();
            console.log("posting: ", army);

            $.when(
                $.post("/siege/armies/"+id, army),
                $.ajax({
                    url: window.location.href+"/armies/"+siegeArmyId,
                    type: 'PUT',
                    data: JSON.stringify(siege),
                    dataType: 'json'
                })
            ).then(function(data, textStatus, xhr){
                console.log(data);
                return false;
            });
        }
    });

    /*make the siege square cell turn into a dropdown*/
    $('#assigned').on('click', '.square p', function(){
        var options = $('#sieges tr td:nth-child(5)').text().trim().split(" ");
        options.push("DIR");
        var select = $(this).parent().find('.squareSelect');
        var cur = $(this).text();
        $.each(options, function(index, option){
            select.append($('<option>', { value: option}).text(option))
        });
        select.val(cur);
        $(this).hide();
        select.show();
        select.focus();
    });

    /*turn off dropdown in the siege square cell*/
    $('#assigned').on('focusout', '.squareSelect', function(){
        var square = $(this).parent().find('p');
        var selected = $(this).val();
        square.text(selected);
        $(this).empty();
        $(this).hide();
        square.show();
    });


    /*make the orders square cell turn into a dropdown*/
    $('#assigned').on('click', '.orders p', function(){
        var options = ['occupy', 'attack', 'blockade', 'siege'];
        var select = $(this).parent().find('select');
        $.each(options, function(index, option){
            select.append($('<option>', { value: option}).text(option))
        });
        var cur = $(this).text();
        select.val(cur);
        $(this).hide();
        select.show();
        select.focus();
    });

    /*turn off dropdown in the orders square cell*/
    $('#assigned').on('focusout', '.ordersSelect', function(){
        var orders = $(this).parent().find('p');
        var selected = $(this).val();
        orders.text(selected);
        $(this).empty();
        $(this).hide();
        orders.show();
    });

    /*adjust launch time when offset is changed*/
    $('.siegetable').on('focusout', '.offsetInput', function(){
        var match = $(this).val().match(offsetRegex);
        if(!match)
        {
            $(this).addClass('input-error');
        }
        else {
            if($(this).hasClass('input-error'))
            {
                $(this).removeClass('input-error');
            }
            var row = $(this).parent().parent();
            var offsetP = row.find('.offset').find('p'); 
            if(offsetP.length > 0)
            {
                offsetP.text($(this).val());
                offsetP.show();
                $(this).hide();
            }
            var newLaunchTime = calcLaunchTime(row);
            var timeCell = row.find('.timer');
            console.log(timeCell);
            timeCell.text(stringifyDateTime(newLaunchTime));
        }
    });

    /*change army speed*/
    $('.siegetable').on('click', '.speed p', function(){
        var speed = $(this).text();
        var parent = $(this).parent();
        var speedInput = parent.find('.speedInput');
        $(this).hide();
        console.log("Printing speedinput", speedInput);
        speedInput.val(speed);
        speedInput.show();
        setTimeout(function(){speedInput.focus()},200);
    });

    /*focusing out of speed input turns it back into a table cell*/
    $('.siegetable').on('blur', '.speedInput', function(){
        var row = $(this).parent().parent();
        
        var speed = $(this).val();
        var speedCell = $(this).parent().find('p');
        var oldSpeed = speedCell.text();
        var launchCell = row.find('.timer');
        var etaCell = row.find('.eta');
        speedCell.text(speed);
        var newLaunchTime = calcLaunchTime(row);

        var newETA = calcETA(row);
        if(etaCell.length > 0){
            etaCell.text(parseFloat(Math.round(newETA*1000)/1000).toFixed(3));
        }
        $(this).hide();
        speedCell.show();
        launchCell.text(stringifyDateTime(newLaunchTime));
        if(speed != oldSpeed)
        {
        speedCell.addClass("error");
        if(etaCell.length > 0)
        {
            etaCell.addClass("error");
        }
        }
    });

    $('#assigned').on('click', '.offset p', function(){
        var row = $(this).parent();
        var offset = $(this).text();
        var offsetInput = row.find('.offsetInput');
        $(this).hide();
        offsetInput.val(offset);
        offsetInput.show();
        offsetInput.focus();
    });

    /*Deleting siege on the edit siege table should redirect back to the dashboard*/
    $('#sieges').on('click', '.delete', function () {
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

    /*Clicking on the edit button should bring up a siege form*/
    $('#sieges').on('click', '.edit', function () {
        console.log("editing this siege")
        });

    /*Clicking on the delete icon in the assigned table should delete army from siege*/
    $('#assigned').on('click', '.removeArmy', function(){
        var id = $(this).parent().parent().attr('data');
        var siegeId = $(this).attr('data');
        console.log("Siegearmy ID:", id);
        $.ajax({
            url: "/siege/" + siegeId + "/armies/" + id,
            type: 'DELETE',
            success: function(data, textStatus, xhr){
            console.log(textStatus);
            window.location.href = "/siege/" + siegeId;
        },
        error: function(error){
            console.log(error);
        }
        })

    });

    function validateOffset(offset){
        if (offset == "" || !offset.match(offsetRegex)) {
            return false;
        }
        return true;
    }

    function validateSpeed(speed){
        if (speed == "" || isNaN(parseFloat(speed))){
            return false;
        }
        return true;
    }

    /*Function to convert time from table cell to datetime*/
    function dateFromTableCell(dateStr){
        var match = dateStr.match(dateRegex);
        return new Date(Date.UTC(match[3], match[1]-1, match[2], match[4], match[5], match[6]));
    }

    /*Function to calculate launch time based on speed adjustments*/
    function calcLaunchTime(row){
        var eta = calcETA(row);
        var offset;
        if (row.find('.offsetInput').length > 0)
        {
            offset = getOffsetSeconds(row.find('.offsetInput').val());
        }
        else
        {
            offset = getOffsetSeconds(row.find('.offset p').text());
        }
        console.log("calculating launch, offset:", row.find('.offset'), offset);
        return new Date(siegeLandTime.getTime() - (eta*3600000) + offset*1000);
    }

    function calcETA(row)
    {
        var dist = parseFloat(row.find('.dist').text());
        var speed = parseFloat(row.find('.speed').text());
        console.log("Calculating ETA", dist/speed);
        return dist/speed;
    }

    /*Helper function to parse ID with a dash*/ 
    function sliceAfterDash(str){
            return str.slice(str.lastIndexOf("-")+1);
        }

    //Convert date object to datetime string in MM-DD-YYYY HH:MM:SS format
    function stringifyDateTime(date) {
        var month = zeroPadded((date.getUTCMonth()+1).toString());
        var day = zeroPadded(date.getUTCDate().toString());
        var y = date.getUTCFullYear();
        var h = zeroPadded(date.getUTCHours().toString());
        var min = zeroPadded(date.getUTCMinutes().toString());
        var sec = zeroPadded(date.getUTCSeconds().toString());
        return month + "-" + day + "-" + y + " " + h + ":" + min + ":" + sec;
    }

    function zeroPadded(myStr)
    {
        if (myStr.length == 1)
        {
            return "0" + myStr;
        }
        return myStr;
    }

    function getOffsetSeconds(offset)
    {
        console.log(offset);
        if(offset == "")
        {
            return 0;
        }
        var time = offset.match(offsetRegex);
        var seconds = parseInt(time[2])*3600 + parseInt(time[3])*60+parseInt(time[4]);
        console.log(time, seconds, time[1], time[2], time[3], time[4]);
        if (time[1] != undefined)
        {
            console.log("negative offset");
            return -seconds;
        }
        return seconds;
    }
});
