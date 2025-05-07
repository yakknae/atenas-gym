document.getElementById("asistencia-form").addEventListener("submit", (e) => {
  e.preventDefault();

  const socioId = document.getElementById("socio").value;
  const fecha = new Date().toISOString().split("T")[0]; // Fecha en formato YYYY-MM-DD

  // Obtener la hora en la zona horaria de Buenos Aires (America/Argentina/Buenos_Aires)
  const options = {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  };
  const hora = new Date().toLocaleTimeString("es-AR", options);

  console.log({
    socio_id: socioId,
    fecha: fecha,
    hora: hora, // Hora en formato HH:MM:SS
  });

  fetch("/crear_asistencia", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      socio_id: parseInt(socioId, 10),
      fecha: fecha,
      hora: hora, // Enviamos la hora con la zona horaria de Buenos Aires
    }),
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al registrar la asistencia");
      return response.json();
    })
    .then((data) => {
      alert(data.message);
    })
    .catch((error) => {
      console.error("Error al registrar la asistencia:", error);
      alert("No se pudo registrar la asistencia.");
    });
});
