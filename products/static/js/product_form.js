console.log('form js loaded');
$('#new-image').change(function() {
    let file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
});