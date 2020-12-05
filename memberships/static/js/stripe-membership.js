// Get Stripe publishable key
fetch("/memberships/config/")
.then((result) => {
    return result.json();
})
.then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler for Gold plan
    const submitBtnGold = document.querySelector("#submitBtnGold");
    submitBtnGold.addEventListener("click", () => {
        price_id = (submitBtnGold.dataset.price_id);
        // Get Checkout Session ID
        fetch(`/memberships/create-checkout-session/${price_id}`)
        .then((result) => { return result.json(); })
        .then((data) => {
            console.log(data);
            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
            console.log(res);
        });
    });
    // Event handler for Platinum plan
    const submitBtnPlat = document.querySelector("#submitBtnPlat");
    submitBtnPlat.addEventListener("click", () => {
        price_id = (submitBtnPlat.dataset.price_id);
        // Get Checkout Session ID
        fetch(`/memberships/create-checkout-session/${price_id}`)
        .then((result) => { return result.json(); })
        .then((data) => {
            console.log(data);
            // Redirect to Stripe Checkout
            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
            console.log(res);
        });
    });
});
