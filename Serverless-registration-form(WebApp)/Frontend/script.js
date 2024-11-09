function submitForm() {
    event.preventDefault();

    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const password = document.getElementById('password').value;

    // Create request object
    const xhr = new XMLHttpRequest();

    // Set up request
    xhr.open('POST', 'API_INVOKE_URL/register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Set up response handler
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                alert('Registration successful!');
                document.getElementById('name').value = '';
                document.getElementById('email').value = '';
                document.getElementById('phone').value = '';
                document.getElementById('password').value = '';
            } else {
                alert('Registration failed: ' + xhr.responseText);
            }
        }
    };

    // Send request
    xhr.send(JSON.stringify({
        name: name,
        email: email,
        phone: phone,
        password: password
    }));
}
