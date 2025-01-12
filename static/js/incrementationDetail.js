// JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const decrementButton = document.getElementById('decrementButton');
    const incrementButton = document.getElementById('incrementButton');
    const quantityInput = document.getElementById('quantityInput');

    // Gestion de la réduction de la quantité
    decrementButton.addEventListener('click', function() {
        let quantity = parseInt(quantityInput.value);
        if (quantity > 1) {
            quantity--;
            quantityInput.value = quantity;
        }
    });

    // Gestion de l'augmentation de la quantité
    incrementButton.addEventListener('click', function() {
        let quantity = parseInt(quantityInput.value);
        quantity++;
        quantityInput.value = quantity;
    });
});
