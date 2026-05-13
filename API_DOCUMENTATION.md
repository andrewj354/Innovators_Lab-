# API Documentation for Frontend Developers

**Базовий URL для всіх запитів**: `http://localhost:8000/api/`

---

## 📋 Зміст
1. [Authentication](#authentication)
2. [Tasks API](#tasks-api)
3. [Submissions API](#submissions-api)
4. [Jury API](#jury-api)
5. [Leaderboard API](#leaderboard-api)
6. [Error Handling](#error-handling)

---

## Authentication

### 1️⃣ Вхід до системи
```
POST /api/auth/login/
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "team"  // або "jury", "admin"
  }
}
```

### 2️⃣ Оновити токен (коли закінчився access)
```
POST /api/auth/refresh/
Content-Type: application/json

Request:
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3️⃣ Реєстрація
```
POST /api/auth/register/
Content-Type: application/json

Request:
{
  "email": "newuser@example.com",
  "password": "password123",
  "name": "Jane Doe",
  "role": "team"  // "team" або "jury"
}

Response: 201 Created
{
  "id": 2,
  "email": "newuser@example.com",
  "name": "Jane Doe",
  "role": "team"
}
```

### 4️⃣ Отримати поточного користувача
```
GET /api/auth/me/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "team"
}
```

---

## Tasks API

### 1️⃣ Список завдань для турніру
```
GET /api/tasks/?tournament_id=1&status=published
Authorization: Bearer {access_token}

Query Parameters:
- tournament_id: int (обов'язково)
- status: "draft" | "published" | "closed" (опціонально)
- ordering: "-deadline" | "deadline" | "-created_at" (опціонально)

Response: 200 OK
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "tournament_id": 1,
      "title": "Build a REST API",
      "deadline": "2026-05-20T18:00:00Z",
      "status": "published",
      "is_active": true,
      "time_remaining": "2d 5h",  // Формат: "Xd Yh" або "Deadline passed"
      "requirements_count": 3
    },
    ...
  ]
}
```

### 2️⃣ Детальна інформація про завдання
```
GET /api/tasks/{task_id}/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "tournament_id": 1,
  "created_by": 5,
  "title": "Build a REST API",
  "description": "Create a REST API using Django...",
  "tech_requirements": {...},
  "start_time": "2026-05-13T10:00:00Z",
  "deadline": "2026-05-20T18:00:00Z",
  "status": "published",
  "is_active": true,
  "time_remaining": 3600000,  // У секундах
  "requirements": [
    {
      "id": 1,
      "title": "Must use PostgreSQL",
      "is_required": true
    },
    {
      "id": 2,
      "title": "API documentation (Swagger)",
      "is_required": false
    }
  ],
  "submissions_count": 5,
  "created_at": "2026-05-10T10:00:00Z",
  "updated_at": "2026-05-10T10:00:00Z"
}
```

### 3️⃣ Вимоги до завдання
```
GET /api/tasks/{task_id}/requirements/
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "id": 1,
    "title": "Must use PostgreSQL",
    "is_required": true
  },
  {
    "id": 2,
    "title": "Docker support",
    "is_required": false
  }
]
```

### 4️⃣ Додати вимогу (Admin only)
```
POST /api/tasks/{task_id}/add_requirement/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "title": "Must have unit tests",
  "is_required": true
}

Response: 201 Created
{
  "id": 3,
  "title": "Must have unit tests",
  "is_required": true
}
```

### 5️⃣ Статистика завдання
```
GET /api/tasks/{task_id}/statistics/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "title": "Build a REST API",
  "tournament_id": 1,
  "status": "published",
  "is_active": true,
  "is_deadline_passed": false,
  "deadline": "2026-05-20T18:00:00Z",
  "total_submissions": 5,
  "locked_submissions": 2,
  "requirements": 3,
  "must_have_requirements": 2
}
```

### 6️⃣ Створити завдання (Admin only)
```
POST /api/tasks/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "tournament_id": 1,
  "title": "Build a mobile app",
  "description": "Create a mobile application using React Native...",
  "tech_requirements": {
    "language": "JavaScript",
    "framework": "React Native"
  },
  "start_time": "2026-05-25T10:00:00Z",
  "deadline": "2026-06-01T18:00:00Z",
  "status": "published",
  "requirements": [
    {
      "title": "iOS app works",
      "is_required": true
    },
    {
      "title": "Android app works",
      "is_required": true
    }
  ]
}

