function showDeleteForm(id) {
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteForm").style.display = "block";
}

function hideDeleteForm() {
  document.getElementById("deleteForm").style.display = "none";
}

function ordenarTabla(campo) {
  const tbody = document.getElementById("socios-table-body");
  const filas = Array.from(tbody.querySelectorAll("tr"));
  const ordenAscendente = tbody.dataset.orden !== campo; // Alterna orden

  // Seleccionar la columna correcta con base en 'campo'
  let indexColumna = 0; // Default si campo no coincide
  if (campo === "nombre") {
    indexColumna = 2; // Columna "Nombre" está en la segunda posición
  } else if (campo === "apellido") {
    indexColumna = 3; // Columna "Apellido" está en la tercera posición
  }

  filas.sort((filaA, filaB) => {
    const celdaA = filaA
      .querySelector(`td:nth-child(${indexColumna})`)
      .textContent.trim()
      .toLowerCase();
    const celdaB = filaB
      .querySelector(`td:nth-child(${indexColumna})`)
      .textContent.trim()
      .toLowerCase();

    if (celdaA < celdaB) return ordenAscendente ? -1 : 1;
    if (celdaA > celdaB) return ordenAscendente ? 1 : -1;
    return 0;
  });

  // Alternar orden y actualizar el atributo data-orden
  tbody.dataset.orden = ordenAscendente ? campo : "";

  // Remover y reinsertar filas ordenadas
  filas.forEach((fila) => tbody.appendChild(fila));
}

function eliminarSocio() {
  const socioId = document.getElementById("deleteId").value;

  fetch(`/socios/${socioId}/eliminar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al eliminar el socio");
      }
      return response.text();
    })
    .then(() => {
      document.getElementById(`socio-${socioId}`).remove();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al eliminar el socio: " + error.message);
    })
    .finally(() => {
      hideDeleteForm();
    });
}
