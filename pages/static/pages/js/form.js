console.log("sanity check");
$(document).on('submit', '#contact-form', function(e){
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '/contact/submit/',
        data: {
            first_name:$('#id_first_name').val(),
            last_name:$('#id_last_name').val(),
            email:$('#id_email').val(),
            phone_number:$('#id_phone_number').val(),
            subject:$('#id_subject').val(),
            your_message:$('#id_your_message').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(){
            console.log("Form submitted successfully")
        },
        statusCode: {
            404: function() {
                alert( "Url to submit to not found!" );
            },
            500: function() {
                console.log("No response from server after submission." );
            }
        }
    }).done(function(msg) {
        console.log( "Data Saved: " + msg );
        $("#contact-form").trigger("reset");
        $('.form-messages').html( "<p>Your message has been submitted successfully. We will respond to your message as soon as possible.</p>" );
        $('.form-messages').fadeIn( "slow" );
    });
})