Response: 201 Created
{
  "id": 2,
  "tournament_id": 1,
  "created_by": 5,
  "title": "Build a mobile app",
  ...
}
```

### 7️⃣ Оновити завдання (Admin only)
```
PUT /api/tasks/{task_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "title": "Build a mobile app (Updated)",
  "status": "closed"
}

Response: 200 OK
{
  "id": 2,
  "title": "Build a mobile app (Updated)",
  "status": "closed",
  ...
}
```

---

## Submissions API

### 1️⃣ Список подач для задачи
```
GET /api/submissions/?task={task_id}&team_id=10
Authorization: Bearer {access_token}

Query Parameters:
- task: int (FK до Task, обов'язково для фільтрації)
- team_id: int (опціонально)
- is_locked: true | false (опціонально)

Response: 200 OK
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "task": 1,
      "task_title": "Build a REST API",
      "team_id": 10,
      "is_locked": false,
      "can_edit": true,
      "submitted_at": "2026-05-18T15:30:00Z"
    },
    ...
  ]
}
```

### 2️⃣ Отримати подачу команди
```
GET /api/submissions/{submission_id}/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "task": 1,
  "task_details": {
    "id": 1,
    "title": "Build a REST API",
    "deadline": "2026-05-20T18:00:00Z",
    "is_active": true,
    "is_deadline_passed": false
  },
  "team_id": 10,
  "github_url": "https://github.com/team/project",
  "video_url": "https://youtube.com/watch?v=...",
  "live_demo_url": "https://demo.example.com",
  "description": "We built a REST API with...",
  "is_locked": false,
  "can_edit": true,
  "submitted_at": "2026-05-18T15:30:00Z",
  "updated_at": "2026-05-18T16:45:00Z"
}
```

### 3️⃣ Створити подачу (Team)
```
POST /api/submissions/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "task": 1,
  "team_id": 10,
  "github_url": "https://github.com/team/project",
  "video_url": "https://youtube.com/watch?v=...",
  "live_demo_url": "https://demo.example.com",
  "description": "Our approach was..."
}

Response: 201 Created
{
  "id": 1,
  "task": 1,
  "team_id": 10,
  "github_url": "https://github.com/team/project",
  ...
}

Errors:
- 400: "Cannot submit after deadline"
- 400: "Team already submitted to this task"
```

### 4️⃣ Оновити подачу (Team, до дедлайну)
```
PUT /api/submissions/{submission_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "github_url": "https://github.com/team/project-updated",
  "description": "We updated our approach..."
}

Response: 200 OK
{
  "id": 1,
  "github_url": "https://github.com/team/project-updated",
  ...
}

