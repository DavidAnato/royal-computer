// Fonction pour changer l'image ou la vidéo principale avec animation
function changeMainMedia(mediaUrl, isVideo) {
  const mainImage = document.querySelector("#mainImage");
  const mainVideo = document.querySelector("#mainVideo");

  // Cachez l'image principale si une vidéo est sélectionnée
  if (isVideo) {
    mainImage.style.display = "none";
    mainVideo.style.display = "block";
    mainVideo.setAttribute("src", mediaUrl);
  } else {
    mainVideo.style.display = "none";
    mainImage.style.display = "block";
    mainImage.setAttribute("src", mediaUrl);
  }

  // Supprimez la classe d'animation si elle est déjà appliquée
  mainImage.classList.remove("main-image-animation");
  mainVideo.classList.remove("main-image-animation");

  // Utilisez un délai pour forcer le reflow et permettre la réapplication de l'animation
  void mainImage.offsetWidth; 
  void mainVideo.offsetWidth;

  // Réappliquez la classe d'animation
  mainImage.classList.add("main-image-animation");
  mainVideo.classList.add("main-image-animation");
}

// Sélectionnez toutes les miniatures d'images et vidéos
const thumbnails = document.querySelectorAll(".mini-image");
const playIcons = document.querySelectorAll(".play-icon");

// Ajoutez un écouteur d'événements à chaque miniature (image ou vidéo)
thumbnails.forEach((thumbnail) => {
  thumbnail.addEventListener("click", () => {
    const isVideo = thumbnail.tagName.toLowerCase() === "video"; // Vérifiez si c'est une vidéo
    const mediaUrl = thumbnail.getAttribute("src");

    // Changez l'image ou la vidéo principale avec l'animation
    changeMainMedia(mediaUrl, isVideo);
  });
});

// Ajoutez un écouteur d'événements à chaque icône de lecture
playIcons.forEach((icon) => {
  icon.addEventListener("click", (event) => {
    // Empêche la propagation de l'événement pour ne pas interférer avec l'image
    event.stopPropagation();

    // Trouver la vidéo correspondante à l'icône play
    const videoElement = icon.closest("a").querySelector("video");
    const videoUrl = videoElement.getAttribute("src");

    // Change l'élément principal en vidéo (sans jouer)
    changeMainMedia(videoUrl, true);
  });
});
