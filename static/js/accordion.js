document.addEventListener("DOMContentLoaded", function () {
    const accordionButtons = document.querySelectorAll(".accordion-button");
  
    // Ajoutez un gestionnaire d'événements pour chaque bouton du menu d'accordéon
    accordionButtons.forEach((button) => {
      button.addEventListener("click", function () {
        // Fermez toutes les sections du menu d'accordéon
        accordionButtons.forEach((otherButton) => {
          if (otherButton !== button) {
            const target = document.querySelector(
              otherButton.getAttribute("data-bs-target")
            );
            if (target.classList.contains("show")) {
              const bsCollapse = new bootstrap.Collapse(target);
              bsCollapse.hide();
            }
          }
        });
      });
    });
  });
  