// for inputing the release date
flatpickr("#datepicker", {
    dateFormat: "Y-m-d",
});

// scroll to the top upon refresh/reload page
if (history.scrollRestoration) {
    history.scrollRestoration = 'manual';
} else {
    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }
}

// run the function after all the previous scripts have been loaded
document.addEventListener('DOMContentLoaded', function () {
    // get the modal
    const deleteModal = new bootstrap.Modal(document.getElementById("deleteMovie"));

    // update the delete movie button's data
    const deleteButtons = document.querySelectorAll(".delete-button");
    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            // extract data from button attribtues
            let baseUrl = "{{ url_for('admin.delete_movie', movie_id='') }}"
            baseUrl = baseUrl + button.dataset.movieId

            // assign the url to the action of the button
            document.getElementById('deleteMovieForm').action = baseUrl;

            // show the delete modal
            deleteModal.show();
        });
    });

    // clear any error lists when the update modal is hidden
    document.getElementById("updateMovie").addEventListener('hide.bs.modal', event => {
        document.getElementById("updateMovieErrorContainer").classList.add("d-none");
        document.getElementById("updateMovieErrorSpan").textContent = "";
    });

    // clear any error lists and input data when the add modal is hidden
    document.getElementById("addNewMovie").addEventListener('hide.bs.modal', event => {
        // error messages
        document.getElementById("addMovieErrorContainer").classList.add("d-none");
        document.getElementById("addMovieErrorSpan").textContent = "";

        // input data
        document.getElementById("movieName").value = "";
        document.getElementById("movieDescription").value = "";
        document.getElementById("mediaLocation").value = "";
        document.getElementById("posterLocation").value = "";
        document.getElementById("duration").value = "";
        document.getElementById("imdbRating").value = "";
        document.getElementById("rottenTomatoesRating").value = "";
        document.getElementById("metacriticRating").value = "";

        // reset the calendar
        let calendar = flatpickr(document.querySelectorAll(".add-movie-release-date")[0], {});
        calendar.clear();

        // clears all the genres
        document.querySelectorAll(".add-movie-checkbox").forEach((element) => {
            element.checked = false;
        });
    });

    // update the update movie modal's data
    const updateModal = new bootstrap.Modal(document.getElementById("updateMovie"));
    const updateButtons = document.querySelectorAll(".update-button");
    updateButtons.forEach(button => {
        button.addEventListener('click', function () {

            // update the action of the form
            let baseUrl = "{{ url_for('admin.update_movie', movie_id='') }}";
            baseUrl = baseUrl + button.dataset.movieId;
            document.getElementById("updateMovieForm").action = baseUrl;

            // update the rest of the data
            document.getElementById("updateMovieId").value = button.dataset.movieId;
            document.getElementById("updateMovieName").value = button.dataset.movieName;
            document.getElementById("updateMovieDescription").value = button.dataset.movieDescription;
            document.getElementById("updateMediaLocation").value = button.dataset.movieMediaLocation;
            document.getElementById("updatePosterLocation").value = button.dataset.moviePosterLocation;
            document.getElementById("updateDuration").value = button.dataset.movieDuration;
            document.getElementById("updateImdbRating").value = button.dataset.movieImdbRating;
            document.getElementById("updateRottenTomatoesRating").value = button.dataset.movieRottenTomatoesRating;
            document.getElementById("updateMetacriticRating").value = button.dataset.movieMetacriticRating;

            // update the release date
            let calendar = flatpickr(document.querySelectorAll(".update-movie-release-date")[0], {});
            calendar.setDate(button.dataset.movieReleaseDate, true, 'Y-m-d');

            // update the genres
            const movieGenres = button.dataset.movieGenres;
            if (movieGenres != 'No genres') {
                movieGenres.split(",").forEach(genre => {
                    document.getElementById("update" + genre.trimStart()).checked = true;
                });
            }

            updateModal.show();
        });
    });
});

