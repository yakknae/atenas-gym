function logout() {
  fetch("/logout", {
    method: "GET",
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = "/login"; // Redirige al login
      } else {
        console.error("Error al cerrar sesión");
      }
    })
    .catch((error) => console.error("Error:", error));
}
