// Get hamburger button
const hamburger = document.getElementById("hamburger");

// Get nav links
const navLinks = document.getElementById("navLinks");


// When hamburger is clicked
hamburger.addEventListener("click", () => {

    navLinks.classList.toggle("active");

});