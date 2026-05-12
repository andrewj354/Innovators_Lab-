# Tournament Service

## Опис

Tournament Service - це мікросервіс для управління турнірами, командами, членами команд та завданнями. Служить як основний сервіс для організації конкурсів та турнірів.

## Архітектура

### Моделі

#### User
- **id** (PK): Унікальний ідентифікатор
- **name**: Повне ім'я користувача
- **email**: Унікальна електронна пошта
- **role**: Роль користувача (admin, jury, team_lead, team_member)
- **created_at**: Дата реєстрації

#### Tournament
- **id** (PK): Унікальний ідентифікатор
- **created_by** (FK): Користувач-засновник
- **title**: Назва турніру
- **description**: Описання
- **reg_start**: Початок реєстрації
- **reg_end**: Закінчення реєстрації
- **max_teams**: Максимум команд
- **status**: Статус (planning, registration, running, completed)
- **created_at**: Дата створення

#### Team
- **id** (PK): Унікальний ідентифікатор
- **tournament_id** (FK): Турнір
- **name**: Назва команди
- **captain_name**: Ім'я капітана
- **captain_email**: Email капітана
- **city**: Місто
- **contact**: Контактна інформація
- **registered_at**: Дата реєстрації

#### TeamMember
- **id** (PK): Унікальний ідентифікатор
- **team_id** (FK): Команда
- **full_name**: Повне ім'я
- **email**: Email члена

#### Task
- **id** (PK): Унікальний ідентифікатор
- **tournament_id** (FK): Турнір
- **created_by** (FK): Творець завдання
- **title**: Назва завдання
- **description**: Описання
- **tech_requirements**: Технічні вимоги
- **start_time**: Час початку
- **deadline**: Дедлайн
- **status**: Статус (draft, published, closed)

#### TaskRequirement
- **id** (PK): Унікальний ідентифікатор
- **task_id** (FK): Завдання
- **title**: Описання вимоги
- **is_required**: Чи обов'язкова

## Встановлення

```bash
# 1. Перейти в директорію сервісу
cd services/tournament-service

# 2. Створити virtual environment
python -m venv venv

# 3. Активувати virtual environment
# На Windows:
venv\Scripts\activate
# На macOS/Linux:
source venv/bin/activate

# 4. Встановити залежності
pip install -r requirements.txt

# 5. Налаштувати БД (створити .env файл)
echo "DB_NAME=tournament_db" > .env
echo "DB_USER=postgres" >> .env
echo "DB_PASSWORD=postgres" >> .env
echo "DB_HOST=localhost" >> .env

# 6. Запустити міграції
python manage.py migrate

# 7. Створити суперлокального користувача
python manage.py createsuperuser
```

## Запуск

### Розробка
```bash
python manage.py runserver 8001
```

### Production (з Gunicorn)
```bash
gunicorn config.wsgi --bind 0.0.0.0:8001
```

## Тестування

### Запуск всіх тестів
```bash
pytest
```

### Запуск з покриттям
```bash
pytest --cov=apps
```

### Запуск конкретного тесту
```bash
pytest apps/tournaments/tests.py::TestUserModel::test_create_user -v
```

## API Endpoints

### Users
- `GET /api/users/` - Список користувачів
- `POST /api/users/` - Створити користувача
- `GET /api/users/{id}/` - Деталі користувача
- `PUT /api/users/{id}/` - Оновити користувача
- `DELETE /api/users/{id}/` - Видалити користувача

### Tournaments
- `GET /api/tournaments/` - Список турнірів
- `POST /api/tournaments/` - Створити турнір
- `GET /api/tournaments/{id}/` - Деталі турніру
- `PUT /api/tournaments/{id}/` - Оновити турнір
- `GET /api/tournaments/{id}/teams/` - Команди турніру
- `GET /api/tournaments/{id}/tasks/` - Завдання турніру
- `GET /api/tournaments/{id}/statistics/` - Статистика

### Teams
- `GET /api/teams/` - Список команд
- `POST /api/teams/` - Створити команду
- `GET /api/teams/{id}/` - Деталі команди
- `GET /api/teams/{id}/members/` - Члени команди
- `POST /api/teams/{id}/members/` - Додати члена
- `GET /api/teams/{id}/statistics/` - Статистика

### Tasks
- `GET /api/tasks/` - Список завдань
- `POST /api/tasks/` - Створити завдання
- `GET /api/tasks/{id}/` - Деталі завдання
- `GET /api/tasks/{id}/requirements/` - Вимоги
- `POST /api/tasks/{id}/requirements/` - Додати вимогу
- `GET /api/tasks/{id}/statistics/` - Статистика

## OOP-паттерни

### Models
- Использование docstrings для документування
- Методи для бізнес-логіки (is_active, can_accept_teams, тощо)
- Properties для обчислюваних значень (members_count, is_registration_open)
- Meta класи для конфігурації
- Validators для валідації даних

### Serializers
- Розділення на Create/Update та Read serializers
- Custom validators для перевірки даних
- SerializerMethodField для обчислюваних полів
- Nested serializers для зв'язаних даних

### Views
- ViewSets для CRUD операцій
- Custom actions (@action) для спеціальних функцій
- Правильна обробка дозволів (permissions)
- Фільтрування, пошук та впорядкування

## Ліцензія

MIT
