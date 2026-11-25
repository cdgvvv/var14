// 1. Бургер-меню
const burger = document.getElementById('burger-btn');
const nav = document.getElementById('main-nav');

if (burger && nav) {
    burger.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('active');
        burger.setAttribute('aria-expanded', String(isOpen));
    });
}

function showFieldError(inputEl, message) {
    if (!inputEl) return;
    inputEl.style.borderColor = 'var(--error)';
    const parent = inputEl.closest('.form-group') || inputEl.parentElement;
    let errEl = parent.querySelector('.js-field-error');
    if (!errEl) {
        errEl = document.createElement('p');
        errEl.className = 'js-field-error';
        parent.appendChild(errEl);
    }
    errEl.textContent = message;
}

function clearFieldError(inputEl) {
    if (!inputEl) return;
    inputEl.style.borderColor = 'var(--border-color)';
    const parent = inputEl.closest('.form-group') || inputEl.parentElement;
    const errEl = parent.querySelector('.js-field-error');
    if (errEl) {
        errEl.remove();
    }
}

// 2. Клиентская валидация формы бронирования (обязательные поля, email, телефон, длина текста, игроки)
const bookingForm = document.getElementById('booking-form');
if (bookingForm) {
    bookingForm.addEventListener('submit', function (e) {
        let valid = true;

        const nameInput = document.getElementById('id_customer_name');
        const emailInput = document.getElementById('id_customer_email');
        const phoneInput = document.getElementById('id_customer_phone');
        const playersInput = document.getElementById('id_players_count');
        const sessionInput = document.getElementById('id_session_id');

        [nameInput, emailInput, phoneInput, playersInput, sessionInput].forEach(clearFieldError);

        const nameVal = (nameInput.value || '').trim();
        if (!nameVal || nameVal.length < 2 || nameVal.length > 100) {
            valid = false;
            showFieldError(nameInput, 'Введите имя (от 2 до 100 символов).');
        }

        const emailVal = (emailInput.value || '').trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailVal || !emailRegex.test(emailVal)) {
            valid = false;
            showFieldError(emailInput, 'Введите корректный email (например, name@example.com).');
        }

        const phoneVal = (phoneInput.value || '').trim();
        const phoneDigits = phoneVal.replace(/\D/g, '');
        if (!phoneVal || phoneDigits.length < 7 || phoneDigits.length > 15) {
            valid = false;
            showFieldError(phoneInput, 'Введите корректный номер телефона (от 7 до 15 цифр).');
        }

        const players = parseInt(playersInput.value, 10);
        const maxPlayers = parseInt(this.dataset.maxPlayers, 10);
        if (isNaN(players) || players < 2 || players > 12) {
            valid = false;
            showFieldError(playersInput, 'Укажите от 2 до 12 игроков.');
        } else if (!isNaN(maxPlayers) && players > maxPlayers) {
            valid = false;
            showFieldError(playersInput, `Максимальное число игроков для этой комнаты — ${maxPlayers}.`);
        }

        if (!sessionInput.value) {
            valid = false;
            showFieldError(sessionInput, 'Выберите свободный сеанс.');
        }

        if (!valid) {
            e.preventDefault();
        }
    });
}

// 2b. Клиентская валидация формы создания команды в профиле
const teamForm = document.getElementById('team-form');
if (teamForm) {
    teamForm.addEventListener('submit', function (e) {
        let valid = true;
        const teamName = document.getElementById('id_name');
        const members = document.getElementById('id_members_list');
        [teamName, members].forEach(clearFieldError);

        if (!teamName.value.trim() || teamName.value.trim().length < 2) {
            valid = false;
            showFieldError(teamName, 'Название команды должно быть не короче 2 символов.');
        }
        if (members.value.trim().length > 300) {
            valid = false;
            showFieldError(members, 'Список участников не должен превышать 300 символов.');
        }
        if (!valid) {
            e.preventDefault();
        }
    });
}

// 3a. Динамический фильтр каталога без перезагрузки страницы
const liveGenreSelect = document.getElementById('live-genre-select');
const liveDiffSelect = document.getElementById('live-difficulty-select');
const catalogItems = document.querySelectorAll('.catalog-item');

function applyDynamicCatalogFilter() {
    if (!catalogItems.length) return;
    const selectedGenre = liveGenreSelect ? liveGenreSelect.value : '';
    const selectedDiff = liveDiffSelect ? liveDiffSelect.value : '';

    catalogItems.forEach((item) => {
        const matchGenre = !selectedGenre || item.dataset.genre === selectedGenre;
        const matchDiff = !selectedDiff || item.dataset.difficulty === selectedDiff;
        item.style.display = matchGenre && matchDiff ? '' : 'none';
    });
}

if (liveGenreSelect) {
    liveGenreSelect.addEventListener('change', applyDynamicCatalogFilter);
}
if (liveDiffSelect) {
    liveDiffSelect.addEventListener('change', applyDynamicCatalogFilter);
}

// 3b. Динамический живой поиск без перезагрузки страницы
const liveSearchInput = document.getElementById('live-search-input');
const searchItems = document.querySelectorAll('.search-item');
const searchCountEl = document.getElementById('search-count');

if (liveSearchInput && searchItems.length) {
    liveSearchInput.addEventListener('input', function () {
        const q = this.value.trim().toLowerCase();
        let visibleCount = 0;

        searchItems.forEach((item) => {
            const hay = `${item.dataset.title || ''} ${item.dataset.genre || ''} ${item.dataset.desc || ''}`;
            const matches = !q || hay.includes(q);
            item.style.display = matches ? '' : 'none';
            if (matches) visibleCount += 1;
        });

        if (searchCountEl) {
            searchCountEl.textContent = q
                ? `Найдено квестов по запросу «${this.value.trim()}»: ${visibleCount}`
                : `Все доступные квесты в каталоге: ${visibleCount}`;
        }
    });
}

// 4. Fetch API: Живая проверка слота с индикатором загрузки
const sessionSelect = document.getElementById('id_session_id');
const slotStatus = document.getElementById('slot-status');

async function checkSelectedSlot(sessionId) {
    if (!slotStatus) return;
    if (!sessionId) {
        slotStatus.textContent = '';
        return;
    }

    slotStatus.textContent = '⏳ Проверка доступности слота...';
    slotStatus.style.color = 'var(--text-muted)';

    try {
        const response = await fetch(`/api/check-slot/?session_id=${encodeURIComponent(sessionId)}`);
        const data = await response.json();

        if (data.available) {
            slotStatus.textContent = `Слот свободен (${data.date} в ${data.time})`;
            slotStatus.style.color = 'var(--success)';
        } else {
            slotStatus.textContent = data.error || 'Сеанс уже занят или не найден';
            slotStatus.style.color = 'var(--error)';
        }
    } catch (error) {
        slotStatus.textContent = 'Ошибка сети при проверке сеанса';
        slotStatus.style.color = 'var(--error)';
    }
}

if (sessionSelect) {
    sessionSelect.addEventListener('change', function () {
        checkSelectedSlot(this.value);
    });
    if (sessionSelect.value) {
        checkSelectedSlot(sessionSelect.value);
    }
}
