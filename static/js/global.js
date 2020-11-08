(function ($) {
    $(function () {
        /** Make header sticky after scroll y amount, 
         * and make Back to Top visible */
        $(window).scroll(function() {
            // Track scroll amount
            let yPos = ( $(window).scrollTop() );
            // Get header height
            let headerHeight = ( $('header').outerHeight() );

            /* When scroll is greater than header,
             * also add class to back-to-top */
            if(yPos > (headerHeight + 25)) {
                $('header').addClass('sticky');
                $('.back-to-top').addClass('visible');
            }
            else {
                $('header').removeClass('sticky');
                $('.back-to-top').removeClass('visible');
            }
        });

        /** Scroll to top */
        $('.back-to-top').on('click', function(event){
            event.preventDefault();
            $('html').animate({
                scrollTop: 0
                }, 700
            );
        });

    }); // end of document ready
})(jQuery); // end of jQuery name space