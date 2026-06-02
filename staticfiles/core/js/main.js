// ================= SPLASH SCREEN =================

window.addEventListener("load", () => {

  const splash = document.getElementById("splash-screen");

  if (splash) {

    setTimeout(() => {

      splash.style.opacity = "0";

      setTimeout(() => {
        splash.style.display = "none";
      }, 1000);

    }, 1600);

  }

});


// ================= SMOOTH SCROLL =================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

  anchor.addEventListener("click", function (e) {

    e.preventDefault();

    const target = document.querySelector(
      this.getAttribute("href")
    );

    if (target) {

      target.scrollIntoView({
        behavior: "smooth"
      });

    }

  });

});


// ================= ACTIVE NAVBAR =================

const sections = document.querySelectorAll("section");
const navLinks = document.querySelectorAll(".nav-link");

function activateMenu() {

  let current = "home";

  sections.forEach(section => {

    const sectionTop = section.offsetTop - 200;
    const sectionHeight = section.offsetHeight;

    if (
      window.scrollY >= sectionTop &&
      window.scrollY < sectionTop + sectionHeight
    ) {

      current = section.getAttribute("id");

    }

  });

  navLinks.forEach(link => {

    link.classList.remove(
      "text-[#E8A0BF]",
      "font-semibold",
      "border-b-2",
      "border-[#E8A0BF]",
      "pb-1"
    );

    if (
      link.getAttribute("href") === `#${current}`
    ) {

      link.classList.add(
        "text-[#E8A0BF]",
        "font-semibold",
        "border-b-2",
        "border-[#E8A0BF]",
        "pb-1"
      );

    }

  });

}

// RUN ON SCROLL
window.addEventListener("scroll", activateMenu);

// RUN ON PAGE LOAD
window.addEventListener("load", activateMenu);