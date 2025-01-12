// Récupérer les références des champs du formulaire
const firstNameInput = document.querySelector("#first_name");
const lastNameInput = document.querySelector("#last_name");
const usernameInput = document.querySelector("#username");

// Ajouter des écouteurs d'événements sur les champs "Prénom" et "Nom"
firstNameInput.addEventListener("input", updateUsername);
lastNameInput.addEventListener("input", updateUsername);

// Fonction pour mettre à jour le champ "Nom d'utilisateur"
function updateUsername() {
  const firstName = firstNameInput.value.trim().toLowerCase();
  const lastName = lastNameInput.value.trim().toLowerCase();

  // Générer un nombre aléatoire entre 1 et 100
  const randomNum = Math.floor(Math.random() * 100) + 1;

  // Créer différentes variations du nom d'utilisateur
  const usernameVariations = [
    `${firstName}${randomNum}${lastName}`, // david1anato
    `${lastName}${randomNum}${firstName}`, // anato1david
    `${firstName}.${lastName}`, // david.anato
    `${lastName}.${firstName}`, // anato.david
    `${firstName}${randomNum}`, // david1
    `${lastName}${randomNum}`, // anato1
    `${firstName.charAt(0)}${lastName}${randomNum}`, // danato1 (première lettre du prénom + nom de famille)
    `${lastName.charAt(0)}${firstName}${randomNum}`, // adavid1 (première lettre du nom de famille + prénom)
    `${firstName}${lastName}`, // davidanato
    `${lastName}${firstName}`, // anatodavid
  ];

  // Choix aléatoire d'une variation du nom d'utilisateur
  const randomIndex = Math.floor(Math.random() * usernameVariations.length);
  const username = usernameVariations[randomIndex];

  // Mettre à jour la valeur du champ "Nom d'utilisateur"
  usernameInput.value = username;
}
