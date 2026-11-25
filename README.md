# QuestDark — Сервис бронирования квест-комнат

## Быстрый запуск
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

## Разделы и маршруты
- Главная (`/`) — `quests:home`
- Каталог квестов (`/catalog/`) — `quests:catalog` (пагинация по 20 записей, фильтр по жанру и сложности, а также мгновенный JS-фильтр без перезагрузки)
- Карточка квеста (`/quest/<int:pk>/`) — `quests:quest_detail`
- Форма бронирования (`/quest/<int:pk>/book/`) — `quests:book_quest` (серверная + JS валидация имени, email, телефона, количества игроков; проверка слота через `fetch('/api/check-slot/')`)
- Поиск (`/search/`) — `quests:search` (серверный поиск + живой поиск без перезагрузки)
- О проекте (`/about/`) — `quests:about` (статическая страница с правилами, UI-Kit и расписанием)
- Личный кабинет (`/accounts/profile/`) — `users:profile` (бронирования, отмена с возвратом слота, создание команд)
"# var14" 