// perform an ajax request on adding a new movie
document.getElementById("addNewMovieForm").addEventListener('submit', async function (event) {
    event.preventDefault(); // stop the normal form submission

    // disable the submit button to prevent another submission
    const submitButton = document.getElementById("addNewMovieSubmitButton");
    submitButton.disabled = true;

    // get the form data and parase it as json format
    const form = event.target;
    const formData = new FormData(form);
    var obj = {}
    formData.forEach(function (value, key) {
        obj[key] = value;
    });
    var json = JSON.stringify(obj);

    try {
        const url = "{{ url_for('admin.add_movie') }}";

        // send the request
        const csrfToken = document.getElementById("addNewMovieCSRFToken").value;
        console.log(csrfToken);
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        })
        const result = await response.json();
        if (result["status"] == "FAIL") {
            document.getElementById("addMovieErrorContainer").classList.remove("d-none");
            document.getElementById("addMovieErrorSpan").textContent = "ERROR: " + result["message"];

            // enable the submit button
            submitButton.disabled = false;

            // scroll to the top of the modal
            document.getElementById("addMovieModalContent").scrollTop = 0;

        } else if (result['status'] == "SUCCESS") {
            // show message
            document.getElementById("addMovieErrorContainer").classList.remove("d-none");
            document.getElementById("addMovieErrorContainer").classList.remove("border-danger");
            document.getElementById("addMovieErrorContainer").classList.add("border-success");
            document.getElementById("addMovieErrorSpan").textContent = result["message"];

            // enable the submit button
            submitButton.disabled = true;

            // scroll to the top of the modal
            document.getElementById("addMovieModalContent").scrollTop = 0;

            // reload the page after a short time pause
            console.log("update movie successfully!");
            setTimeout(() => {
                location.reload();
            }, 750); // 0.75 seconds delay to show success
        } else {
            console.error("Received an unexpected API response from " + url);
        }

    } catch (error) {
        console.error("AJAX error: " + error);
    }
});

// perform an ajax request on deleting a movie
document.getElementById('deleteMovieForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // stop the normal form submission

    // disable the submit button to prevent from additional submission
    const submitButton = document.getElementById("deleteMovieButton");
    submitButton.disabled = true;

    try {
        const url = document.getElementById('deleteMovieForm').action;

        // send the request
        const csrfToken = document.getElementById("deleteMovieCSRFToken").value;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        });
        const result = await response.json(); // parse the result! important to use "await"!

        if (result["status"] == "FAIL") {
            document.getElementById("deleteMovieErrorContainer").classList.remove("d-none");
            document.getElementById("deleteMovieErrorSpan").textContent = "ERROR: " + result["message"] + ". Please refresh the page.";
        } else if (result['status'] == "SUCCESS") {
            // show message
            document.getElementById("deleteMovieErrorContainer").classList.remove("d-none");
            document.getElementById("deleteMovieErrorContainer").classList.remove("border-danger");
            document.getElementById("deleteMovieErrorContainer").classList.add("border-success");
            document.getElementById("deleteMovieErrorSpan").textContent = result["message"];

            // enable the submit button
            submitButton.disabled = true;

            console.log("delete movie successfully!");

            // reload the page after a short time pause
            setTimeout(() => {
                location.reload();
            }, 750); // 0.75 seconds delay to show success
        } else {
            console.error("Received an unexpected API response from " + url);
        }
    } catch (error) {
        console.error("AJAX error: " + error);
    }
});

// perform an ajax request on update movie
document.getElementById('updateMovieForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // stop the normal form submission

    // disable the button
    const submitButton = document.getElementById("updateMovieButton");
    submitButton.disabled = true;

    const form = event.target;
    const formData = new FormData(form);
    const movieId = formData.get('movieId');

    // convert form data object to json
    var object = {};
    formData.forEach(function (value, key) {
        object[key] = value;
    });
    var json = JSON.stringify(object);

    // try and fetch the from the API endpoint
    try {
        const url = "{{ url_for('admin.update_movie', movie_id='') }}" + movieId;

        // send the request
        const csrfToken = document.getElementById("updateMovieCSRFToken").value;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: json,
        });
        const result = await response.json(); // parse the result! important to use "await"!

        console.log(result['status']);
        if (result['status'] == "FAIL") {
            document.getElementById("updateMovieErrorContainer").classList.remove("d-none");
            document.getElementById("updateMovieErrorSpan").textContent = "ERROR: " + result['message'];

            // enable the submit button
            submitButton.disabled = false;

            // scroll to the top of the modal
            document.getElementById("updateMovieModalBody").scrollTop = 0;

        } else if (result['status'] == "SUCCESS") {
            // show message
            document.getElementById("updateMovieErrorContainer").classList.remove("d-none");
            document.getElementById("updateMovieErrorContainer").classList.remove("border-danger");
            document.getElementById("updateMovieErrorContainer").classList.add("border-success");
            document.getElementById("updateMovieErrorSpan").textContent = result["message"];

            // enable the submit button
            submitButton.disabled = true;

            // scroll to the top of the modal
            document.getElementById("updateMovieModalBody").scrollTop = 0;

            // reload the page after a short time pause
            console.log("update movie successfully!");
            setTimeout(() => {
                location.reload();
            }, 750); // 0.75 seconds delay to show success
        } else {
            console.error("Received an unexpected API response from " + url);
        }

    } catch (error) {
        console.error("AJAX error:", error);
    }
});