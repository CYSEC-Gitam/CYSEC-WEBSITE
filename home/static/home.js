
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