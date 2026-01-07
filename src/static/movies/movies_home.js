function removeGenre(element) {
    // change the value of the genre to false
    const elementID = '#check' + element;
    document.querySelector(elementID).checked = false;
    // submit the form with the changed value
    document.querySelector(".form").submit();
}