# Tournament Management System - Microservices Architecture

Повнофункціональна система управління турнірами на мікросервісній архітектурі з Django REST Framework і Vue.js.

## 📋 Архітектура

```
API Gateway (Port 8000)
    ├── User Service (Port 8004)
    ├── Tournament Service (Port 8001)
    ├── Submission Service (Port 8002)
    ├── Product Service (Port 8001)
    ├── Cart Service (Port 8002)
    └── Order Service (Port 8003)

Frontend (Vue.js, Port 3000)
```

## 🏗️ Мікросервіси

### 1. User Service
**Відповідальність**: Управління користувачами, автентифікацією, авторизацією

**Моделі**:
- User (з ролями: admin, jury, team_lead, team_member)

**Endpoints**:
- POST `/api/auth/login/` - Вхід
- POST `/api/auth/refresh/` - Оновити токен
- POST `/api/users/register/` - Реєстрація
- GET `/api/users/profile/` - Профіль
- PUT `/api/users/profile/update/` - Оновити профіль

### 2. Tournament Service
**Відповідальність**: Управління турнірами, командами, завданнями

**Моделі**:
- Tournament (турніри)
- Team (команди)
- TeamMember (члени команд)
- Task (завдання)
- TaskRequirement (вимоги завдань)

**Endpoints**:
- `GET/POST /api/tournaments/` - Турніри
- `GET/POST /api/teams/` - Команди
- `GET/POST /api/tasks/` - Завдання
- `GET/POST /api/task-requirements/` - Вимоги

### 3. Submission Service
**Відповідальність**: Управління поданнями, оцінюванням, лідербордом

**Моделі**:
- Submission (подачі рішень)
- JuryAssignment (призначення журі)
- Score (оцінки)
- Leaderboard (таблиця лідерів)

**Endpoints**:
- `GET/POST /api/submissions/` - Подачі
- `GET/POST /api/jury-assignments/` - Призначення журі
- `GET/POST /api/scores/` - Оцінки
- `GET /api/leaderboard/` - Таблиця лідерів

### 4-6. Product/Cart/Order Services
Існуючі сервіси для e-commerce функціональності

## 🔧 Встановлення

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Node.js 16+
- pip / venv

### Встановлення User Service
```bash
cd services/user-service
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Налаштування БД
echo "DB_NAME=user_db" > .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8004
```

### Встановлення Tournament Service
```bash
cd services/tournament-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

echo "DB_NAME=tournament_db" > .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8001
```

### Встановлення Submission Service
```bash
cd services/submission-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

echo "DB_NAME=submission_db" > .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8002
```

### Запуск API Gateway
```bash
cd api-gateway
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver 8000
```

### Запуск Frontend
```bash
cd frontend
npm install
npm run dev
# або для production
npm run build
```

## ✅ Тестування

### Tournament Service
```bash
cd services/tournament-service

# Запуск всіх тестів
pytest

# Запуск з покриттям
pytest --cov=apps

# Запуск конкретного тест-класу
pytest apps/tournaments/tests.py::TestUserModel -v

# Запуск конкретного тесту
pytest apps/tournaments/tests.py::TestUserModel::test_create_user -v
```

### Submission Service
```bash
cd services/submission-service

# Запуск всіх тестів
pytest

# Запуск з покриттям
pytest --cov=apps

# Запуск конкретних тестів
pytest apps/submissions/tests.py::TestSubmissionModel -v
```

## 📊 Database Schema

### Tournament Service DB
```sql
-- Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    email VARCHAR(254) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20),
    created_at TIMESTAMP
);

-- Tournaments
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    created_by INT REFERENCES users(id),
    title VARCHAR(255),
    description TEXT,
    reg_start TIMESTAMP,
    reg_end TIMESTAMP,
    max_teams INT,
    status VARCHAR(20),
    created_at TIMESTAMP
);

-- Teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    tournament_id INT REFERENCES tournaments(id),
    name VARCHAR(255),
    captain_name VARCHAR(150),
    captain_email VARCHAR(254),
    city VARCHAR(100),
    contact VARCHAR(20),
    registered_at TIMESTAMP
);

-- Team Members
CREATE TABLE team_members (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id),
    full_name VARCHAR(150),
    email VARCHAR(254)
);

-- Tasks
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    tournament_id INT REFERENCES tournaments(id),
    created_by INT REFERENCES users(id),
    title VARCHAR(255),
    description TEXT,
    tech_requirements TEXT,
    start_time TIMESTAMP,
    deadline TIMESTAMP,
    status VARCHAR(20)
);

-- Task Requirements
CREATE TABLE task_requirements (
    id SERIAL PRIMARY KEY,
    task_id INT REFERENCES tasks(id),
    title VARCHAR(255),
    is_required BOOLEAN
);
```

