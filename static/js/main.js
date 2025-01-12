function togglePasswordVisibility(fieldID="password", iconID="password-icon") {
  const passwordInput = document.getElementById(fieldID);
  passwordInput.type = passwordInput.type === "password" ? "text" : "password";
  const passwordIcon = document.getElementById(iconID);
  passwordIcon.classList.remove("fa-eye");
  passwordIcon.classList.add("fa-eye-slash");
}


document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector(".form");
  const fields = Array.from(form.querySelectorAll(".field"));
  const submitButton = form.querySelector("button[type='submit']");
  
  // Initial Setup: Show only the first 3 fields
  fields.forEach((field, index) => {
    if (index >= 3) {
      field.style.display = "none";
      field.style.transition = "all 0.5s ease";
    }
  });

  // Replace submit button with "Next" button initially
  submitButton.innerHTML = "Suivant <i class='fas fa-arrow-down'></i>";
  submitButton.type = "button"; // Prevent form submission

  submitButton.addEventListener("click", () => {
    const hiddenFields = fields.filter(field => field.style.display === "none");
    
    if (hiddenFields.length > 0) {
      // Show remaining fields with a sliding effect
      hiddenFields.forEach((field, index) => {
        setTimeout(() => {
          field.style.display = "block";
          field.style.opacity = "0";
          field.style.transform = "translateY(-10px)";
          
          setTimeout(() => {
            field.style.opacity = "1";
            field.style.transform = "translateY(0)";
          }, 50);
        }, index * 100); // Stagger animation
      });

      // Change button to "S'inscrire"
      submitButton.innerHTML = " <i class='fas fa-user-plus fa-lg fa-fw'></i> S'inscrire";
      submitButton.type = "submit"; // Allow form submission
    }
  });
});
