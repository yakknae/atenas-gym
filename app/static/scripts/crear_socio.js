function validarFormulario() {
  const dni = document.getElementById("dni").value;
  const email = document.getElementById("email").value;
  const telefono = document.getElementById("telefono").value;
  const direccion = document.getElementById("direccion").value;
  const fechaNacimiento = new Date(document.getElementById("fecha_nacimiento").value);
  const hoy = new Date();

  // Validación del email
  if (!email.includes("@") || !email.includes(".")) {
    alert("Por favor, ingresa un email válido.");
    return false;
  }

  // Validación del DNI
  if (dni.length < 7 || dni.length > 8 || isNaN(dni)) {
    alert("El DNI debe ser un número válido de 7 u 8 dígitos.");
    return false;
  }

  // Validación del teléfono
  if (telefono.length < 8 || telefono.length > 15 || isNaN(telefono)) {
    alert("El número de teléfono debe ser válido y tener entre 8 y 15 dígitos.");
    return false;
  }

  // Validación de la dirección
  if (direccion.length < 5) {
    alert("La dirección debe contener al menos 5 caracteres.");
    return false;
  }

  // Validación de la fecha de nacimiento
  if (fechaNacimiento > hoy) {
    alert("La fecha de nacimiento no puede ser una fecha futura.");
    return false;
  }

  return true;
}

// Asociar la validación al formulario
document.getElementById("socioForm").onsubmit = function () {
  return validarFormulario();
};

function disableButton() {
  document.getElementById("submitButton").disabled = true;
}
