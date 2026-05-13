# Submission Service

## Опис

Submission Service - це мікросервіс для управління поданнями рішень, оцінюванням від журі та таблицею лідерів.

## Архітектура

### Моделі

#### Submission
- **id** (PK): Унікальний ідентифікатор
- **task_id** (FK): ID завдання
- **team_id** (FK): ID команди
- **github_url**: URL репозиторію
- **video_url**: URL відео демонстрації
- **live_demo_url**: URL живої демонстрації
- **description**: Описання подачі
- **is_locked**: Заблокована від редагування
- **submitted_at**: Дата подачі
- **updated_at**: Дата оновлення

#### JuryAssignment
- **id** (PK): Унікальний ідентифікатор
- **submission_id** (FK): Подача
- **jury_user_id**: ID користувача-журі
- **is_evaluated**: Оцінена чи ні
- **assigned_at**: Дата призначення

#### Score
- **id** (PK): Унікальний ідентифікатор
- **assignment_id** (FK): Призначення журі
- **backend_code**: Оцінка (0-100)
- **database**: Оцінка БД (0-100)
- **frontend_code**: Оцінка фронту (0-100)
- **functionality**: Оцінка функціональності (0-100)
- **usability**: Оцінка зручності (0-100)
- **comment**: Коментар
- **evaluated_at**: Дата оцінювання

#### Leaderboard
- **id** (PK): Унікальний ідентифікатор
- **tournament_id**: ID турніру
- **team_id**: ID команди
- **total_score**: Загальна оцінка
- **rank**: Місце в рейтингу
- **calculated_at**: Дата обчислення

## Встановлення

```bash
# 1. Перейти в директорію сервісу
cd services/submission-service

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
echo "DB_NAME=submission_db" > .env
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
python manage.py runserver 8002
```

### Production (з Gunicorn)
```bash
gunicorn config.wsgi --bind 0.0.0.0:8002
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
pytest apps/submissions/tests.py::TestSubmissionModel::test_create_submission -v
```

## API Endpoints

### Submissions
- `GET /api/submissions/` - Список подач
- `POST /api/submissions/` - Створити подачу
- `GET /api/submissions/{id}/` - Деталі подачі
- `PUT /api/submissions/{id}/` - Оновити подачу
- `POST /api/submissions/{id}/lock/` - Заблокувати
- `POST /api/submissions/{id}/unlock/` - Розблокувати
- `GET /api/submissions/{id}/scores/` - Отримати оцінки

### Jury Assignments
- `GET /api/jury-assignments/` - Список призначень
- `POST /api/jury-assignments/` - Призначити журі
- `GET /api/jury-assignments/{id}/` - Деталі призначення
- `POST /api/jury-assignments/{id}/mark_as_evaluated/` - Позначити як оцінене
- `GET /api/jury-assignments/pending_assignments/` - Невиконані завдання

### Scores
- `GET /api/scores/` - Список оцінок
- `POST /api/scores/` - Створити оцінку
- `GET /api/scores/{id}/` - Деталі оцінки
- `GET /api/scores/{id}/statistics/` - Статистика

### Leaderboard
- `GET /api/leaderboard/` - Весь лідербордом
- `GET /api/leaderboard/{id}/` - Деталі запису
- `GET /api/leaderboard/by_tournament/` - За турніром
- `GET /api/leaderboard/top_teams/` - Топ команди
- `POST /api/leaderboard/recalculate/` - Пересчитати

## OOP-паттерни

### Models
- Docstrings для всіх моделей
- Методи для операцій (lock, unlock, mark_as_evaluated, update_score)
- Properties для обчислюваних значень (average_score, total_score)
- Static/class методи для операцій над набором (recalculate_tournament_leaderboard)
- Validators для забезпечення цілісності даних

### Serializers
- Розділення на Create/Update та Read serializers
- Вкладені serializers для зв'язаних даних
- SerializerMethodField для обчислюваних полів
- Custom validators для валідації оцінок

### Views
- ViewSets з CRUD операціями
- Custom actions для спеціальних функцій (lock, unlock, scores)
- Read-only ViewSet для Leaderboard
- Правильна обробка дозволів

## Бізнес-логіка

### Автоматичні операції
1. При створенні Score - juryjassignment позначається як evaluated
2. При додаванні подачі - перевіряється унікальність (task_id + team_id)
3. При блокуванні подачі - неможливо редагувати

### Обчислення
- Середня оцінка: (backend_code + database + frontend_code + functionality + usability) / 5
- Загальна оцінка: сума всіх 5 критеріїв
- Рейтинг: впорядкування за total_score

## Ліцензія

MIT