Errors:
- 400: "Cannot submit after deadline"
- 403: "Submission is locked"
```

### 5️⃣ Заблокувати подачу (Admin)
```
POST /api/submissions/{submission_id}/lock/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "status": "success",
  "message": "Submission locked",
  "is_locked": true
}
```

### 6️⃣ Розблокувати подачу (Admin)
```
POST /api/submissions/{submission_id}/unlock/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "status": "success",
  "message": "Submission unlocked",
  "is_locked": false
}
```

### 7️⃣ Оцінки для подачи
```
GET /api/submissions/{submission_id}/jury_assignments/
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "id": 1,
    "submission": 1,
    "submission_info": {
      "github_url": "https://github.com/team/project",
      "video_url": "https://youtube.com/watch?v=...",
      "live_demo_url": "https://demo.example.com"
    },
    "is_evaluated": true,
    "score": {
      "id": 1,
      "backend_code": 85,
      "database": 90,
      "frontend_code": 80,
      "functionality": 95,
      "usability": 88,
      "comment": "Great work!",
      "average_score": 87.6,
      "total_score": 438,
      "evaluated_at": "2026-05-19T10:00:00Z"
    },
    "assigned_at": "2026-05-18T18:00:00Z"
  }
]
```

### 8️⃣ Подачи команди
```
GET /api/submissions/by_team/?team_id=10
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "id": 1,
    "task": 1,
    "task_title": "Build a REST API",
    "team_id": 10,
    "is_locked": false,
    "can_edit": true,
    "submitted_at": "2026-05-18T15:30:00Z"
  },
  ...
]
```

---

## Jury API

### 1️⃣ Мої призначення
```
GET /api/jury-assignments/my_assignments/
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "id": 1,
    "submission": 1,
    "submission_info": {
      "github_url": "https://github.com/team/project",
      "video_url": "https://youtube.com/watch?v=...",
      "live_demo_url": "https://demo.example.com"
    },
    "team_id": 10,
    "is_evaluated": false,
    "score": null,
    "assigned_at": "2026-05-18T18:00:00Z"
  },
  ...
]
```

### 2️⃣ Мої невиконані завдання
```
GET /api/jury-assignments/pending/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "count": 3,
  "assignments": [
    {
      "id": 1,
      "submission": 1,
      "submission_info": {...},
      "team_id": 10,
      "is_evaluated": false,
      "score": null,
      "assigned_at": "2026-05-18T18:00:00Z"
    },
    ...
  ]
}
```

### 3️⃣ Деталі призначення
```
GET /api/jury-assignments/{assignment_id}/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "submission": 1,
  "submission_details": {
    "team_id": 10,
    "task_title": "Build a REST API",
    "task_description": "Create a REST API using Django...",
    "github_url": "https://github.com/team/project",
    "video_url": "https://youtube.com/watch?v=...",
    "live_demo_url": "https://demo.example.com",
    "requirements": [
      {
        "title": "Must use PostgreSQL",
        "is_required": true
      },
      {
        "title": "API documentation",
        "is_required": false
      }
    ]
  },
  "jury_user_id": 5,
  "is_evaluated": false,
  "scores": [],
  "assigned_at": "2026-05-18T18:00:00Z"
}
```

### 4️⃣ Позначити як оцінене
```
POST /api/jury-assignments/{assignment_id}/mark_as_evaluated/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "status": "success",
  "message": "Assignment marked as evaluated",
  "is_evaluated": true
}
```

### 5️⃣ Розподілити завдання (Admin only)
```
POST /api/jury-assignments/distribute_tasks/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "submission_ids": [1, 2, 3, 4, 5],
  "jury_ids": [5, 6, 7],
  "tasks_per_jury": 3  // Кількість завдань на журі (опціонально, default=3)
}

Response: 200 OK
{
  "status": "success",
  "created_assignments": 12
}
```

---

## Scores API

### 1️⃣ Оцінити подачу
```
POST /api/scores/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "assignment": 1,
  "backend_code": 85,
  "database": 90,
  "frontend_code": 80,
  "functionality": 95,
  "usability": 88,
  "comment": "Great implementation! Consider improving error handling."
}

Response: 201 Created
{
  "id": 1,
  "assignment": 1,
  "backend_code": 85,
  "database": 90,
  "frontend_code": 80,
  "functionality": 95,
  "usability": 88,
  "comment": "Great implementation!...",
  "average_score": 87.6,
  "total_score": 438,
  "evaluated_at": "2026-05-19T10:00:00Z"
}

Errors:
- 400: "All scores must be between 0 and 100"
```

### 2️⃣ Оновити оцінку
```
PUT /api/scores/{score_id}/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "backend_code": 87,
  "comment": "Updated comment"
}

Response: 200 OK
{
  "id": 1,
  "backend_code": 87,
  ...
}
```

### 3️⃣ Порівняти оцінки для подачи
```
GET /api/scores/{score_id}/comparison/
Authorization: Bearer {access_token}

Response: 200 OK
{
  "submission_id": 1,
  "team_id": 10,
  "scores": [
    {
      "id": 1,
      "assignment": 1,
      "backend_code": 85,
      "database": 90,
      "frontend_code": 80,
      "functionality": 95,
      "usability": 88,
      "average_score": 87.6
    },
    {
      "id": 2,
      "assignment": 2,
      "backend_code": 80,
      "database": 85,
      "frontend_code": 85,
      "functionality": 90,
      "usability": 82,
      "average_score": 84.4
    }
  ],
  "average": {
    "backend_code": 82.5,
    "database": 87.5,
    "frontend_code": 82.5,
    "functionality": 92.5,
    "usability": 85
  }
}
```

---

## Leaderboard API

### 1️⃣ Лідербордом для турніру
```
GET /api/leaderboard/by_tournament/?tournament_id=1
Authorization: Bearer {access_token}

