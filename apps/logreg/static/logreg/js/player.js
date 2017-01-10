$(document).ready(function(){
    var passwordVerified = false;
    var emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var nameRegex = /^[-@_a-zA-Z]{3,}/
    var apiRegex = /(elgea-COMRP-)([-_a-zA-Z0-9]{91})[=]/
    $('#formSubmit').prop('disabled', true);

    $('button.edit').click(function(){
        var id = $(this).attr('id');
        if($('#formDiv').css('display') != 'none'){
            $('#formSubmit').prop('disabled', true);
            $('#errors').text('');
            $('#input-1').val('').prop('name', '').prop('type', 'text');
            if($('#formDiv').find('#pass1').length > 0){
                $('#formDiv').find('#pass1').remove();
                $('#formDiv').find('#pass2').remove();
            }
            $('#formDiv').hide();
        }
        else
        {
            switch(id){
                case "name":
                    $('#formDiv').find('.info-label').text("Name:");
                    $('#playerForm').attr('action', '/account/name');
                    $('#input-1').attr('name', 'name');
                    break;
                case "passwd":
                    $('#formDiv .info-value').prepend("" +
                        "<div id='pass1'><input id='input-2' type='password'></div>" +
                        "<div id='pass2'><button class='btn btn-info' id='checkPass'>Verify password</button></div>"
                    )
                    $('#formDiv').find('.info-label').text("Password:");
                    $('#playerForm').attr('action', '/account/password');
                    $('#input-1').prop('type', 'password').attr('name', 'password');
                    break;
                case "key":
                    $('#formDiv').find('.info-label').text("Combat API key:");
                    $('#playerForm').attr('action', '/account/apikey');
                    $('#input-1').attr('name', 'key');
                    break;
                case "email":
                    $('#formDiv').find('.info-label').text("Email:")
                    $('#playerForm').attr('action', '/account/email');
                    $('#input-1').attr('name', 'email');
                    break;
                default:
                    $('#formDiv').find('.info-label').text("Label:")
            }
            $('#formDiv').show();
        }
    });

    $('#formDiv').on('click', '#checkPass', function(){

        var payLoad = {'password': $('#input-2').val()}
        $.post("/account/checkpassword", payLoad)
            .done(function(data){
                alert(data);
                passwordVerified = true;
            }).
        fail(function(){
            alert("Invalid password, try again!")
            passwordVerified = false;
            $('#formSubmit').prop('disabled', true);
        });
    })

    $('#formDiv').on('focusout', 'input[name="password"]', function(){
        var pass = $(this).val();
        console.log(pass.length);
        if(pass.length < 8){
            console.log("too short!", $(this))
            $('#errors').text("Password must be at least 8 characters long");
        }
        else{
            if(passwordVerified){
                $('#formSubmit').prop('disabled', false);
            }
        }
    });

    $('#formDiv').on('keyup', 'input[name="email"]', function(){
        var email = $(this).val();
        if(email.match(emailRegex)){
            $('#errors').text('');
            $('#formSubmit').prop('disabled', false);
        }
        else{
            $('#formSubmit').prop('disabled', true);
        }
    });

    $('#formDiv').on('focusout', 'input[name="email"]', function(){
        var email = $(this).val()
        if(!email.match(emailRegex)){
            $('#errors').text("Not a valid email");
        }
    })

    $('#formDiv').on('keyup', 'input[name="name"]', function(){
      var name = $(this).val()
        if(name.match(nameRegex)){
            $('#errors').text('');
            $('#formSubmit').prop('disabled', false);
        }
        else{
            $('#formSubmit').prop('disabled', true);
        }
    });

    $('#formDiv').on('focusout', 'input[name="name"]', function(){
        var email = $(this).val()
        if(!email.match(nameRegex)){
            $('#errors').text("Name should be at least 3 characters long and contain only letters or -, _, and @");
        }
    })

    $('#formDiv').on('keyup', 'input[name="key"]', function(){
        var key = $(this).val();
        if(key.match(apiRegex)){
            $('#errors').text('');
            $('#formSubmit').prop('disabled', false);
        }
        else{
            $('#formSubmit').prop('disabled', true);
        }
    });

    $('#formDiv').on('focusout', 'input[name="key"]', function(){
        var email = $(this).val()
        if(!email.match(apiRegex)){
            $('#errors').text("Invalid API key pattern");
        }
    })

    $('#formDiv').on('focus', '#input-1', function(){
        $('#errors').text('');
    });


});