console.log("Admin Sanity check");

window.addEventListener("load", function() {
    (function($) {
        $("#id_category").change(function() {
            console.log($('#id_category').find(":selected").text());
        });
    })(django.jQuery);
});
// Hide sizes options depending on category selected
const hideSizes = function(){
    console.log('change deteched');
    console.log($('field-category'));
    console.log($('#id_category option:selected').text());
    if ($('#id_category option:selected').text()=="clothing"){
        console.log("Clothing selected");
        $('.field-shoe_sizes').hide();
        $('.field-clothing_sizes').show();
    }
    else if ($('#id_category').find(":selected").text()=="trainers"){
        console.log("Trainers selected");
        $('.field-clothing_sizes').hide();
        $('.field-shoe_sizes').show();
    }
    else {
        $('.field-shoe_sizes').hide();
        $('.field-clothing_sizes').hide();
    }
}
// run on page load
//hideSizes()(django.jQuery);
// run when changed
//$('#id_category').change(hideSizes)(django.jQuery);