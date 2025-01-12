// Fonction pour activer la navigation par onglets
function activateTab(tabId) {
    // Désactive tous les onglets et les contenus
    const tabs = document.querySelectorAll(".nav-link");
    tabs.forEach((tab) => {
      tab.classList.remove("active");
    });
  
    const tabContents = document.querySelectorAll(".tab-pane");
    tabContents.forEach((content) => {
      content.classList.remove("show", "active");
    });
  
    // Active l'onglet et le contenu correspondants
    const activeTab = document.querySelector(`#${tabId}`);
    if (activeTab) {
      activeTab.classList.add("show", "active");
      const correspondingNavLink = document.querySelector(`[href="#${tabId}"]`);
      if (correspondingNavLink) {
        correspondingNavLink.classList.add("active");
      }
    }
  }
  
  // Ajoutez un écouteur d'événement pour chaque lien d'onglet
  const tabLinks = document.querySelectorAll(".pill-nav-link");
  tabLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault(); // Empêche le comportement par défaut du lien
      const tabId = link.getAttribute("href").substring(1); // Récupère l'identifiant de l'onglet
      activateTab(tabId); // Active l'onglet correspondant
    });
  });
  
  // Active le premier onglet au chargement de la page
  activateTab("ex1-pills-1");
  