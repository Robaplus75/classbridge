// add hovered class to selected list item
let list = document.querySelectorAll(".navigation li");

function activeLink() {
  list.forEach((item) => {
    item.classList.remove("hovered");
  });
  this.classList.add("hovered");
}

//list.forEach((item) => item.addEventListener("mouseover", activeLink));

// Menu Toggle
let toggle = document.querySelector(".toggle");
let navigation = document.querySelector(".navigation");
let main = document.querySelector(".main");

toggle.onclick = function () {
  navigation.classList.toggle("active");
  main.classList.toggle("active");
};

// Get all the navigation links
const navLinks = document.querySelectorAll('.navigation li a');

// Add click event listener to each link
navLinks.forEach(link => {
  // Check if the link URL matches the current URL on page load
  
  if (link.href === window.location.href) {
    link.parentNode.classList.add('currentPage');
  }
});

