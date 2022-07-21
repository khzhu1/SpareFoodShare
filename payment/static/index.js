var stripe = Stripe(STRIPE_PUBLIC_KEY);
var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');
// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
var displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

var form = document.getElementById('payment-form');

elem.addEventListener('click', function(evt) {
  evt.preventDefault();
  
  $.ajax({
    type: "POST",
    url: '/payment/add/',
    data: {
      order_key: clientsecret,
      price: price,
      pid: product_id,
      user_id: user_id,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    },
    success: function (json) {
      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/success/");
          }
        }
      });

    },
  });
})




