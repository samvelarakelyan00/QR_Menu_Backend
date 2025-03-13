const getStartedButtons = document.querySelectorAll('.get-started-btn');

getStartedButtons.forEach(button => {
  button.addEventListener('click', () => {
    const plan = button.dataset.plan;
    const duration = button.dataset.duration;
    const price = button.dataset.price;

    // You can replace this alert with your actual payment processing logic
    alert(`Selected: ${plan} Plan, ${duration} Months, Price: ${price} AMD. Proceed to payment.`);

    // Here, you would typically redirect the user to a payment page or trigger
    // a payment modal, passing the plan details (plan, duration, price)
    // to your payment processing system.
  });
});