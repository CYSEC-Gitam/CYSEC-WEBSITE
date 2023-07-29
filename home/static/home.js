
const text = document.querySelector(".sec-text");

const textLoad = () => {

  setTimeout(() => {

    text.innerHTML = "for the Students";

  }, 0);

  setTimeout(() => {

    text.textContent = "by the Students";

  }, 4000);

  setTimeout(() => {

    text.textContent = "for Cybersecurity Enthusiasts";

  }, 8000);

}



textLoad();

setInterval(textLoad, 12000);


// faq js

const items = document.querySelectorAll('.accordion button');

function toggleAccordion() {
  const itemToggle = this.getAttribute('aria-expanded');

  for (i = 0; i < items.length; i++) {
    items[i].setAttribute('aria-expanded', 'false');
  }

  if (itemToggle == 'false') {
    this.setAttribute('aria-expanded', 'true');
  }
}

items.forEach((item) => item.addEventListener('click', toggleAccordion));
