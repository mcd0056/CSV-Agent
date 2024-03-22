// script.js

var BaseURL = "http://localhost:8000"

document.getElementById('uploadButton').addEventListener('click', async function() {
    var fileInput = document.getElementById('csvFileInput');
    var file = fileInput.files[0];
    if(file) {
        let formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${BaseURL}/upload_csv/`, {
                method: 'POST',
                body: formData,
            });
            if (response.ok) {
                const result = await response.json();
                showToast(result.message);
            } else {
                // Get more detailed error information
                const errorResult = await response.text();
                showToast(`Failed to upload and process CSV. Server says: ${errorResult}`);
            }
        } catch (error) {
            console.error('Error uploading CSV:', error);
            showToast(`Error during CSV upload: ${error.message}`);
        }
    } else {
        alert("Please select a file to upload.");
    }
});

document.getElementById('sendButton').addEventListener('click', function() {
    var userInput = document.getElementById('userInput').value;
    if(userInput) {
        // Insert a loading spinner or message in the response display area
        document.getElementById('response-display').innerHTML = '<div class="spinner"></div>';

        fetch(`${BaseURL}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userInput })
        })
        .then(response => response.json()) // Expecting JSON response, directly parse it
        .then(data => {
            // Remove the loading message/spinner and display the response
            document.getElementById('response-display').textContent = data.response;
        })
        .catch(error => {
            console.error('Fetch error:', error);
            // Show an error message, replacing the loading message/spinner
            document.getElementById('response-display').textContent = "Error sending the request.";
        });
    } else {
        alert("Please enter a question.");
    }
});


function showToast(message) {
    // Placeholder for toast message implementation
    alert(message);
}
