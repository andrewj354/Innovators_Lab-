# Турнірна Платформа — Посібник Розгортування та Тестування

## Зміст
1. [Вимоги](#вимоги)
2. [Швидкий Старт](#швидкий-старт)
3. [Локальне Розгортування](#локальне-розгортування)
4. [Docker Розгортування](#docker-розгортування)
5. [Тестування](#тестування)
6. [Архітектура](#архітектура)
7. [Усунення Неполадок](#усунення-неполадок)

---

## Вимоги

### Системні вимоги
- **ОС**: Linux, macOS або Windows (з WSL2)
- **Docker**: v20.10+
- **Docker Compose**: v1.29+
- **Python**: 3.11+ (для локального розгортування)
- **Node.js**: 18+ (для frontend)

### Опціональні інструменти
- Git
- PostgreSQL Client
- Redis CLI

---

## Швидкий Старт

### 1. Docker Compose (Рекомендується)

```bash
# Клонування репозиторію
git clone <repository-url>
cd Innovators_Lab-

# Запуск всіх сервісів
docker-compose up -d

# Перевірка статусу
docker-compose ps

# Перегляд логів
docker-compose logs -f
```

**Доступні адреси:**
- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- User Service: http://localhost:8001
- Task Service: http://localhost:8002
- Tournament Service: http://localhost:8003

---

## Локальне Розгортування

### 1. Налаштування Базової Бази Даних

```bash
# Установка PostgreSQL
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql
# Windows: Завантажити з postgresql.org

# Запуск PostgreSQL
# macOS: brew services start postgresql
# Ubuntu: sudo systemctl start postgresql
# Windows: запустити PostgreSQL сервіс

# Створення бази даних
psql -U postgres -c "CREATE DATABASE innovators_db;"
psql -U postgres -c "CREATE DATABASE user_db;"
psql -U postgres -c "CREATE DATABASE tournament_db;"
psql -U postgres -c "CREATE DATABASE submission_db;"

# Запуск Redis
# macOS: brew install redis && brew services start redis
# Ubuntu: sudo apt-get install redis-server && sudo systemctl start redis-server
# Windows: Використовувати WSL2 або Docker для Redis
```

### 2. Налаштування Backend Сервісів

#### User Service

```bash
cd services/user-service

# Створення віртуального середовища
python -m venv venv
source venv/bin/activate  # macOS/Linux
# або
venv\Scripts\activate  # Windows

# Установка залежностей
pip install -r requirements.txt

# Налаштування .env
cp .env.example .env
# Редагувати .env з DB credentials

# Міграції
python manage.py migrate

# Запуск сервісу
python manage.py runserver 8001
```

#### Tournament Service

```bash
cd services/tournament-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Редагувати .env

python manage.py migrate

python manage.py runserver 8003
```

#### Submission Service

```bash
cd services/submission-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

python manage.py migrate

python manage.py runserver 8002
```

#### API Gateway

```bash
cd api-gateway

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

python manage.py migrate

python manage.py runserver 8000
```

### 3. Налаштування Frontend

```bash
cd frontend

# Установка залежностей
npm install

# Запуск development сервера
npm run dev

# Построїння для продакшену
npm run build
```

---

## Docker Розгортування

### 1. Побудова образів

```bash
# Побудова всіх образів
docker-compose build

# Побудова окремого образу
docker-compose build api-gateway
docker-compose build user-service
docker-compose build tournament-service
docker-compose build submission-service
docker-compose build frontend
```

### 2. Запуск контейнерів

```bash
# Запуск у фоновому режимі
docker-compose up -d

# Запуск з виводом логів
docker-compose up

# Запуск окремого сервісу
docker-compose up -d user-service
```

### 3. Управління контейнерами

```bash
# Перегляд статусу
docker-compose ps

# Перегляд логів
docker-compose logs -f  # Всі сервіси
docker-compose logs -f user-service  # Окремий сервіс

# Зупинка контейнерів
docker-compose stop

# Запуск зупинених контейнерів
docker-compose start

# Перезапуск контейнерів
docker-compose restart

# Видалення контейнерів
docker-compose down

# Видалення з видаленням томів (БД)
docker-compose down -v
```

### 4. Налаштування容器

#### Доступ до PostgreSQL

```bash
# Через Docker
docker-compose exec postgres psql -U postgres -d innovators_db

# Видалення і повторне створення БД
docker-compose exec postgres dropdb -U postgres innovators_db
docker-compose exec postgres createdb -U postgres innovators_db
```

#### Запуск Django команд

```bash
# У контейнері
docker-compose exec user-service python manage.py migrate
docker-compose exec user-service python manage.py createsuperuser

# Або з Python
docker-compose exec user-service python manage.py shell
```

---

## Тестування

### 1. Unit Тести

#### Локально

```bash
# User Service
cd services/user-service
pytest --cov=apps --cov-report=html

# Tournament Service
cd services/tournament-service
pytest --cov=apps --cov-report=html

# Submission Service
cd services/submission-service
pytest --cov=apps --cov-report=html

# API Gateway
cd api-gateway
pytest --cov=apps --cov-report=html
```

#### У Docker

```bash
# Запуск тестів у контейнері
docker-compose exec user-service pytest --cov=apps
docker-compose exec tournament-service pytest --cov=apps
docker-compose exec submission-service pytest --cov=apps
docker-compose exec api-gateway pytest --cov=apps
```

### 2. Запуск всіх тестів

#### Linux/macOS

```bash
chmod +x run_tests.sh
./run_tests.sh
```

#### Windows

```bash
run_tests.bat
```

### 3. Integration Тести

```bash
# Перевірка API Gateway
curl http://localhost:8000/health/

# Перевірка User Service
curl http://localhost:8001/api/auth/health/

# Перевірка Tournament Service
curl http://localhost:8003/api/tournaments/health/

# Перевірка Submission Service
curl http://localhost:8002/api/tasks/health/
```

### 4. Frontend Тести

```bash
cd frontend

# Запуск лінтера
npm run lint

# Построїння та перевірка
npm run build
```

---

## Архітектура

### Мікросервісна Архітектура

```
┌─────────────────────────────────────────────┐
│            Frontend (React)                  │
│         http://localhost:3000               │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         API Gateway (Django)                │
│  Маршрутизація • CORS • Rate Limiting     │
│         http://localhost:8000              │
└──┬──────────────────┬───────────┬──────────┘
   │                  │           │
   ▼                  ▼           ▼
┌────────────┐   ┌────────────┐ ┌────────────┐
│User Service│   │Tournament  │ │Submission  │
│  :8001     │   │  :8003     │ │   :8002    │
│ JWT • Auth │   │  CRUD TM   │ │CRUD Tasks  │
└────────────┘   └────────────┘ └────────────┘
   │                  │           │
   └──────────────────┴───────────┘
              ▼
        ┌─────────────┐
        │ PostgreSQL  │
        │  :5432      │
        └─────────────┘
              ▼
        ┌─────────────┐
        │    Redis    │
        │  :6379      │
        └─────────────┘
```

### Структура БД

Кожен мікросервіс має власну БД:
- `user_db` — користувачі, автентифікація, профілі
- `tournament_db` — турніри, команди, розклад
- `submission_db` — завдання, подачі, оцінки
- `rank_db` — оцінювання журі, leaderboard

---

## Усунення Неполадок

### Проблема: Контейнери не стартують

```bash
# Перевірити логи
docker-compose logs

# Перевірити, чи займаті порти
docker ps
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Видалити і перебудувати
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Проблема: Помилка підключення до БД

```bash
# Перевірити PostgreSQL контейнер
docker-compose ps postgres

# Перевірити логи
docker-compose logs postgres

# Перезапустити БД
docker-compose restart postgres

# Пересоздати БД
docker-compose exec postgres dropdb -U postgres -f innovators_db
docker-compose exec postgres createdb -U postgres innovators_db
docker-compose exec api-gateway python manage.py migrate
```

### Проблема: Тести не проходять

```bash
# Перевірити, чи встановлені залежності
pip install -r requirements.txt

# Перевірити налаштування БД в конфігурації тестів
cat pytest.ini

# Запустити з verbose output
pytest -v --tb=short

# Запустити конкретний тест
pytest apps/users/tests.py::UserModelTest::test_create_user -v
```

### Проблема: Frontend не з'єднується з API

```bash
# Перевірити .env файл
cat frontend/.env.example

# Перевірити VITE_API_URL
# Має бути http://localhost:8000 для локального запуску

# Перевірити CORS налаштування
curl -H "Origin: http://localhost:3000" -i http://localhost:8000/api/users/
```

### Проблема: Недостатньо пам'яті для Docker

```bash
# Збільшити памяті Docker
# Docker Desktop → Preferences → Resources → Memory: 4GB+

# Видалити невикористовувані об'єкти
docker system prune -a
docker volume prune
```

---

## Перевірка Здоров'я (Health Checks)

### API Gateway Health

```bash
curl http://localhost:8000/health/
```

### User Service Health

```bash
curl http://localhost:8001/api/auth/health/
```

### Tournament Service Health

```bash
curl http://localhost:8003/api/tournaments/health/
```

### Submission Service Health

```bash
curl http://localhost:8002/api/tasks/health/
```

---

## Середовищні Змінні

### .env файли

Кожен сервіс потребує `.env` файлу. Приклади є в `.env.example`.

#### API Gateway (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/innovators_db
REDIS_URL=redis://localhost:6379/0
```

#### User Service (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/user_db
REDIS_URL=redis://localhost:6379/1
JWT_SECRET=your-jwt-secret
```

---

## Продакшн Розгортування

### Рекомендації

1. **Змініть SECRET_KEY** для всіх сервісів
2. **Включіть DEBUG = False**
3. **Налаштуйте ALLOWED_HOSTS**
4. **Використовуйте SSL/TLS**
5. **Налаштуйте правильні баз даних**
6. **Включіть логування**
7. **Налаштуйте backup стратегію**

### Docker Stack для Продакшну

```bash
# Використовувати docker stack deploy
docker stack deploy -c docker-compose.prod.yml tournament-platform

# Або Kubernetes
kubectl apply -f k8s/
```

---

## Корисні Команди

```bash
# Очистити всі Docker об'єкти
docker system prune -a --volumes

# Переглянути використання ресурсів
docker stats

# Доступ до контейнера
docker-compose exec service-name bash

# Скопіювати файли з контейнера
docker cp container-name:/path/to/file ./local/path

# Посилання на сервіси всередині Docker Compose
# http://service-name:port (напр. http://postgres:5432)
```

---

## Контакти та Підтримка

- Документація: [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- Архітектура: [ARCHITECTURE.md](./ARCHITECTURE.md)
- Статус: [COMPLETION_STATUS.md](./COMPLETION_STATUS.md)

---

**Останнє оновлення:** Січень 2025
