// Wrapping the code in event listener and passing the django.jQuery library so can use dollar within this function, is from the second answer on this page https://stackoverflow.com/questions/58087470/django-jquery-is-not-a-function-message

window.addEventListener("load", function() {
    (function($) {
        // Hide sizes options depending on category selected
        const hideSizes = function(){
            console.log($('#id_category').find(":selected").text());
            if ($('#id_category').find(":selected").text()=="clothing"){
                $('.field-shoe_sizes').hide();
                $('.field-clothing_sizes').show();
            }
            else if ($('#id_category').find(":selected").text()=="footwear"){
                $('.field-clothing_sizes').hide();
                $('.field-shoe_sizes').show();
            }
            else {
                $('.field-shoe_sizes').hide();
                $('.field-clothing_sizes').hide();
            }
        };
        
        // run on page load
        hideSizes();
        // run when changed
        $('#id_category').change(hideSizes);
    })(django.jQuery);
});