// Photo
// Ajoutez ce script JavaScript pour mettre à jour l'aperçu de l'image après la sélection d'un fichier
document
  .getElementById("id_profile_photo")
  .addEventListener("change", function () {
    var fileInput = this;
    var imgPreview = document.getElementById("profile-preview");

    if (fileInput.files && fileInput.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        imgPreview.src = e.target.result;
      };

      reader.readAsDataURL(fileInput.files[0]);
    }
  });

// Ajoutez le CSS directement depuis le JavaScript
var style = document.createElement("style");
style.innerHTML = `
        .image-container img {
            width: 100%;
            height: 100%;
            aspect-ratio : 1;
            object-fit: cover;
        }
    `;
document.head.appendChild(style);
