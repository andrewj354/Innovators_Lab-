# 🧪 Посібник Тестування Турнірної Платформи

## Зміст

1. [Огляд](#огляд)
2. [Setup Тестування](#setup-тестування)
3. [Запуск Тестів](#запуск-тестів)
4. [Тестування Сервісів](#тестування-сервісів)
5. [Покриття Кодом](#покриття-кодом)
6. [Best Practices](#best-practices)
7. [Неполадки](#неполадки)

---

## Огляд

### Фреймворки Тестування

| Фреймворк | Використання |
|-----------|-------------|
| pytest | Unit & Integration тести (Python) |
| pytest-django | Django тесты |
| pytest-cov | Вимірювання покриття |
| factory-boy | Создание тестових даних |
| responses | Mock HTTP запитів |

### Типи Тестів

| Тип | Опис | Місцеположення |
|-----|------|---------------|
| **Unit тести** | Тестування окремих функцій/методів | `apps/*/tests.py` |
| **Integration тести** | Тестування взаємодії компонентів | `apps/*/tests.py` |
| **API тести** | Тестування HTTP endpoints | `apps/*/tests.py` |
| **Gateway тести** | Тестування маршрутизації | `api-gateway/apps/gateway/tests.py` |

---

## Setup Тестування

### 1. Установка Залежностей

```bash
# Для кожного сервісу
cd services/user-service
pip install -r requirements.txt
# або
pip install pytest pytest-django pytest-cov factory-boy
```

### 2. Налаштування pytest.ini

Файл `pytest.ini` у кожному сервісі:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=apps
    --cov-report=term-missing
    --cov-report=html
    -v
testpaths = apps
```

### 3. Конфігурація conftest.py

```python
import pytest
import django
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup():
    """Налаштування тестової БД"""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
```

---

## Запуск Тестів

### 1. Запуск Всіх Тестів

#### Локально

```bash
# Всі тести всіх сервісів
./run_tests.sh          # Linux/macOS
run_tests.bat           # Windows

# З деталізованим виводом
pytest -v -s

# З покриттям
pytest --cov=apps --cov-report=html
```

#### У Docker

```bash
# User Service
docker-compose exec user-service pytest

# Tournament Service
docker-compose exec tournament-service pytest

# Submission Service
docker-compose exec submission-service pytest

# API Gateway
docker-compose exec api-gateway pytest
```

### 2. Запуск Конкретних Тестів

```bash
# Конкретний файл
pytest apps/users/tests.py -v

# Конкретний клас
pytest apps/users/tests.py::UserModelTest -v

# Конкретний метод
pytest apps/users/tests.py::UserModelTest::test_create_user -v

# За маркером
pytest -m django_db

# За ключовим словом
pytest -k "test_create" -v
```

### 3. Параметри pytest

```bash
# Короткий вивід
pytest -q

# Довгий вивід
pytest -vv

# З дамп локалей при помилці
pytest -l

# З інтерпретатором при помилці
pytest --pdb

# Зупинити при першій помилці
pytest -x

# Зупинити після N помилок
pytest --maxfail=3

# Послідовність тестів випадкова
pytest --random-order

# Повторити тести 3 рази
pytest --count=3
```

---

## Тестування Сервісів

### User Service

```bash
cd services/user-service

# Всі тести
pytest

# Тести моделей
pytest apps/users/tests.py::UserModelTest -v

# Тести автентифікації
pytest apps/authentication/tests.py -v

# Тести з покриттям
pytest --cov=apps --cov-report=html
```

#### Тестові Класи

```python
# apps/users/tests.py
class UserModelTest        # Тести моделі User
class UserProfileModelTest # Тести моделі UserProfile
class UserSerializerTest   # Тести serializer
class UserAPITest          # Тести API endpoints

# apps/authentication/tests.py
class AuthenticationTest   # Тести auth endpoints
```

### Tournament Service

```bash
cd services/tournament-service

# Всі тести
pytest

# Тести турнірів
pytest apps/tournaments/tests.py::TestTournamentModel -v

# Тести команд
pytest apps/tournaments/tests.py::TestTeamModel -v
```

#### Тестові Класи

```python
class TestUserModel
class TestTournamentModel
class TestTeamModel
class TestTeamMemberModel
class TestTaskModel
class TestTaskRequirementModel
```

### Submission Service

```bash
cd services/submission-service

pytest

# Конкретна моделі
pytest apps/submissions/tests.py::TestSubmissionModel -v
pytest apps/submissions/tests.py::TestJuryAssignmentModel -v
pytest apps/submissions/tests.py::TestScoreModel -v
```

#### Тестові Класи

```python
class TestSubmissionModel         # Тести подач
class TestJuryAssignmentModel     # Тести призначень журі
class TestScoreModel              # Тести оцінок
class TestLeaderboardModel        # Тести leaderboard
```

### API Gateway

```bash
cd api-gateway

pytest

# Тести маршрутизації
pytest apps/gateway/tests.py::GatewayRoutingTest -v

# Тести middleware
pytest apps/gateway/tests.py::GatewayMiddlewareTest -v
```

---

## Покриття Кодом

### Генерування звіту

```bash
# HTML звіт
pytest --cov=apps --cov-report=html

# Відкрити звіт
open htmlcov/index.html          # macOS
xdg-open htmlcov/index.html      # Linux
start htmlcov\index.html         # Windows
```

### Мінімальне покриття

```bash
# Требувати 80% покриття
pytest --cov=apps --cov-fail-under=80

# Вивести невкриті рядки
pytest --cov=apps --cov-report=term-missing
```

### Аналіз Звіту

Шукайте файли з низьким покриттям:

```python
# Good (>80%)
apps/models.py ................................. 100%
apps/serializers.py ............................ 95%

# Потребує уваги (<50%)
apps/views.py .................................. 45%
```

---

## Best Practices

### 1. Структура Тесту

```python
class UserModelTest(TestCase):
    """Тести моделі User"""
    
    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpass123',
        }
    
    def tearDown(self):
        """Очистка після кожного тесту"""
        pass
    
    def test_create_user(self):
        """Тест створення користувача"""
        # Arrange
        expected_email = self.user_data['email']
        
        # Act
        user = User.objects.create_user(**self.user_data)
        
        # Assert
        self.assertEqual(user.email, expected_email)
        self.assertTrue(user.check_password(self.user_data['password']))
```

### 2. Фікстури

```python
import pytest
from factory import django as factory_django

@pytest.fixture
def user_factory():
    """Фікстура для створення користувачів"""
    class UserFactory(factory_django.DjangoModelFactory):
        class Meta:
            model = User
        email = 'test@example.com'
        username = 'testuser'
    return UserFactory

@pytest.mark.django_db
def test_with_fixture(user_factory):
    user = user_factory.create()
    assert user.email == 'test@example.com'
```

### 3. Мокування

```python
from unittest.mock import patch, MagicMock

@patch('requests.get')
def test_external_api_call(mock_get):
    mock_get.return_value.json.return_value = {'status': 'ok'}
    
    result = call_external_api()
    
    assert result['status'] == 'ok'
    mock_get.assert_called_once()
```

### 4. Тестування API

```python
from rest_framework.test import APITestCase
from rest_framework import status

class UserAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='api@example.com',
            password='testpass123'
        )
    
    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'email': 'new@example.com', 'password': 'newpass123'}
        response = self.client.post('/api/users/', data)
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_403_FORBIDDEN
        ])
```

### 5. Параметризовані Тести

```python
import pytest

@pytest.mark.parametrize('email,valid', [
    ('valid@example.com', True),
    ('invalid-email', False),
    ('another@test.com', True),
])
def test_email_validation(email, valid):
    result = validate_email(email)
    assert result == valid
```

---

## Неполадки

### Проблема: Тести не можуть знайти Django

```bash
# Розв'язок: Встановити DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=config.settings
pytest

# Або у conftest.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
```

### Проблема: Помилка "DisallowedHost"

```python
# Розв'язок: Налаштувати ALLOWED_HOSTS в test settings
ALLOWED_HOSTS = ['*']  # Або конкретні хости
```

### Проблема: Тести не видяті

```bash
# Перевірити, що файл називається tests.py або test_*.py
# Перевірити, що тести у пакеті з __init__.py
# Перевірити pytest.ini conifg

pytest --collect-only  # Показати всі тести
```

### Проблема: Помилка "No such table"

```bash
# Розв'язок: Міграції не застосовані
python manage.py migrate --run-syncdb
pytest

# Або у conftest.py автоматично
os.environ['DJANGO_DB_ENGINE'] = 'sqlite'
```

### Проблема: Помилка "Permission denied" на Docker

```bash
# Розв'язок: Дати дозвіл на виконання
chmod +x run_tests.sh

# Або запустити напрямки
bash run_tests.sh
```

---

## CI/CD Інтеграція

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest --cov=apps --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Корисні Команди

```bash
# Список всіх тестів
pytest --collect-only

# Запуск з налагодженням
pytest --pdb

# Запуск останніх помилкових тестів
pytest --lf

# Запуск невдалих тестів
pytest --ff

# Профайлинг тестів (яких найдовше)
pytest --durations=10

# Запуск окремого тесту з точкою зупинки
pytest apps/users/tests.py::UserModelTest::test_create_user -s
```

---

## Контрольний Список для Розробника

- [ ] Написати тести перед кодом (TDD)
- [ ] Покриття новоого коду >= 80%
- [ ] Тести проходять локально
- [ ] Тести проходять у Docker
- [ ] Немає попереджень при запуску лінтера
- [ ] Додано коментарі до складних тестів
- [ ] Тести не залежать від порядку виконання
- [ ] Тести чистять дані після себе

---

**Версія**: 1.0.0  
**Остання оновлення**: Січень 2025
