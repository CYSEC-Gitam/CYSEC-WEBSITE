
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
let question = document.querySelectorAll(".question");

question.forEach(question => {
  question.addEventListener("click", event => {
    const active = document.querySelector(".question.active");
    if (active && active !== question) {
      active.classList.toggle("active");
      active.nextElementSibling.style.maxHeight = 0;
    }
    question.classList.toggle("active");
    const answer = question.nextElementSibling;
    if (question.classList.contains("active")) {
      answer.style.maxHeight = answer.scrollHeight + "px";
    } else {
      answer.style.maxHeight = 0;
    }
  })
})





 
var swiper = new Swiper(".slide-content", {
  slidesPerView: "auto",
  spaceBetween: 25,
  loop: true,
  autoplay: true,
  autoplayTimeout: 500,
  autoplayHoverPause: true,
  centerSlide: 'true',
  fade: 'true',
  grabCursor: 'true',
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
    dynamicBullets: true,
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  breakpoints:{
      0: {
          slidesPerView: 1,
      },
      520: {
          slidesPerView: 2,
      },
      950: {
          slidesPerView: 3,
      },
  },
});
