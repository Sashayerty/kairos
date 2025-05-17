// Функция переключения темы
function toggleTheme() {
  const html = document.documentElement;
  const theme =
    html.getAttribute("data-bs-theme") === "dark" ? "light" : "dark";

  // Обновляем атрибут темы
  html.setAttribute("data-bs-theme", theme);

  // Сохраняем выбор в localStorage
  localStorage.setItem("theme", theme);

  // Обновляем иконку кнопки
  const icon = document.querySelector(".theme-toggle i");
  icon.className = theme === "dark" ? "bi bi-moon-stars-fill fs-5" : "bi bi-sun-fill fs-5";
}

// Инициализация темы при загрузке
function initTheme() {
  const savedTheme =
    localStorage.getItem("theme") ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches
      ? "dark"
      : "light");

  document.documentElement.setAttribute("data-bs-theme", savedTheme);

  const icon = document.querySelector(".theme-toggle i");
  icon.className = savedTheme === "dark" ? "bi bi-moon-stars-fill fs-5" : "bi bi-sun-fill fs-5";
}

// Вешаем обработчик на кнопку
document.querySelector(".theme-toggle").addEventListener("click", toggleTheme);

// Запускаем инициализацию при загрузке
initTheme();
