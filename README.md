Custom Auth & Permissions API

Это тестовое backend-приложение на Django + DRF с кастомной системой аутентификации и авторизации.

Функционал:

- Регистрация пользователей (автоматически даётся право view на проекты)
- Login/Logout через JWT + blacklist токенов
- Просмотр проектов (project) с проверкой прав
- Редактирование проектов (edit) через права
- Админ может выдавать права другим пользователям
- Мягкое удаление пользователей (is_active=False)
- Кастомные сериализаторы и пермишены
- Покрытие тестами на основные сценарии

Установка и запуск:

1. Клонируем репозиторий:
git clone <repo_url>
cd <repo_folder>

2. Создаём виртуальное окружение и устанавливаем зависимости:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. Настраиваем Postgres:
- Создайте базу данных, пользователя и пароль
- Настройте DATABASES в settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

4. Применяем миграции:
python manage.py makemigrations
python manage.py migrate

5. Запускаем сервер:
python manage.py runserver

Тестирование:

pytest

Примечания:

- Токены JWT хранятся в заголовке Authorization: Bearer <token>
- Админ создаётся через поле is_admin=True
- По дефолту пользователи получают только право view на проекты