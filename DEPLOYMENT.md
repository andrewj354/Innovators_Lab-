# 🚀 Deployment Guide — Турнірна Платформа

## Архітектура Мікросервісів

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vue)                        │
│                    Port 3000 / 5173                             │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP(S)
┌────────────────────────────▼────────────────────────────────────┐
│                      API Gateway (Django)                       │
│                         Port 8000                               │
│                   routing.middleware.auth                       │
└──────┬──────────────────┬──────────────────┬────────────────────┘
       │                  │                  │
       │                  │                  │
   ┌───▼────┐        ┌───▼────────┐     ┌──▼─────────┐
   │         │        │             │     │            │
   │ user-   │        │ task-       │     │ tournament-│
   │ service │        │ service     │     │ service    │
   │ (8001)  │        │ (8002)      │     │ (8003)     │
   │         │        │             │     │            │
   │ Models: │        │ Models:     │     │ Models:    │
   │ - User  │        │ - Task      │     │ - Tournament
   │ - Team  │        │ - Submission│     │ - TournamentTeam
   │ - auth  │        │ - Jury      │     │ - TournamentRound
   │         │        │ - Score     │     │            │
   │         │        │ - Leaderboard     │            │
   └────┬────┘        └────┬────────┘     └──┬─────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    ┌──────▼──────┐
                    │ PostgreSQL  │
                    │             │
                    │ user_db     │
                    │ task_db     │
                    │ tournament_ │
                    │ db          │
                    └─────────────┘
```

---

## 1️⃣ Вимоги

- **Python 3.10+**
- **PostgreSQL 13+** (або SQLite для розробки)
- **pip** або **poetry**
- **Node.js 18+** (для frontend)
- **Git**

---

## 2️⃣ Встановлення

### A) Клонувати репозиторій

```bash
git clone <repository-url>
cd microservices-shop
```

### B) Встановити PostgreSQL

**Windows (через chocolatey):**
```bash
choco install postgresql
```

**macOS:**
```bash
brew install postgresql
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

Створити користувача та БД:
```sql
CREATE USER postgres WITH PASSWORD 'postgres';
CREATE DATABASE user_db OWNER postgres;
CREATE DATABASE task_db OWNER postgres;
CREATE DATABASE tournament_db OWNER postgres;
ALTER ROLE postgres SUPERUSER;
```

### C) Встановити Backend (Python)

**Windows PowerShell:**
```powershell
# Перейти до API Gateway
cd api-gateway
pip install -r requirements.txt
cp .env.example .env

# Перейти до кожного сервісу та встановити залежності
cd ../services/user-service
pip install -r requirements.txt
cp .env.example .env

cd ../submission-service
pip install -r requirements.txt
cp .env.example .env

cd ../tournament-service
pip install -r requirements.txt
cp .env.example .env
```

### D) Встановити Frontend (Node.js)

```bash
cd frontend
npm install
cp .env.example .env.local
```

---

## 3️⃣ Конфігурація

### A) Оновити .env файли

**api-gateway/.env:**
```
SECRET_KEY=your-super-secret-key-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**services/user-service/.env:**
```
SECRET_KEY=user-service-secret-key
DEBUG=True
DB_NAME=user_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

**services/submission-service/.env:**
```
SECRET_KEY=task-service-secret-key
DEBUG=True
DB_NAME=task_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

**services/tournament-service/.env:**
```
SECRET_KEY=tournament-service-secret-key
DEBUG=True
DB_NAME=tournament_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

### B) Мігрувати БД

Виконати в кожному сервісі:

```bash
# User Service
cd services/user-service
python manage.py migrate

# Task Service
cd ../submission-service
python manage.py migrate

# Tournament Service
cd ../tournament-service
python manage.py migrate
```

### C) Створити Super User (опціонально)

```bash
cd services/user-service
python manage.py createsuperuser
```

---

## 4️⃣ Запуск

### Варіант A: В окремих терміналах (для розроблення)

**Terminal 1 — PostgreSQL:**
```bash
# Windows
pg_ctl -D "C:\Program Files\PostgreSQL\14\data" start

# macOS
brew services start postgresql

# Linux
sudo service postgresql start
```

**Terminal 2 — API Gateway (8000):**
```bash
cd api-gateway
python manage.py runserver 8000
```

**Terminal 3 — User Service (8001):**
```bash
cd services/user-service
python manage.py runserver 8001
```

**Terminal 4 — Task Service (8002):**
```bash
cd services/submission-service
python manage.py runserver 8002
```

**Terminal 5 — Tournament Service (8003):**
```bash
cd services/tournament-service
python manage.py runserver 8003
```

