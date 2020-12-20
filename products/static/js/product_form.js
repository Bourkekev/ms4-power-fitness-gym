$('#new-image').change(function() {
    let file = $('#new-image')[0].files[0];
    $('#filename').text(`Image will be set to: ${file.name}`);
});

// Hide sizes options depending on category selected
const hideSizes = function(){
    //console.log($(this));
    //console.log($(this).find(":selected").text());
    if ($(this).find(":selected").text()=="Clothing"){
        console.log("Clothing selected");
        $('#div_id_shoe_sizes').hide();
        $('#div_id_clothing_sizes').show();
    }
    else if ($(this).find(":selected").text()=="Trainers"){
        console.log("Trainers selected");
        $('#div_id_clothing_sizes').hide();
        $('#div_id_shoe_sizes').show();
    }
    else {
        $('#div_id_shoe_sizes').hide();
        $('#div_id_clothing_sizes').hide();
    }
    
}
$('#id_category').change(hideSizes);