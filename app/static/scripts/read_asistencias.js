document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM completamente cargado");

  // Función para cargar todas las asistencias al cargar la página
  function cargarAsistencias() {
    fetch("/asistencias")
      .then((response) => response.json())
      .then((data) => {
        console.log(data); // Imprime la respuesta completa
        const tableBody = document.getElementById("asistencias-table").querySelector("tbody");
        tableBody.innerHTML = ""; // Limpiar tabla

        data.forEach((asistencia) => {
          if (asistencia.socio && asistencia.socio.nombre && asistencia.socio.apellido) {
            const row = document.createElement("tr");
            row.innerHTML = `
        <td>${asistencia.id || "No disponible"}</td>
        <td>${asistencia.socio.nombre || "No disponible"}</td>
        <td>${asistencia.socio.apellido || "No disponible"}</td>
        <td>${asistencia.fecha || "No disponible"}</td>
        <td>${asistencia.hora || "No disponible"}</td>
      `;
            tableBody.appendChild(row);
          } else {
            console.error("Socio no encontrado en la asistencia:", asistencia);
          }
        });
      })
      .catch((error) => {
        console.error("Error al cargar asistencias:", error);
      });
  }

  // Cargar asistencias al iniciar
  cargarAsistencias();

  // Función para mostrar y ocultar formularios
  window.toggleForm = function (formId) {
    // Ocultar todos los formularios antes de mostrar el seleccionado
    const allForms = document.querySelectorAll(".form-container");
    allForms.forEach((form) => {
      form.style.display = "none"; // Ocultar todos los formularios
    });

    // Mostrar el formulario seleccionado
    const form = document.getElementById(formId);
    if (form) {
      form.style.display = "block"; // Mostrar el formulario
    } else {
      console.error(`Formulario con ID ${formId} no encontrado.`);
    }
  };

  // Generar informe para un socio
  document.getElementById("searchForm")?.addEventListener("submit", (event) => {
    event.preventDefault(); // Evita la recarga de la página
    const socio = document.getElementById("socioName").value;
    if (!socio) {
      alert("Por favor, ingrese un nombre o apellido para buscar.");
      return;
    }
    fetch(`/read_asistencias/informe?socio=${socio}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("No se pudo generar el informe");
        }
        return response.text();
      })
      .then((html) => {
        document.body.innerHTML = html; // Reemplaza el contenido con el informe
      })
      .catch((error) => console.error("Error al generar el informe:", error));
  });

  // Limpiar filtros
  document.getElementById("clear-filters")?.addEventListener("click", () => {
    // Limpiar los campos de filtro
    document.getElementById("socioName").value = "";
    document.getElementById("filterDate").value = "";

    // Realizar una nueva petición a la API para obtener todas las asistencias
    fetch("/asistencias")
      .then((response) => response.json())
      .then((data) => {
        // Llamar a una función para volver a cargar la tabla con los datos obtenidos
        cargarAsistencias(); // Recarga la tabla con todos los datos
      })
      .catch((error) => {
        console.error("Error al limpiar los filtros:", error);
      });
  });

  // Función para ordenar la tabla por una columna específica
  function ordenarTabla(campo) {
    const tbody = document.getElementById("asistencias-table-body");
    const filas = Array.from(tbody.querySelectorAll("tr"));
    const ordenAscendente = tbody.dataset.orden !== campo; // Alterna entre ascendente y descendente

    let indexColumna;
    if (campo === "nombre") {
      indexColumna = 2; // Columna "Nombre" está en la segunda posición
    } else if (campo === "apellido") {
      indexColumna = 3; // Columna "Apellido" está en la tercera posición
    } else {
      return; // Si el campo no es "nombre" ni "apellido", no hace nada
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

    tbody.dataset.orden = ordenAscendente ? campo : "";

    filas.forEach((fila) => tbody.appendChild(fila));
  }

  // Asignar evento click a las cabeceras de la tabla
  document
    .getElementById("orden-tabla-nombre")
    .addEventListener("click", () => ordenarTabla("nombre"));
  document
    .getElementById("orden-tabla-apellido")
    .addEventListener("click", () => ordenarTabla("apellido"));

  // Filtrar asistencias por fecha
  document.getElementById("filterForm")?.addEventListener("submit", (event) => {
    event.preventDefault(); // Evita la recarga de la página
    const fecha = document.getElementById("filterDate").value;
    if (!fecha) {
      alert("Por favor, seleccione una fecha para filtrar.");
      return;
    }

    fetch(`/read_asistencias/filtrar?fecha=${fecha}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("No se pudo filtrar las asistencias");
        }
        return response.text(); // Recibir la nueva página completa como texto HTML
      })
      .then((html) => {
        // Reemplazar todo el contenido del body
        const newDocument = new DOMParser().parseFromString(html, "text/html");
        document.body.innerHTML = newDocument.body.innerHTML;
      })
      .catch((error) => console.error("Error al filtrar asistencias:", error));
  });
});
