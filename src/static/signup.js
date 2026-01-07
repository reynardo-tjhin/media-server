document.getElementById("signUpForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent form normal form submission

    const submitButton = document.getElementById("signUpButton");

    const form = event.target;
    const formData = new FormData(form);
    var obj = {};
    formData.forEach(function (value, key) {
        obj[key] = value;
    });
    var json = JSON.stringify(obj);

    try {
        const url = "{{ url_for('auth.check_signup_details') }}";
        const csrfToken = document.getElementById("signUpCSRFToken").value;
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        });
        const result = await response.json();

        if (result['status'] == 'FAIL') {
            // show error
            document.getElementById("signUpErrorContainer").classList.remove("d-none");
            document.getElementById("signUpErrorSpan").textContent = "ERROR: " + result["message"];

            // re-enable sign in button
            submitButton.disabled = false;

        } else if (result['status'] == 'SUCCESS') {
            // show success message
            document.getElementById("signUpErrorContainer").classList.remove("d-none");
            document.getElementById("signUpErrorContainer").classList.remove("border-danger");
            document.getElementById("signUpErrorContainer").classList.add("border-success");
            document.getElementById("signUpErrorSpan").textContent = result["message"];

            // pause a bit
            setTimeout(() => {
                // redirect to the homepage
                window.location.href = '/'; // "{{ url_for('home.home') }}";
            }, 750); // 0.75 seconds delay to show success

        } else {
            console.error("Error from server");
        }

    } catch (error) {
        console.error("AJAX Error: " + error);
    }
});