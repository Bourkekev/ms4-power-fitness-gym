// Get Stripe publishable key
fetch("/memberships/config/")
    .then(res => res.text())          // convert to plain text
    .then(text => console.log(text))  // then log it out
    // .then((result) => {
    //     return result.json();
    // })
    // .then((data) => {
    //     // Initialize Stripe.js
    //     const stripe = Stripe(data.publicKey);
    // });

// Create a Checkout Session with the selected plan ID
let createCheckoutSession = function (priceId) {
    return fetch("/create-checkout-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            priceId: priceId,
        }),
    }).then(handleFetchResult);
};

// Handle any errors returned from Checkout
var handleResult = function (result) {
    if (result.error) {
        var displayError = document.getElementById("error-message");
        displayError.textContent = result.error.message;
    }
};

// Setup event handler to create a Checkout Session when button is clicked
document
    .getElementById("submitBtnGold")
    .addEventListener("click", function (evt) {
        createCheckoutSession(PriceId).then(function (data) {
            // Call Stripe.js method to redirect to the new Checkout page
            stripe
                .redirectToCheckout({
                    sessionId: data.sessionId,
                })
                .then(handleResult);
        });
    });