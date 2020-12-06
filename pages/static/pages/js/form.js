// Submit contact form via ajax
$(document).on('submit', '#contact-form', function(e){
    e.preventDefault();
    $('.submit-icon').hide();
    $('.submit-spinner').css('display', 'inline-block');

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
        $("#contact-form").trigger("reset");
        $('.form-messages').html( `<p>${msg} We will respond to your message as soon as possible.</p>` );
        $('.form-messages').fadeIn( "slow" );
        $('html').animate({
            scrollTop: $('.form-messages').offset().top -70
            }, 500
        );
        $('.submit-spinner').hide();
        $('.submit-check').show();
    });
})