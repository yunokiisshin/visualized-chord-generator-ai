document.getElementById('generateButton').addEventListener('click', function() {
    fetch('/generate-chords', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Process the received data and update the frontend as needed
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});