**Terminal 6 — Frontend (3000/5173):**
```bash
cd frontend
npm run dev
```

### Варіант B: Docker Compose (для production)

Створити `docker-compose.yml` у root:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: user_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  user-service:
    build: ./services/user-service
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8001
    ports:
      - "8001:8001"
    depends_on:
      - postgres
    environment:
      DB_HOST: postgres

  task-service:
    build: ./services/submission-service
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8002
    ports:
      - "8002:8002"
    depends_on:
      - postgres
    environment:
      DB_HOST: postgres

  tournament-service:
    build: ./services/tournament-service
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8003
    ports:
      - "8003:8003"
    depends_on:
      - postgres
    environment:
      DB_HOST: postgres

  api-gateway:
    build: ./api-gateway
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - user-service
      - task-service
      - tournament-service

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      VITE_API_URL: http://api-gateway:8000

volumes:
  postgres_data:
```

Запустити:
```bash
docker-compose up -d
```

---

## 5️⃣ Перевірка

### A) API Gateway Health Check

```bash
curl http://localhost:8000/api/health/
```

**Очікуваний результат:**
```json
{
  "status": "healthy",
  "service": "api-gateway"
}
```

### B) User Service

```bash
# Отримати користувачів
curl http://localhost:8000/api/users/

# Логін
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password"}'
```

### C) Task Service

```bash
# Отримати завдання
curl http://localhost:8000/api/tasks/?tournament_id=1
```

### D) Tournament Service

```bash
# Отримати турніри
curl http://localhost:8000/api/tournaments/
```

---

## 6️⃣ Тестування

### Backend (Python)

```bash
cd services/user-service
pytest

cd ../submission-service
pytest

cd ../tournament-service
pytest
```

### Frontend (JavaScript)

```bash
cd frontend
npm run test
```

---

## 7️⃣ Усунення несправностей

### ❌ PostgreSQL Connection Error

**Рішення:**
```bash
# Перевірити чи запущена PostgreSQL
# Windows
pg_ctl status

# macOS
brew services list

# Linux
sudo systemctl status postgresql
```

### ❌ Port Already in Use

**Рішення:**
```bash
# Знайти процес на порті 8000 та вбити його
# Windows (PowerShell)
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### ❌ Migration Error

**Рішення:**
```bash
# Видалити всі міграції (крім __init__.py) та перестворити
python manage.py makemigrations
python manage.py migrate

# Якщо це не допоможе, reset БД
python manage.py migrate --fake app 0001
```

---

## 8️⃣ Структура URL API

Всі запити йдуть через API Gateway `http://localhost:8000`:

### User Service
- `GET /api/auth/me/` — поточний користувач
- `POST /api/auth/login/` — вхід
- `POST /api/auth/register/` — реєстрація

### Task Service
- `GET /api/tasks/` — список завдань
- `POST /api/tasks/` — створити завдання (admin)
- `POST /api/submissions/` — подати рішення
- `GET /api/jury-assignments/my_assignments/` — мої оцінки
- `GET /api/leaderboard/by_tournament/` — рейтинг

### Tournament Service
- `GET /api/tournaments/` — список турнірів
- `POST /api/tournaments/` — створити турнір (admin)
- `GET /api/tournaments/{id}/teams/` — команди турніру

---

## 9️⃣ Приклад повного Flow

```bash
# 1. Запустити PostgreSQL
# 2. Запустити всі сервіси в окремих терміналах
# 3. Очікувати на прив'язку до портів (1-2 сек)

# 4. Логін
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"team@example.com","password":"password"}'

# 5. Сохранить access token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# 6. Отримати турніри
curl http://localhost:8000/api/tournaments/ \
  -H "Authorization: Bearer $TOKEN"

# 7. Отримати завдання турніру
curl "http://localhost:8000/api/tasks/?tournament_id=1" \
  -H "Authorization: Bearer $TOKEN"

# 8. Подати рішення
curl -X POST http://localhost:8000/api/submissions/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "task": 1,
    "team_id": 10,
    "github_url": "https://github.com/team/project",
    "description": "Our solution"
  }'
```

---

## 🔟 Production Checklist

- [ ] Змінити SECRET_KEY на продакшен версії
- [ ] Встановити DEBUG=False
- [ ] Налаштувати ALLOWED_HOSTS
- [ ] Налаштувати CORS для фронтенда
- [ ] Встановити SSL сертифікати
- [ ] Налаштувати логування (ELK stack)
- [ ] Налаштувати моніторинг (Sentry, NewRelic)
- [ ] Налаштувати backup БД
- [ ] Налаштувати CI/CD (GitHub Actions, GitLab CI)

---

**Сервис успішно запущений! 🎉**

Для подробиці дивіться [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
