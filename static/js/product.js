const products = document.querySelectorAll(".product", );

products.forEach((product) => {
  const wrapper = product.querySelector(".single-product-wrapper");
  const wrapperHover = product.querySelector(".single-product-wrapper-hover");

  // Fonction pour gérer l'affichage en fonction de la taille de l'écran
  const handleMobileView = () => {
    if (window.innerWidth < 768) { // 768px est la largeur de l'écran mobile (md)
      wrapper.classList.add("d-none");
      wrapperHover.classList.remove("d-none");
    } else {
      wrapperHover.classList.add("d-none");
      wrapper.classList.remove("d-none");
    }
  };

  // Exécutez la fonction lors du chargement de la page
  handleMobileView();

  // Écoutez les redimensionnements de la fenêtre
  window.addEventListener("resize", handleMobileView);

  product.addEventListener("mouseenter", () => {
    if (window.innerWidth >= 768) {
      wrapperHover.classList.remove("d-none");
      wrapper.classList.add("d-none");
    }
  });

  product.addEventListener("mouseleave", () => {
    if (window.innerWidth >= 768) {
      wrapperHover.classList.add("d-none");
      wrapper.classList.remove("d-none");
    }
  });
});

