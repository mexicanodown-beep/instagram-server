// script.js - Validación y efectos para Instagram (versión escolar)

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('loginForm');
  const usernameInput = form.querySelector('input[type="text"]');
  const passwordInput = form.querySelector('input[type="password"]');

  // Validación en tiempo real
  usernameInput.addEventListener('input', validateField);
  passwordInput.addEventListener('input', validateField);

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    let isValid = true;

    // Validar campo de usuario
    if (usernameInput.value.trim() === '') {
      showError(usernameInput, 'Ingresa un teléfono, usuario o correo.');
      isValid = false;
    } else {
      clearError(usernameInput);
    }

    // Validar contraseña
    if (passwordInput.value.trim() === '') {
      showError(passwordInput, 'Ingresa tu contraseña.');
      isValid = false;
    } else {
      clearError(passwordInput);
    }

    if (isValid) {
      // Simular inicio de sesión
      alert('✅ ¡Inicio de sesión exitoso! (Este es un proyecto escolar)');
      
      // Opcional: cambiar el botón a "Cargando..."
      const button = form.querySelector('button');
      button.textContent = 'Cargando...';
      button.disabled = true;
      button.style.backgroundColor = '#4dabf7';
      
      setTimeout(() => {
        button.textContent = 'Iniciar sesión';
        button.disabled = false;
        button.style.backgroundColor = '#0095f6';
      }, 2000);
    }
  });

  function showError(input, message) {
    input.style.borderColor = '#ed4956';
    const error = document.createElement('div');
    error.textContent = message;
    error.style.color = '#ed4956';
    error.style.fontSize = '12px';
    error.style.marginTop = '4px';
    error.className = 'error-message';
    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('error-message')) {
      input.parentNode.insertBefore(error, input.nextSibling);
    }
  }

  function clearError(input) {
    input.style.borderColor = '#404040';
    const error = input.nextElementSibling;
    if (error && error.classList.contains('error-message')) {
      error.remove();
    }
  }

  function validateField() {
    clearError(this);
  }
});