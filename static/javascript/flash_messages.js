// Esperar a que el DOM cargue completamente
document.addEventListener("DOMContentLoaded", function () {
  const flashMessages = document.querySelectorAll(".flash-message");
  flashMessages.forEach(function (message) {
    // Ocultar el mensaje después de 2 segundos
    setTimeout(function () {
      message.style.opacity = "0"; // Añadir efecto de desvanecimiento
      setTimeout(() => message.remove(), 500); // Eliminarlo completamente después de la animación
    }, 1000);
  });
});
