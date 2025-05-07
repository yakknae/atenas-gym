function showDeleteForm(id) {
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteForm").style.display = "block";
}

function hideDeleteForm() {
  document.getElementById("deleteForm").style.display = "none";
}

function eliminarCombo() {
  const comboId = document.getElementById("deleteId").value;

  fetch(`/planes/${comboId}/eliminar`, {
    method: "POST", // Mantén POST aquí como en el backend
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error al eliminar el combo");
      }
      return response.json();
    })
    .then((data) => {
      alert(data.message);
      document.getElementById(`combo-${comboId}`).remove();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al eliminar el combo: " + error.message);
    })
    .finally(() => {
      hideDeleteForm();
    });
}
