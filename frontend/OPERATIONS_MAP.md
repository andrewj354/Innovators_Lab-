# Карта операцій Frontend

Цей файл показує усі можливі операції на фронтенді.

## 🔴 Auth (Аутентифікація)

| Операція | API | Сторінка | Статус |
|---------|-----|---------|--------|
| Логін | `POST /auth/login/` | LoginPage | ✅ Існує |
| Реєстрація | `POST /auth/register/` | RegisterPage | ✅ Існує |
| Забув пароль | `POST /auth/forgot-password/` | ForgotPasswordPage | ✅ Існує |
| Скидання пароля | `POST /auth/reset-password/` | ResetPasswordPage | ✅ Існує |
| 2FA верифікація | `POST /auth/verify-2fa/` | Verify2FA | ✅ Існує |

## 🎮 Tournaments (Турніри)

| Операція | API | Маршрут | Статус |
|---------|-----|---------|--------|
| Список турнірів | `GET /tournaments/` | `/tournaments` | ✅ Існує |
| Деталі турніру | `GET /tournaments/{id}/` | `/tournaments/:id` | ✅ Існує |
| Створити турнір | `POST /tournaments/` | `/tournaments/new` | ✅ Форма |
| Оновити турнір | `PUT /tournaments/{id}/` | `/tournaments/:id/edit` | ✅ Форма |

## 📋 Tasks (Завдання)

| Операція | API | Маршрут | Статус |
|---------|-----|---------|--------|
| Список завдань | `GET /tasks/?tournament_id=X` | `/tournaments/:id/tasks` | ✅ **НОВЕ** |
| Деталі завдання | `GET /tasks/{id}/` | `/tasks/:id` | ✅ **НОВЕ** |
| Вимоги завдання | `GET /tasks/{id}/requirements/` | (у деталях) | ✅ **НОВЕ** |
| Статистика завдання | `GET /tasks/{id}/statistics/` | (для адміну) | 🔲 TODO |
| Створити завдання | `POST /tasks/` | 🔲 TODO | 🔲 TODO |
| Оновити завдання | `PUT /tasks/{id}/` | 🔲 TODO | 🔲 TODO |
| Додати вимогу | `POST /tasks/{id}/add_requirement/` | 🔲 TODO | 🔲 TODO |

## 📤 Submissions (Подачи)

| Операція | API | Маршрут | Статус |
|---------|-----|---------|--------|
| Список подач | `GET /submissions/?task=X` | `/submissions` | ✅ **НОВЕ** |
| Деталі подачи | `GET /submissions/{id}/` | `/submissions/:id` | ✅ **НОВЕ** |
| Подачи команди | `GET /submissions/by_team/?team_id=X` | `/submissions?team=X` | ✅ **НОВЕ** |
| Створити подачу | `POST /submissions/` | `/submissions/new` | ✅ **НОВЕ** |
| Оновити подачу | `PUT /submissions/{id}/` | (редагування) | ✅ **НОВЕ** |
| Заблокувати подачу | `POST /submissions/{id}/lock/` | (для адміну) | 🔲 TODO |
| Розблокувати подачу | `POST /submissions/{id}/unlock/` | (для адміну) | 🔲 TODO |
| Оцінки для подачи | `GET /submissions/{id}/jury_assignments/` | 🔲 TODO | 🔲 TODO |

## ⭐ Scores (Оцінки)

| Операція | API | Сторінка | Статус |
|---------|-----|---------|--------|
| Оцінити подачу | `POST /scores/` | `/jury/assignments/:id` | ✅ **НОВЕ** |
| Оновити оцінку | `PUT /scores/{id}/` | (редагування оцінки) | ✅ **НОВЕ** |
| Порівняти оцінки | `GET /scores/{id}/comparison/` | 🔲 TODO | 🔲 TODO |

## 👨‍⚖️ Jury (Журі)

