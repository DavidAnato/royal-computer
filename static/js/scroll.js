// Sélectionnez les conteneurs et boutons
const newProductsContainer = document.querySelector(".product-container-new");
const prevBtnNewProducts = document.getElementById("prevBtnNewProducts");
const nextBtnNewProducts = document.getElementById("nextBtnNewProducts");
const newProductElements = document.querySelectorAll(".product-container-new .product");

const promoProductsContainer = document.querySelector(".product-container-promo");
const prevBtnPromoProducts = document.getElementById("prevBtnPromoProducts");
const nextBtnPromoProducts = document.getElementById("nextBtnPromoProducts");
const promoProductElements = document.querySelectorAll(".product-container-promo .product");

// Fonction pour recalculer le montant de défilement
function recalculateScrollAmount(elements) {
  if (!elements.length) return 0; // Si aucun produit trouvé, retournez 0
  const style = window.getComputedStyle(elements[0]);
  const margin = parseInt(style.marginLeft, 10) + parseInt(style.marginRight, 10);
  return elements[0].offsetWidth + margin;
}

// Initialisation
let scrollAmountNewProducts = recalculateScrollAmount(newProductElements);
let scrollAmountPromoProducts = recalculateScrollAmount(promoProductElements);
let scrollPositionNewProducts = 0;
let scrollPositionPromoProducts = 0;

// Recalculer lors du redimensionnement de la fenêtre
window.addEventListener("resize", () => {
  scrollAmountNewProducts = recalculateScrollAmount(newProductElements);
  scrollAmountPromoProducts = recalculateScrollAmount(promoProductElements);
});

// Fonction pour gérer le défilement
function handleScroll(container, position, amount, direction) {
  position += direction * amount;
  const maxScroll = container.scrollWidth - container.clientWidth;
  if (position < 0) position = 0;
  if (position > maxScroll) position = maxScroll;
  container.scroll({
    left: position,
    behavior: "smooth",
  });
  return position;
}

// Écouteurs pour NEW PRODUCTS
prevBtnNewProducts.addEventListener("click", () => {
  scrollPositionNewProducts = handleScroll(newProductsContainer, scrollPositionNewProducts, scrollAmountNewProducts, -1);
});
nextBtnNewProducts.addEventListener("click", () => {
  scrollPositionNewProducts = handleScroll(newProductsContainer, scrollPositionNewProducts, scrollAmountNewProducts, 1);
});

// Écouteurs pour PROMO PRODUCTS
prevBtnPromoProducts.addEventListener("click", () => {
  scrollPositionPromoProducts = handleScroll(promoProductsContainer, scrollPositionPromoProducts, scrollAmountPromoProducts, -1);
});
nextBtnPromoProducts.addEventListener("click", () => {
  scrollPositionPromoProducts = handleScroll(promoProductsContainer, scrollPositionPromoProducts, scrollAmountPromoProducts, 1);
});
