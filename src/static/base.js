document.addEventListener("DOMContentLoaded", async function () {
    // check whether the user is logged in/logged out
    try {
        const url = '/auth/is-logged-in'; // "{{ url_for('auth.is_logged_in') }}";
        const response = await fetch(url, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();

        // user is logged in
        if (result["message"] == "True") {
            document.getElementById("sign-up-sign-in-btn").classList.add("d-none"); // hide sign up/sign in button
            document.getElementById("account-btn").classList.remove("d-none"); // show account button

            // user is logged out
        } else if (result["message"] == "False") {
            document.getElementById("sign-up-sign-in-btn").classList.remove("d-none"); // show sign up/sign in button
            document.getElementById("account-btn").classList.add("d-none"); // hide account button

        } else {
            console.error("Error from the server side not showing the correct response.");
        }
    } catch (error) {
        console.error("AJAX error: " + error);
    }

    // get the username
    try {
        const url = '/auth/username'; // "{{ url_for('auth.get_username') }}";
        const response = await fetch(url, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
            }
        });
        const result = await response.json();
        if (result['status'] == 'SUCCESS') {
            document.getElementById("accountName").textContent = result["message"];
        } else if (result['status'] == 'FAIL') {
            console.log("Get username: not signed in, hence ignore...");
        } else {
            console.error("Get username: Error from the server side not showing the correct response.");
        }
    } catch (error) {
        console.error("AJAX error:" + error);
    }
});