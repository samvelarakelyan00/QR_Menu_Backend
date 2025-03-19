const ratingPointsContainer = document.querySelector('.rating-points');
const selectedRating = document.getElementById('selected-rating');
const feedbackText = document.getElementById('feedback-text');
const submitButton = document.getElementById('submit-feedback');

const popup = document.getElementById('popup');
const popupMessage = document.getElementById('popup-message');
const popupClose = document.getElementById('popup-close');
const popupIcon = document.querySelector('.popup-icon');

let currentRating = 0;

// Generate rating points
for (let i = 1; i <= 10; i++) {
  const ratingPoint = document.createElement('div');
  ratingPoint.classList.add('rating-point');
  ratingPoint.textContent = i;

  ratingPoint.addEventListener('click', () => {
    currentRating = i;
    selectedRating.textContent = `Rating: ${i}`;

    // Update styling for selected point
    document.querySelectorAll('.rating-point').forEach((point) => point.classList.remove('selected'));
    ratingPoint.classList.add('selected');
  });

  ratingPointsContainer.appendChild(ratingPoint);
}

submitButton.addEventListener('click', () => {
  if (currentRating === 0) {
    showPopup('Please select a rating.', false);
    return;
  }

  const feedback = feedbackText.value;

  // Simulate sending data (replace with actual AJAX call)
  simulateSendData(currentRating, feedback)
    .then(() => {
      // Clear the form
      currentRating = 0;
      selectedRating.textContent = '';
      feedbackText.value = '';

      document.querySelectorAll('.rating-point').forEach(point => point.classList.remove('selected'));

      // Show success pop-up
      showPopup('Feedback sent successfully!', true);
    })
    .catch(() => {
      // Show error pop-up
      showPopup('Failed to send feedback. Please try again.', false);
    });
});

// Function to show pop-up with dynamic styling
function showPopup(message, isSuccess = true) {
  popupMessage.textContent = message;

  if (isSuccess) {
    popup.style.borderColor = "#4CAF50"; // Green border
    popupMessage.style.color = "#4CAF50"; // Green text
    popupIcon.textContent = "✔"; // Green checkmark
    popupIcon.style.color = "#4CAF50"; // Green check icon
  } else {
    popup.style.borderColor = "#F44336"; // Red border for error
    popupMessage.style.color = "#F44336"; // Red text
    popupIcon.textContent = "✖"; // Red X
    popupIcon.style.color = "#F44336"; // Red X icon
  }

  popup.style.display = 'block';
}

// Close the pop-up when clicking "OK"
popupClose.addEventListener('click', () => {
  popup.style.display = 'none';
});

// Simulate sending data (replace with your actual AJAX call)
function simulateSendData(rating, feedback) {
  return new Promise((resolve, reject) => {
    const success = Math.random() > 0.2; // 80% success rate

    setTimeout(() => {
      if (success) {
        console.log('Simulated feedback sent:', { rating, feedback });
        resolve();
      } else {
        console.error('Simulated feedback failed to send.');
        reject();
      }
    }, 1000); // Simulate a 1-second delay
  });
}