Response: 200 OK
[
  {
    "rank": 1,
    "team_id": 10,
    "total_score": 87.6,
    "calculated_at": "2026-05-19T12:00:00Z"
  },
  {
    "rank": 2,
    "team_id": 11,
    "total_score": 84.4,
    "calculated_at": "2026-05-19T12:00:00Z"
  },
  {
    "rank": 3,
    "team_id": 12,
    "total_score": 81.2,
    "calculated_at": "2026-05-19T12:00:00Z"
  }
]
```

### 2️⃣ Топ команди турніру
```
GET /api/leaderboard/top_teams/?tournament_id=1&limit=10
Authorization: Bearer {access_token}

Response: 200 OK
{
  "tournament_id": 1,
  "top_count": 10,
  "teams": [
    {
      "rank": 1,
      "team_id": 10,
      "total_score": 87.6,
      "calculated_at": "2026-05-19T12:00:00Z"
    },
    ...
  ]
}
```

### 3️⃣ Пересчитати лідербордом (Admin)
```
POST /api/leaderboard/recalculate/
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "tournament_id": 1
}

Response: 200 OK
{
  "status": "success"
}
```

---

## Error Handling

### Всі помилки повертають JSON з даною структурою:

```json
{
  "error": "Error message",
  "status_code": 400,
  "detail": "Additional details if available"
}
```

### Які статус-коди ви отримаєте:

| Код | Значення | Приклад |
|-----|----------|---------|
| 200 | ✅ OK | Успішний запит |
| 201 | ✅ Created | Новий ресурс створений |
| 400 | ❌ Bad Request | Неправильні дані |
| 401 | ❌ Unauthorized | Немає токена |
| 403 | ❌ Forbidden | Немає прав доступу |
| 404 | ❌ Not Found | Ресурс не знайдений |
| 409 | ❌ Conflict | Дублювання (наприклад, команда вже подала) |

### Приклад помилки при виконанні:
```
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "github_url": ["Invalid URL format"],
  "team_id": ["This field may not be null"]
}
```

---

## Примітки для фронтендерів

### 🔐 Authorization
Всі запити крім `/api/auth/login/` та `/api/auth/register/` потребують:
```
Authorization: Bearer {access_token}
```

### 📅 Формат дати/часу
Всі дати повертаються у форматі ISO 8601:
```
2026-05-19T10:00:00Z
```

На фронті конвертуйте:
```javascript
const deadline = new Date("2026-05-20T18:00:00Z");
console.log(deadline.toLocaleString('uk-UA'));  // 20.05.2026, 21:00:00
```

### 🎯 Логіка фронтенду для подач:
```javascript
// 1. Перевірити чи можна редагувати
if (submission.can_edit) {
  // Показати форму редагування
} else if (submission.is_locked) {
  // Показати "Submission locked"
} else {
  // Показати "Deadline passed"
}

// 2. Якщо дедлайн близько, показати таймер
const timeRemaining = task.time_remaining;  // У секундах
if (timeRemaining < 86400) {  // Менше 24 годин
  // Показати червоний таймер
}
```

### 📊 Таблиця статусів завдань:
- **draft** 🟡 - Завдання створене але ще не опубліковане (видно тільки admin)
- **published** 🟢 - Завдання опубліковане і команди можуть подавати
- **closed** 🔴 - Дедлайн пройшов, подачи заблоковані

### 👥 Ролі користувачів:
- **admin** - Може створювати завдання, розподіляти роботи, закривати реєстрацію
- **jury** - Может оцінювати роботи
- **team** - Може подавати рішення

---

## Приклад повного flow

```javascript
// 1. Login
const loginRes = await fetch('/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'team@example.com',
    password: 'password123'
  })
});
const { access } = await loginRes.json();

// 2. Отримати завдання для турніру
const tasksRes = await fetch('/api/tasks/?tournament_id=1&status=published', {
  headers: { 'Authorization': `Bearer ${access}` }
});
const tasks = await tasksRes.json();

// 3. Отримати деталі першого завдання
const taskRes = await fetch(`/api/tasks/${tasks.results[0].id}/`, {
  headers: { 'Authorization': `Bearer ${access}` }
});
const task = await taskRes.json();

// 4. Подати рішення
const submitRes = await fetch('/api/submissions/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access}`
  },
  body: JSON.stringify({
    task: task.id,
    team_id: 10,
    github_url: 'https://github.com/team/project',
    video_url: 'https://youtube.com/watch?v=...',
    live_demo_url: 'https://demo.example.com',
    description: 'Our approach...'
  })
});
const submission = await submitRes.json();
```

---

**Версія**: 1.0.0  
**Остання оновлення**: 12 травня 2026  
**Статус**: ✅ Готово для використання
