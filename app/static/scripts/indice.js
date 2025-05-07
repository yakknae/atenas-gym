document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll("#socios-table-body tr");
  filas.forEach((fila, index) => {
    const celdaIndice = fila.querySelector(".indice");
    if (celdaIndice) {
      celdaIndice.textContent = index + 1; // Índice comienza en 1
    }
  });
});
