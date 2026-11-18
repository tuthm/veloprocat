"use strict";

/* ---------- Мобильное меню ---------- */
const burger = document.getElementById("burger");
const nav = document.getElementById("nav");
if (burger && nav) {
  burger.addEventListener("click", () => {
    const open = nav.classList.toggle("nav--open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });
}

/* ---------- Калькулятор стоимости (динамический элемент №1) ---------- */
const calc = document.querySelector(".calc");
if (calc) {
  const price = parseFloat(calc.dataset.price) || 0;
  const startEl = document.getElementById("calc-start");
  const endEl = document.getElementById("calc-end");
  const totalEl = document.getElementById("calc-total");
  const today = new Date().toISOString().slice(0, 10);
  if (startEl) startEl.min = today;
  if (endEl) endEl.min = today;

  const recalc = () => {
    if (!startEl.value || !endEl.value) { totalEl.textContent = "—"; return; }
    const days = (new Date(endEl.value) - new Date(startEl.value)) / 86400000;
    if (days < 1) { totalEl.textContent = "—"; return; }
    totalEl.textContent = new Intl.NumberFormat("ru-RU").format(days * price) + " ₽";
  };
  startEl.addEventListener("change", recalc);
  endEl.addEventListener("change", recalc);
}

/* ---------- Клиентская валидация формы брони ---------- */
const PHONE_RE = /^\+7\d{10}$/;
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

const bookingForm = document.getElementById("booking-form");
if (bookingForm) {
  const errors = {
    start_date: "",
    end_date: "",
    phone: "",
    email: "",
  };

  const showErrors = () => {
    Object.entries(errors).forEach(([key, msg]) => {
      const slot = bookingForm.querySelector(`[data-error="${key}"]`);
      if (slot) slot.textContent = msg;
    });
    const formError = document.getElementById("form-error");
    if (formError) formError.textContent = "";
  };

  bookingForm.addEventListener("submit", (event) => {
    const start = bookingForm.querySelector('[name="start_date"]');
    const end = bookingForm.querySelector('[name="end_date"]');
    const phone = bookingForm.querySelector('[name="phone"]');
    const email = bookingForm.querySelector('[name="email"]');

    errors.start_date = "";
    errors.end_date = "";
    errors.phone = "";
    errors.email = "";

    const today = new Date().toISOString().slice(0, 10);
    if (!start.value) errors.start_date = "Выберите дату начала.";
    else if (start.value < today) errors.start_date = "Дата начала не может быть в прошлом.";
    if (!end.value) errors.end_date = "Выберите дату конца.";
    else if (start.value && end.value <= start.value) errors.end_date = "Дата конца должна быть позже даты начала.";
    if (!PHONE_RE.test(phone.value.trim().replace(/\s/g, ""))) errors.phone = "Телефон в формате +7XXXXXXXXXX.";
    if (!EMAIL_RE.test(email.value.trim())) errors.email = "Укажите корректную электронную почту.";

    showErrors();
    if (Object.values(errors).some(Boolean)) {
      event.preventDefault();
    }
  });
}

/* ---------- Живой поиск (динамический элемент №2) ---------- */
const searchInput = document.getElementById("search-input");
const grid = document.getElementById("catalog-grid");
if (searchInput && grid) {
  const api = grid.dataset.api;
  const STATUS_LABELS = { free: "Свободен", rented: "В прокате", repair: "Требуется ремонт" };

  const renderCard = (u) => `
    <article class="card">
      <a href="/unit/${u.id}/">
        <div class="card__photo"><div class="card__placeholder">Bike photo</div></div>
        <p class="card__category">${u.category}</p>
        <h3 class="card__name">${u.name}</h3>
        <p class="card__price">${new Intl.NumberFormat("ru-RU").format(u.price)} ₽ / сутки</p>
        <span class="status status--${u.status}">${STATUS_LABELS[u.status] || u.status_label}</span>
      </a>
    </article>`;

  let timer = null;
  searchInput.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      const q = searchInput.value.trim();
      fetch(`${api}?q=${encodeURIComponent(q)}`)
        .then((res) => res.json())
        .then((data) => {
          if (data.units.length === 0) {
            grid.innerHTML = '<p class="empty">Ничего не найдено</p>';
          } else {
            grid.innerHTML = data.units.map(renderCard).join("");
          }
          const counter = document.getElementById("catalog-counter");
          if (counter) {
            counter.textContent = "Найдено " + data.count + " " +
              (data.count % 10 === 1 && data.count % 100 !== 11 ? "единица"
                : [2, 3, 4].includes(data.count % 10) && ![12, 13, 14].includes(data.count % 100)
                  ? "единицы" : "единиц");
          }
        })
        .catch(() => {});
    }, 300);
  });
}
