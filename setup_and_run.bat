@echo off
chcp 65001 > nul
if not exist .venv (
    echo Создание виртуального окружения .venv...
    python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_quests
echo Запуск сервера на http://127.0.0.1:8000/
python manage.py runserver
