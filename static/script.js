// Function to handle form submission and send AJAX request for booking
function bookTurf(cityName, turfName) {
    // Get the phone number input value
    var phoneNumber = document.getElementById('phone_number').value;

    // Validate phone number (you can add more validation as needed)
    if (!phoneNumber || phoneNumber.length !== 10) {
        alert('Please enter a valid 10-digit phone number.');
        return;
    }

    // Prepare the data to be sent in the AJAX request
    var formData = new FormData();
    formData.append('phone_number', phoneNumber);

    // Send an AJAX POST request to the server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/details/' + cityName + '/' + turfName, true); // Endpoint for fetching details
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest'); // Set the X-Requested-With header for AJAX detection
    xhr.onload = function() {
        if (xhr.status === 200) {
            var responseData = JSON.parse(xhr.responseText);
            // Display the details in a modal or any other element on the page
            // For example, assuming there's a div with id "details-container" to display details
            document.getElementById('details-container').innerHTML = responseData.details;
            // Show success message
            alert('Booking successful! SMS sent.');
            // You can perform additional actions here after successful booking
        } else {
            // Show failure message
            alert('Booking successful, but SMS failed to send.');
            // You can handle the failure scenario here
        }
    };
    xhr.send(formData); // Send the form data
}