| Операція | API | Маршрут | Статус |
|---------|-----|---------|--------|
| Мої призначення | `GET /jury-assignments/my_assignments/` | `/jury/assignments` | ✅ **НОВЕ** |
| Невиконані завдання | `GET /jury-assignments/pending/` | (фільтр) | ✅ **НОВЕ** |
| Деталі призначення | `GET /jury-assignments/{id}/` | `/jury/assignments/:id` | ✅ **НОВЕ** |
| Позначити як оцінене | `POST /jury-assignments/{id}/mark_as_evaluated/` | (після оцінки) | ✅ **НОВЕ** |
| Розподілити завдання | `POST /jury-assignments/distribute_tasks/` | 🔲 TODO | 🔲 TODO |

## 🏆 Leaderboard (Лідербордом)

| Операція | API | Маршрут | Статус |
|---------|-----|---------|--------|
| Лідербордом турніру | `GET /leaderboard/by_tournament/?tournament_id=X` | `/tournaments/:id/leaderboard` | ✅ **НОВЕ** |
| Топ команди | `GET /leaderboard/top_teams/?tournament_id=X&limit=X` | (у лідербордом) | ✅ **НОВЕ** |
| Пересчет лідербордом | `POST /leaderboard/recalculate/` | 🔲 TODO | 🔲 TODO |

## Легенда

| Статус | Значення |
|--------|----------|
| ✅ Існує | Сторінка/операція повністю реалізована |
| ✅ **НОВЕ** | Щойно створене для цього релізу |
| 🔲 TODO | Потребує розробки |
| 🚧 WIP | В процесі розробки |

## 📊 Статистика

| Категорія | Всього | Готові | TODO |
|-----------|--------|--------|------|
| **Auth операції** | 5 | 5 | 0 |
| **Tournament операції** | 4 | 4 | 0 |
| **Task операції** | 7 | 3 | 4 |
| **Submission операції** | 8 | 7 | 1 |
| **Score операції** | 3 | 2 | 1 |
| **Jury операції** | 5 | 4 | 1 |
| **Leaderboard операції** | 3 | 2 | 1 |
| **ВСЬОГО** | **35** | **27** | **8** |

## 🎯 Пріоритет для розширення

### Висока пріоритет (для production)
1. ✅ `POST /submissions/` → Подача рішення
2. ✅ `POST /scores/` → Оцінювання
3. ✅ `GET /leaderboard/by_tournament/` → Показ рейтингу
4. 🔲 `POST /jury-assignments/distribute_tasks/` → Розподіл завдань

### Середня пріоритет (для функціональності)
1. 🔲 `POST /tasks/` → Створення завдань
2. 🔲 `POST /leaderboard/recalculate/` → Пересчет рейтингу
3. 🔲 `GET /scores/{id}/comparison/` → Порівняння оцінок

### Низька пріоритет (nice-to-have)
1. 🔲 `GET /tasks/{id}/statistics/` → Статистика завдання
2. 🔲 `POST /submissions/{id}/lock/` → Блокування подач
3. 🔲 `POST /submissions/{id}/unlock/` → Розблокування подач

## 🔗 Залежності між операціями

```
Користувач
├── Логін → Отримати JWT
└── Виберу роль
    ├── Якщо Team:
    │   ├── Переглянути список турнірів
    │   ├── Переглянути завдання турніру
    │   ├── Подати рішення
    │   └── Переглянути мої подачи
    ├── Якщо Jury:
    │   ├── Переглянути мої призначення
    │   ├── Оцінити подачу
    │   └── Переглянути порівняння оцінок
    └── Якщо Admin:
        ├── Створити турнір
        ├── Створити завдання
        ├── Розподілити завдання журі
        └── Пересчитати лідербордом
```

## 📈 Розвиток

### v1.0 (ПОТОЧНА)
- ✅ Основні операції для team/jury
- ✅ Перегляд турнірів і завдань
- ✅ Подача і оцінювання

### v1.1 (ПЛАНУЄТЬСЯ)
- 🔲 Admin операції (створення, розподіл)
- 🔲 Статистика і звіти
- 🔲 Порівняння оцінок

### v2.0 (МАЙБУТНЬОГО)
- 🔲 Real-time оновлення (WebSocket)
- 🔲 Графіки і діаграми
- 🔲 Export результатів
- 🔲 Mobile app

---

**Версія:** 1.0.0  
**Остання оновлення:** Май 13, 2026  
**Розроблено:** GitHub Copilot (Claude Haiku 4.5)
