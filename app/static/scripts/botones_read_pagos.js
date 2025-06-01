function showDeleteForm(id) {
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteForm").style.display = "block";
}

function hideDeleteForm() {
  document.getElementById("deleteForm").style.display = "none";
}

function eliminarPago() {
  const pagoId = document.getElementById("deleteId").value;

  fetch(`/eliminar_pago/${pagoId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (!response.ok) throw new Error("Error al eliminar el pago");
      return response.json();
    })
    .then((data) => {
      alert(data.message);
      document.getElementById(`pago-${pagoId}`).remove();
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al eliminar el pago: " + error.message);
    })
    .finally(() => {
      hideDeleteForm();
    });
}
