$('#new-image').change(function() {
    let file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
});

// Hide sizes options depending on category selected
const hideSizes = function(){
    if ($('#id_category').find(":selected").text()=="Clothing"){
        $('#div_id_shoe_sizes').hide();
        $('#div_id_clothing_sizes').show();
    }
    else if ($('#id_category').find(":selected").text()=="Footwear"){
        $('#div_id_clothing_sizes').hide();
        $('#div_id_shoe_sizes').show();
    }
    else {
        $('#div_id_shoe_sizes').hide();
        $('#div_id_clothing_sizes').hide();
    }
}
// run on page load
hideSizes();
// run when changed
$('#id_category').change(hideSizes);