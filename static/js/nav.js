// Seuil de défilement pour la barre de navigation
const seuilDeDefilementNav = 220;

// Seuil de défilement pour le lien circulaire
const seuilDeDefilementlinkTop = 300;

// Nav
const nav = document.querySelector(".navbar");
const linkTop = document.querySelector(".go-top-link");

window.addEventListener("scroll", () => {
  const positionDeDefilement = window.scrollY;

  // Animation de la barre de navigation
  if (
    positionDeDefilement >= seuilDeDefilementNav &&
    !nav.classList.contains("sticky-top")
  ) {
    nav.classList.add("shadow-bottom");
    nav.style.animation = "slideIn 0.3s ease-in-out";
    nav.classList.add("sticky-top");
  } else if (
    positionDeDefilement < seuilDeDefilementNav &&
    nav.classList.contains("sticky-top")
  ) {
    nav.classList.remove("shadow-bottom");
    nav.style.animation = "slideOut 0.3s ease-in-out";
    setTimeout(() => {
      nav.classList.remove("sticky-top");
      nav.style.animation = "";
    }, 300);
  }

  // Animation du lien top
  if (positionDeDefilement >= seuilDeDefilementlinkTop) {
    linkTop.classList.remove("d-none");
  } else {
    linkTop.style.animation = "slide-out 0.3s forwards";
    setTimeout(() => {
      linkTop.classList.add("d-none");
      linkTop.style.animation = "";
    }, 300);
  }
});


const scrollToTop = () => {
  preventDefault();
  stopPropagation();
  window.scrollTo({ top: 0, behavior: "smooth" });
};


