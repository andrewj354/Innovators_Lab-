# 🏆 Турнірна Платформа для IT Змаганнь

Повнофункціональна веб-платформа для організації та проведення IT турнірів з автоматичним оцінюванням і рейтингами.

## 📋 Зміст

- [Функціональність](#-функціональність)
- [Технологічний стек](#-технологічний-стек)
- [Архітектура](#-архітектура)
- [Швидкий старт](#-швидкий-старт)
- [Документація](#-документація)
- [Розробка](#-розробка)

---

## ✨ Функціональність

### Для Адміністраторів
- 📊 Керування турнірами (створення, редагування, видалення)
- 👥 Управління користувачами та ролями
- 📝 Розподіл завдань та оцінювачів
- 📈 Моніторинг прогресу турніру
- 🏅 Формування leaderboard

### Для Команд
- 🎯 Реєстрація команд у турніри
- 📖 Перегляд завдань та вимог
- 💾 Подача розв'язків (GitHub, відео, live demo)
- ⏱️ Моніторинг дедлайнів
- 📊 Перегляд результатів і рейтингів

### Для Оцінювачів (Журі)
- 📋 Список призначених робіт
- ⭐ Оцінювання за 5 критеріями (0-100)
- 💬 Залишення коментарів
- 📝 Редагування оцінок
- 📊 Перегляд leaderboard

---

## 🛠️ Технологічний Стек

### Backend
- **Framework**: Django 5.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Auth**: JWT (djangorestframework-simplejwt)
- **Testing**: pytest, pytest-django, pytest-cov

### Frontend
- **Framework**: React 19 + Vite
- **Routing**: React Router v7
- **HTTP Client**: Axios
- **UI**: CSS3
- **Notifications**: react-toastify

### DevOps
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Web Server**: Gunicorn (production)

---

## 🏛️ Архітектура

### Мікросервісна Архітектура

```
┌─────────────────────────────────────────────┐
│         Frontend (React + Vite)             │
│    http://localhost:3000                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      API Gateway (Django Proxy)             │
│    http://localhost:8000                    │
│    • Маршрутизація                          │
│    • CORS                                   │
│    • Rate Limiting                          │
│    • Authentication Forwarding              │
└─────┬──────────────┬───────────┬────────────┘
      │              │           │
      ▼              ▼           ▼
  ┌────────┐     ┌────────┐  ┌────────┐
  │ User   │     │Tour    │  │Submit  │
  │Service │     │nament  │  │ Service│
  │:8001   │     │:8003   │  │:8002   │
  └────────┘     └────────┘  └────────┘
      │              │           │
      └──────────────┴───────────┘
             ▼
        ┌─────────┐
        │PostgreSQL
        │:5432    │
        └─────────┘
             ▼
        ┌─────────┐
        │ Redis   │
        │:6379    │
        └─────────┘
```

### Сервіси

| Сервіс | Порт | Призначення |
|--------|------|-----------|
| API Gateway | 8000 | Маршрутизація всіх запитів |
| User Service | 8001 | Автентифікація, користувачі, команди |
| Task Service | 8002 | Завдання, подачі, оцінки |
| Tournament Service | 8003 | Турніри, розклад, рейтинги |
| Frontend | 3000 | React додаток |
| PostgreSQL | 5432 | База даних |
| Redis | 6379 | Кеш і черги |

---

## 🚀 Швидкий Старт

### Вимоги

- Docker & Docker Compose
- Python 3.11+ (для локального розгортування)
- Node.js 18+ (для frontend)

### 1️⃣ Docker Compose (Рекомендується)

```bash
# Клонування
git clone <repository-url>
cd Innovators_Lab-

# Запуск
docker-compose up -d

# Перевірка
docker-compose ps

# Доступні адреси
# Frontend: http://localhost:3000
# API Gateway: http://localhost:8000
```

### 2️⃣ Локальне Розгортування

```bash
# User Service
cd services/user-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001

# В новому терміналі - Tournament Service
cd services/tournament-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8003

# В новому терміналі - Submission Service
cd services/submission-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8002

# В новому терміналі - API Gateway
cd api-gateway
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000

# В новому терміналі - Frontend
cd frontend
npm install
npm run dev
```

### 3️⃣ Запуск Тестів

```bash
# Всі тести
./run_tests.sh          # Linux/macOS
run_tests.bat           # Windows

# Окремо
cd services/user-service
pytest --cov=apps -v
```

---

## 📚 Документація

| Документ | Опис |
|----------|------|
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Детальний посібник розгортування та тестування |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Архітектурні рішення |
| [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) | API Endpoints |
| [COMPLETION_STATUS.md](./COMPLETION_STATUS.md) | Статус реалізації |

---

## 💻 Розробка

### Структура Проекту

```
Innovators_Lab-/
├── api-gateway/              # API Gateway сервіс
│   ├── apps/
│   ├── config/
│   ├── requirements.txt
│   └── Dockerfile
├── services/
│   ├── user-service/         # Користувачі і автентифікація
│   ├── tournament-service/   # Турніри і розклад
│   └── submission-service/   # Завдання і подачі
├── frontend/                 # React додаток
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── shared/                   # Спільні утиліти
├── docker-compose.yml        # Docker Compose конфіг
├── DEPLOYMENT_GUIDE.md       # Цей файл
└── README.md                 # Цей файл
```

### Запуск Локально (без Docker)

#### Передумови

```bash
# Установка PostgreSQL
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql-client libpq-dev

# Установка Redis
# macOS: brew install redis
# Ubuntu: sudo apt-get install redis-server

# Запуск сервісів
# PostgreSQL: pg_ctl -D /usr/local/var/postgres start
# Redis: redis-server
```

#### Налаштування БД

```bash
createdb user_db
createdb tournament_db
createdb submission_db
createdb rank_db
```

### Контролер Якості

```bash
# Лінтинг (Python)
cd services/user-service
flake8 apps/

# Форматування (Python)
black apps/

# Лінтинг (Frontend)
cd frontend
npm run lint

# Тести
pytest --cov=apps --cov-report=html
```

### Створення Міграцій

```bash
# Після змін моделей
python manage.py makemigrations

# Застосування міграцій
python manage.py migrate

# Перевірка статусу
python manage.py showmigrations
```

### Отримання Токена

```bash
# Створення superuser
python manage.py createsuperuser

# Отримання JWT токена
curl -X POST http://localhost:8001/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

---

## 🐛 Усунення Неполадок

### Контейнери не стартують

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Помилка підключення до БД

```bash
docker-compose logs postgres
docker-compose restart postgres
```

### Тести не проходять

```bash
pip install -r requirements.txt
pytest -v --tb=short
```

Див. [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) для більш детальних рішень.

---

## 📊 Тестування

### Покриття Тестами

- ✅ Unit тести (моделі, serializers)
- ✅ Integration тести (API endpoints)
- ✅ Gateway тести (маршрутизація, middleware)
- ⚠️ Frontend тести (в розробці)
- ⚠️ E2E тести (в розробці)

### Запуск Тестів

```bash
# Всі тести з покриттям
pytest --cov=apps --cov-report=html

# Конкретний тест
pytest apps/users/tests.py::UserModelTest -v

# З виводом
pytest -v -s
```

---

## 🔗 Посилання

- [Django REST Framework Docs](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Docs](https://docs.docker.com/)

---

## 📞 Контакти

- **Lead Developer**: Ростислав
- **Frontend Lead**: Вадим
- **QA Lead**: Ігор

---

## 📄 Ліцензія

Приватний проект. Всі права захищені.

---

**Версія**: 1.0.0  
**Остання оновлення**: Січень 2025