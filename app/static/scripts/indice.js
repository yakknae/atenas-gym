//Tabla socios
document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll("#socios-table-body tr");
  filas.forEach((fila, index) => {
    const celdaIndice = fila.querySelector(".indice");
    if (celdaIndice) {
      celdaIndice.textContent = index + 1; // Índice comienza en 1
    }
  });
});

//Tabla planes sociales
document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll("#planes-table-body tr");
  filas.forEach((fila, index) => {
    const celdaIndice = fila.querySelector(".indice");
    if (celdaIndice) {
      celdaIndice.textContent = index + 1; // Índice comienza en 1
    }
  });
});

//Tabla combos
document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll("#combos-table-body tr");
  filas.forEach((fila, index) => {
    const celdaIndice = fila.querySelector(".indice");
    if (celdaIndice) {
      celdaIndice.textContent = index + 1;
    }
  });
});
//Tabla pagos
document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll("#pagos-table-body tr");
  filas.forEach((fila, index) => {
    const celdaIndice = fila.querySelector(".indice");
    if (celdaIndice) {
      celdaIndice.textContent = index + 1;
    }
  });
});
//Tabla asistencias
document.addEventListener("DOMContentLoaded", function () {
  const filas = document.querySelectorAll("#asistencias-table-body tr");
  filas.forEach((fila, index) => {
    const celdaIndice = fila.querySelector(".indice");
    if (celdaIndice) {
      celdaIndice.textContent = index + 1;
    }
  });
});
