function validar() {
  const dias = document.getElementById("dias").value;
  const precio = document.getElementById("precio").value;
  // Validación de dias
  if (dias < 1 || dias > 7) {
    alert("Ingresar una cantidad de dias valido.");
    return false;
  }
  // Validación de precio
  if (precio < 0) {
    alert("Ingresar un precio valido.");
    return false;
  }
  return true;
}
document.getElementById("formPlan").onsubmit = function () {
  return validar();
};
