// Get Stripe publishable key
fetch("/memberships/config/")
.then((result) => {
    return result.json();
})
.then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Subscription checkout, pass in button that was clicked
    const subCheckout = function(btn) {
        let price_id = (btn.dataset.price_id);
        // Get Checkout Session ID
        fetch(`/memberships/create-checkout-session/${price_id}`)
        .then((result) => { return result.json(); })
        .then((data) => {
            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({sessionId: data.sessionId});
        })
        .then((res) => {
            // console.log(res);
        });
    };
    // Get buttons if exits and listen for click on button
    if (document.querySelector("#membership-select")) {
        const submitBtnGold = document.querySelector("#submitBtnGold");
        const submitBtnPlat = document.querySelector("#submitBtnPlat");
        
        submitBtnGold.addEventListener("click", function(btn) { return subCheckout(submitBtnGold); });
        submitBtnPlat.addEventListener("click", function(btn) { return subCheckout(submitBtnPlat); });
    }
});
