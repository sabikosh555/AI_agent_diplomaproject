# AI Университет — Django

## Іске қосу / Запуск

```bash
# 1. Виртуальное окружение (опционально)
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Установка зависимостей
pip install -r requirements.txt

# 3. Миграции
python manage.py migrate

# 4. Демо-данные (пользователь student / student123)
python manage.py create_demo_data

# 5. Запуск сервера
python manage.py runserver
```

## OpenAI API (AI көмекші үшін)

Ключті орнату үшін:
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-..."

# Немесе settings.py ішінде OPENAI_API_KEY = "sk-..."
```
Ключ бос болса — локальды демо-жауаптар қолданылады.

Откройте: http://127.0.0.1:8000/

## Демо-пользователь

- **Логин:** student
- **Пароль:** student123

## Структура проекта

```
├── ai_university/       # Настройки Django
├── main/                # Главная страница
├── cabinet/             # Личный кабинет
│   ├── views.py         # Function-based views
│   ├── models.py        # StudentProfile, Document, Grade, Notification
│   └── urls.py
├── templates/
│   ├── main/index.html
│   └── cabinet/         # login, dashboard, documents, schedule, assistant, grades, notifications, profile, settings
├── static/
│   ├── css/styles.css
│   └── js/chat.js
└── manage.py
```

## URL-маршруты

| URL | View | Описание |
|-----|------|----------|
| / | index_view | Главная |
| /cabinet/login/ | login_view | Вход |
| /cabinet/logout/ | logout_view | Выход |
| /cabinet/ | dashboard_view | Панель |
| /cabinet/documents/ | documents_view | Документы |
| /cabinet/schedule/ | schedule_view | Расписание |
| /cabinet/assistant/ | assistant_view | AI чат |
| /cabinet/grades/ | grades_view | Оценки |
| /cabinet/notifications/ | notifications_view | Уведомления |
| /cabinet/profile/ | profile_view | Профиль |
| /cabinet/settings/ | settings_view | Настройки |
| /cabinet/api/chat/ | chat_api_view | API AI чата (POST) |
