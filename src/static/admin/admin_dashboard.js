// re-enable the input element to edit the genre title when the button edit is clicked
document.getElementById("editGenreTitleButton").addEventListener('click', function () {
    document.getElementById("genreTitle").disabled = false;
    document.getElementById("genreTitle").style = "";
});

// re-enable the text area element to edit the genre description when the button edit is clicked
document.getElementById("editGenreDescriptionButton").addEventListener('click', function () {
    document.getElementById("genreBody").disabled = false;
    document.getElementById("genreBody").style = "resize: none;"
})

// reset the input element when the genre modal is hidden
document.getElementById("updateGenreModal").addEventListener('hide.bs.modal', event => {
    // reset the input element
    document.getElementById("genreTitle").disabled = true;
    document.getElementById("genreTitle").style = "border: none; outline: none; background: transparent; width: auto;";

    // reset the text area element
    document.getElementById("genreBody").disabled = true;
    document.getElementById("genreBody").style = "border: none; outline: none; background: transparent; resize: none;"
});

// reset elements when the adding a new genre modal is hidden
document.getElementById("addGenreModal").addEventListener('hide.bs.modal', event => {
    // clear errors
    document.getElementById("addGenreErrorContainer").classList.add("d-none");
    document.getElementById("addGenreErrorSpan").textContent = "";

    // clear inputs
    document.getElementById("addGenreTitle").value = "";
    document.getElementById("addGenreDescription").value = "";
});

// load the below after all the JavaScripts stuff has been loaded
document.addEventListener('DOMContentLoaded', function () {
    // get the genre modal
    const genreModal = new bootstrap.Modal(document.getElementById("updateGenreModal"));

    // update the genre modal data
    const genreButtons = document.querySelectorAll(".genre-btn");
    genreButtons.forEach(button => {
        button.addEventListener('click', function () {
            document.getElementById("genreTitle").value = button.dataset.genreName;
            document.getElementById("genreBody").value = button.dataset.genreDescription;
            document.getElementById("genreId").value = button.dataset.genreId;
        });
    });

    // get the delete genre modal 
    const deleteGenreModal = new bootstrap.Modal(document.getElementById("deleteGenreModal"));

    // update the delete genre modal data
    const genreDelButtons = document.querySelectorAll(".del-genre-btn");
    genreDelButtons.forEach(button => {
        button.addEventListener('click', function () {
            document.getElementById("delGenreId").value = button.dataset.genreId;
        });
    });
});

// ajax request for add genre submission
document.getElementById("addGenreForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent the default submission

    // disable submit button
    const submitButton = document.getElementById("addGenreButton");
    submitButton.disabled = true;

    // get the form data
    const form = event.target;
    const formData = new FormData(form);
    var obj = {};
    formData.forEach(function (value, key) {
        obj[key] = value;
    });
    var json = JSON.stringify(obj);

    // perform an ajax request
    try {
        // get the required variables
        const url = '/admin/add-genre'; // "{{ url_for('admin.add_genre') }}"
        const csrfToken = document.getElementById('addGenreCSRFToken').value;

        // request
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        })
        const result = await response.json();
        if (result['status'] == "FAIL") {

            document.getElementById("addGenreErrorContainer").classList.remove("d-none");
            document.getElementById("addGenreErrorSpan").textContent = "ERROR: " + result['message'];

            // re-enable the submit button
            submitButton.disabled = false;

        } else if (result['status'] == "SUCCESS") {

            // show message
            document.getElementById("addGenreErrorContainer").classList.remove("d-none");
            document.getElementById("addGenreErrorContainer").classList.remove("border-danger");
            document.getElementById("addGenreErrorContainer").classList.add("border-success");
            document.getElementById("addGenreErrorSpan").textContent = result["message"];

            // submit button remains disabled to prevent duplication
            // reload the page after a short time pause
            console.log("added new genre successfully!");
            setTimeout(() => {
                location.reload();
            }, 750); // 0.75 seconds delay to show success
        } else {
            console.error("Error in adding a new genre. Please refresh the page.")
        }

    } catch (error) {
        console.error("AJAX Error: " + error);
    }
});

// ajax request to update genre
document.getElementById("updateGenreForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent the default action of submitting the form

    const submitButton = document.getElementById("updateGenreButton");
    submitButton.disabled = true;

    // enable genre body so that the content is sent/posted to the server
    document.getElementById("genreTitle").disabled = false;
    document.getElementById("genreBody").disabled = false;

    // get the form data
    const form = event.target;
    const formData = new FormData(form);
    var obj = {};
    formData.forEach(function (value, key) {
        obj[key] = value;
    });
    var json = JSON.stringify(obj);

    try {
        // get the required variables
        // const url = "{{ url_for('admin.update_genre', genre_id='') }}" + document.getElementById("genreId").value;
        const url = '/admin/update-genre/' + document.getElementById("genreId").value;
        const csrfToken = document.getElementById('editGenreCSRFToken').value;

        // request
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        })
        const result = await response.json();
        console.log(result);
        if (result['status'] == "FAIL") {

            document.getElementById("editGenreErrorContainer").classList.remove("d-none");
            document.getElementById("editGenreErrorSpan").textContent = "ERROR: " + result['message'];

            // re-enable the submit button
            submitButton.disabled = false;

        } else if (result['status'] == "SUCCESS") {

            // show message
            document.getElementById("editGenreErrorContainer").classList.remove("d-none");
            document.getElementById("editGenreErrorContainer").classList.remove("border-danger");
            document.getElementById("editGenreErrorContainer").classList.add("border-success");
            document.getElementById("editGenreErrorSpan").textContent = result["message"];

            // submit button remains disabled to prevent duplication
            // reload the page after a short time pause
            console.log("updated genre successfully!");
            setTimeout(() => {
                location.reload();
            }, 750); // 0.75 seconds delay to show success
        } else {
            console.error("Error in adding a new genre. Please refresh the page.")
        }

    } catch (error) {
        console.error("AJAX error: " + error);
    }
});

// ajax request to delete genre
document.getElementById("deleteGenreForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // prevent the default action of submitting the form

    const submitButton = document.getElementById("deleteGenreButton");
    submitButton.disabled = true;

    try {
        // const url = "{{ url_for('admin.delete_genre', genre_id='') }}" + document.getElementById("delGenreId").value;
        const url = '/admin/delete-genre/' + document.getElementById("delGenreId").value;

        // send the request
        const csrfToken = document.getElementById("deleteGenreCSRFToken").value;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });
        const result = await response.json(); // parse the result! important to use "await"!

        if (result["status"] == "FAIL") {
            document.getElementById("deleteGenreErrorContainer").classList.remove("d-none");
            document.getElementById("deleteGenreErrorSpan").textContent = "ERROR: " + result["message"] + ". Please refresh the page.";

        } else if (result['status'] == "SUCCESS") {
            // show message
            document.getElementById("deleteGenreErrorContainer").classList.remove("d-none");
            document.getElementById("deleteGenreErrorContainer").classList.remove("border-danger");
            document.getElementById("deleteGenreErrorContainer").classList.add("border-success");
            document.getElementById("deleteGenreErrorSpan").textContent = result["message"];

            // enable the submit button
            submitButton.disabled = true;

            console.log("delete genre successfully!");

            // reload the page after a short time pause
            setTimeout(() => {
                location.reload();
            }, 750); // 0.75 seconds delay to show success
        } else {
            console.error("Received an unexpected API response from " + url);
        }
    } catch (error) {
        console.error("AJAX Error: " + error);
    }
});