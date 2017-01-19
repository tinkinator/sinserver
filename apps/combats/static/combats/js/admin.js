$(document).ready(function() {
    var nameRegex = /^[-@_a-zA-Z0-9]{3,}/;
    var idRegex = /[0-9]{6}/;
    var apiRegex = /(elgea-COMRP-)([-_a-zA-Z0-9]{91})[=]/;

    $('[data-toggle="tooltip"]').tooltip({container: 'body'});

    $.validator.addMethod("apiKey", function(value, element){
        return this.optional(element) || apiRegex.test(value)
    }, "Invalid API key format");

    $.validator.addMethod("checkName", function(value, element){
        return this.optional(element) || nameRegex.test(value)
    })

    $('#player-details').validate({
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
        rules:{
            id: {
                required: true,
                digits: true,
                minlength: 6,
                maxlength: 6
            },
            name: {
                required: true,
                minlength: 3,
                checkName: true
            },
            alliance: {
                required: true,
            },
            api_key: {
                required: true,
                apiKey: true
            }
        },
        messages: {
            id: {
                digits: "ID must contain only numbers",
                minLength: "ID must be 6 characters long",
                maxLength: "ID must be 6 characters long"
            },
            name: {
                required: "No name entered",
                checkName: "Invalid name format",
                minLength: "Too short"
            },
            alliance: {
                required: "No alliance entered"
            },
            api_key: {
                required: "No key entered",
                apiKey: "Invalid API key format"
            }

        }
    })


});