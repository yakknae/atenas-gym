function actualizarCobro(idCobro) {
  // Obtener el valor de la fecha de pago desde el campo de entrada
  const fechaPagoInput = document.getElementById(`fecha_pago_${idCobro}`);
  const fechaPago = fechaPagoInput ? fechaPagoInput.value : "";

  // Validación de la fecha de pago
  if (!fechaPago) {
    alert("Por favor complete la fecha de pago.");
    return;
  }

  // Enviar la solicitud a la nueva ruta
  fetch(`/actualizar_pago/${idCobro}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Mostrar el formulario para actualizar la fecha de pago
        const formContainer = document.getElementById("formulario_actualizacion");
        formContainer.innerHTML = `
                <h2>Actualizar Pago</h2>
                <form id="formActualizarPago">
                  <label for="fecha_pago">Fecha de Pago:</label>
                  <input type="date" id="fecha_pago" name="fecha_pago" required>
                  <input type="hidden" id="id_pago" value="${idCobro}">
                  <button type="submit">Actualizar</button>
                </form>
              `;
      } else {
        alert("Error al obtener el formulario para actualizar el pago.");
      }
    })
    .catch((error) => {
      console.error("Error al intentar obtener el formulario:", error);
      alert("Error al obtener el formulario para actualizar el pago.");
    });
}
