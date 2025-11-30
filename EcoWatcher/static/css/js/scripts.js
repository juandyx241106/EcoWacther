const btnAbrirTabla = document.querySelector("#btn-tabla");
const btnCerrarTabla = document.querySelector("#cerrar-tabla");
const modalTabla = document.querySelector("#modal-tabla");

btnAbrirTabla.addEventListener("click", () => {
  modalTabla.showModal();
});

btnCerrarTabla.addEventListener("click", () => {
  modalTabla.close();
});