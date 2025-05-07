function showDeleteForm(id) {
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteForm").style.display = "block";
}
function hideDeleteForm() {
  document.getElementById("deleteForm").style.display = "none";
}

function eliminarPlanSocial() {
  const planSocialId = document.getElementById("deleteId").value;

  fetch(`/planes_sociales/${planSocialId}/eliminar`, {
    method: "POST", // POST como en el backend
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al eliminar el plan social");
      }
      return response.json(); // Asegurarse de que la respuesta es JSON
    })
    .then((data) => {
      alert(data.message); // Mostrar el mensaje que viene de la respuesta

      // Eliminar la fila de la tabla
      const row = document.getElementById(`plan-social-${planSocialId}`);
      if (row) {
        row.remove(); // Eliminar la fila correspondiente solo si existe
      } else {
        console.error("No se encontró la fila con ID:", `plan-social-${planSocialId}`);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al eliminar el plan social: " + error.message);
    })
    .finally(() => {
      hideDeleteForm(); // Ocultar el formulario de eliminación
    });
}
