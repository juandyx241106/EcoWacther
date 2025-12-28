document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("form-registro").addEventListener("submit", function (e) {
        const password = document.getElementById("contraseña").value;
        const confirmPassword = document.getElementById("confirmar_contraseña").value;
        const error = document.getElementById("error-password");

        if (password !== confirmPassword) {
            e.preventDefault();
            error.style.display = "block";
        } else {
            error.style.display = "none";
        }
    });
});