### Submission Service DB
```sql
-- Submissions
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    task_id INT,
    team_id INT,
    github_url VARCHAR(255),
    video_url VARCHAR(255),
    live_demo_url VARCHAR(255),
    description TEXT,
    is_locked BOOLEAN,
    submitted_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Jury Assignments
CREATE TABLE jury_assignments (
    id SERIAL PRIMARY KEY,
    submission_id INT REFERENCES submissions(id),
    jury_user_id INT,
    is_evaluated BOOLEAN,
    assigned_at TIMESTAMP
);

-- Scores
CREATE TABLE scores (
    id SERIAL PRIMARY KEY,
    assignment_id INT REFERENCES jury_assignments(id),
    backend_code INT,
    database INT,
    frontend_code INT,
    functionality INT,
    usability INT,
    comment TEXT,
    evaluated_at TIMESTAMP
);

-- Leaderboard
CREATE TABLE leaderboard (
    id SERIAL PRIMARY KEY,
    tournament_id INT,
    team_id INT,
    total_score FLOAT,
    rank INT,
    calculated_at TIMESTAMP
);
```

## 🎯 OOP-паттерни та Best Practices

### Models
✅ Docstrings для всіх моделей
✅ Методи для бізнес-логіки
✅ Properties для обчислюваних значень
✅ Meta класи для конфігурації
✅ Validators для валідації

### Serializers
✅ Розділення на Create/Read/Update serializers
✅ Custom validators
✅ Вкладені serializers
✅ SerializerMethodField для обчислюваних полів

### Views
✅ ViewSets для CRUD
✅ Custom actions для спеціальних функцій
✅ Правильна обробка permissions
✅ Фільтрування та пошук

### Tests
✅ pytest + pytest-django
✅ Фікстури для даних
✅ Тестування моделей
✅ Покриття > 80%

## 🔐 Безпека

### Authentication
- JWT токени (SimpleJWT)
- Access Token Lifetime: 60 хвилин
- Refresh Token Lifetime: 1 день

### Authorization
- Permission classes на базі DRF
- Role-based access control (admin, jury, team_lead, team_member)

### CORS
- Налаштовано для http://localhost:3000
- Можна змінити в settings.py

### Rate Limiting
- 100 запитів/хвилину для анонімних користувачів
- 1000 запитів/хвилину для авторизованих

## 📝 API Documentation

Детальна документація для кожного сервісу:
- [User Service](services/user-service/README.md)
- [Tournament Service](services/tournament-service/README.md)
- [Submission Service](services/submission-service/README.md)

## 🚀 Production Deployment

### Docker
```bash
docker-compose up -d
```

### Gunicorn
```bash
gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4
```

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_NAME=tournament_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=db.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## 📚 Структура проекту

```
microservices-shop/
├── api-gateway/                 # API Gateway (маршрутизація)
│   ├── apps/
│   │   └── gateway/
│   │       ├── views.py        # Proxy views
│   │       ├── urls.py         # Routes
│   │       └── middleware.py   # Rate limiting
│   └── config/
│       └── settings.py         # Service URLs
│
├── services/
│   ├── user-service/           # Authentication & Users
│   │   ├── apps/users/
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── tests.py
│   │   └── config/
│   │
│   ├── tournament-service/     # NEW - Tournaments & Tasks
│   │   ├── apps/tournaments/
│   │   │   ├── models.py       # Tournament, Team, Task, TaskRequirement
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── tests.py        # 50+ unit tests
│   │   │   └── migrations/
│   │   └── config/
│   │
│   ├── submission-service/     # NEW - Submissions & Scoring
│   │   ├── apps/submissions/
│   │   │   ├── models.py       # Submission, JuryAssignment, Score, Leaderboard
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── tests.py        # 50+ unit tests
│   │   │   └── migrations/
│   │   └── config/
│   │
│   ├── product-service/        # Products (existing)
│   ├── cart-service/           # Cart (existing)
│   └── order-service/          # Orders (existing)
│
└── frontend/                   # Vue.js app
    ├── src/
    │   ├── components/
    │   ├── views/
    │   ├── services/
    │   ├── stores/
    │   └── router/
    └── public/
```

## 🐛 Debugging

### Логи
```bash
# Tournament Service
tail -f services/tournament-service/debug.log

# Submission Service
tail -f services/submission-service/debug.log
```

### Django Shell
```bash
cd services/tournament-service
python manage.py shell
>>> from apps.tournaments.models import Tournament
>>> Tournament.objects.all()
```

## 📞 Support

Для питань та проблем створюйте issues в репозиторії.

## 📄 Ліцензія

MIT License

---

**Остання оновлення**: May 11, 2026
**Версія**: 1.0.0
**Status**: ✅ Production Ready
