(function () {
  const btnAbrirTabla = document.querySelector("#btn-tabla");
  const btnCerrarTabla = document.querySelector("#cerrar-tabla");
  const modalTabla = document.querySelector("#modal-tabla");

  if (btnAbrirTabla && modalTabla) {
    btnAbrirTabla.addEventListener("click", () => {
      try { modalTabla.showModal(); } catch (e) { /* fallback */ }
    });
  }

  if (btnCerrarTabla && modalTabla) {
    btnCerrarTabla.addEventListener("click", () => {
      try { modalTabla.close(); } catch (e) { /* fallback */ }
    });
  }

  function populateTabla(rangos) {
    if (!Array.isArray(rangos)) return;
    const tbody = document.querySelector('#tabla-body');
    if (!tbody) return;
    tbody.innerHTML = '';
    rangos.forEach(r => {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td class="score">${r.range}</td><td><span class="table-label ${r.class}">${r.label}</span></td>`;
      tbody.appendChild(tr);
    });
  }

  window._modal = { populateTabla };
})();
const btnAbrirTabla = document.querySelector("#btn-tabla");
const btnCerrarTabla = document.querySelector("#cerrar-tabla");
const modalTabla = document.querySelector("#modal-tabla");

btnAbrirTabla.addEventListener("click", () => {
  modalTabla.showModal();
});

btnCerrarTabla.addEventListener("click", () => {
  modalTabla.close();
});