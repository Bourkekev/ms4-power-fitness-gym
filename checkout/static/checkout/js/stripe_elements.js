/*
    Core logic/payment flow for this comes from:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from: 
    https://stripe.com/docs/stripe-js
*/

let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
let client_secret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripe_public_key);
let elements = stripe.elements();

/** Create styles for card */
let style = {
    base: {
        color: "#32325d",
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        "::placeholder": {
            color: "#aab7c4",
        },
    },
    invalid: {
        color: "#dc3545",
        iconColor: "#dc3545",
    },
};
// Create card and pass styles
let card = elements.create('card', {style: style});
// Mount on div in checkout.html
card.mount('#card-element');

//Check validation when card element changes 
card.addEventListener('change', function(event){
    let errorDiv = document.getElementById('card-errors');
    if (event.error){
        let html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});
