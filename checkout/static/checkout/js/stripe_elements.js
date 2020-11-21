/*
    Core logic/payment flow for this comes from:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from: 
    https://stripe.com/docs/stripe-js
*/

const stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
const clientSecret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
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
    const errorDiv = document.getElementById('card-errors');
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

/**
 *  Handle submitting payment to Stripe
 *  base on https://stripe.com/docs/payments/accept-a-payment#web-submit-payment
 */
const form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    // prevent multiple submissions, disable submit button
    card.update({ 'disabled': true });
    $('#submit-button').attr('disabled', true);
    // Display processing overlay
    $('#payment-form').fadeToggle(100);
    $('#processing-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email.value),
                address:{
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county.value),
                }
            }
        },
        shipping: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                postal_code: $.trim(form.postcode.value),
                state: $.trim(form.county.value),
            }
        },
    })
    .then(function (result) {
        if (result.error) {
            // Show error to your customer (e.g., insufficient funds)
            const errorDiv = document.getElementById('card-errors');
            let html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>
            `;
            $(errorDiv).html(html);
            // Hide processing overlay
            $('#payment-form').fadeToggle(100);
            $('#processing-overlay').fadeToggle(100);
            // enable submit button
            card.update({ 'disabled': false });
            $('#submit-button').attr('disabled', false);
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === "succeeded") {
                form.submit();
            }
        }
    });
});