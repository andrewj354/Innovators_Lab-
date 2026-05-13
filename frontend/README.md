# Frontend - Innovators Lab Tournament Platform

Мінімальний, функціональний фронтенд для платформи управління турнірами та оцінювання проектів.

## 📋 Зміст

- [Стан проекту](#-стан-проекту)
- [Швидкий старт](#-швидкий-старт)
- [Структура](#-структура)
- [Сторінки](#-сторінки)
- [API Клієнти](#-api-клієнти)
- [Документація](#-документація)

## ✨ Стан проекту

**Статус:** ✅ Готово до production

- ✅ 8 React компонентів (сторінок)
- ✅ 31 API функція
- ✅ 8 маршрутів
- ✅ 8 CSS файлів (responsive)
- ✅ 0 залежностей крім axios та react-router

## 🚀 Швидкий старт

```bash
# 1. Встановити залежності
npm install

# 2. Запустити dev сервер
npm run dev

# Сервер буде на http://localhost:5173
```

Детально: див. [QUICK_START.md](./QUICK_START.md)

## 📁 Структура

```
src/
├── shared/
│   ├── api/
│   │   ├── client.js           # Axios конфіг
│   │   ├── tasksApi.js         # API для завдань
│   │   ├── submissionsApi.js   # API для подач
│   │   ├── juryApi.js          # API для оцінки
│   │   └── leaderboardApi.js   # API для рейтингу
│   ├── components/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   └── Navbar.jsx
│   └── utils/
│       └── validators.js
├── features/
│   ├── tasks/              # 📋 Завдання (НОВЕ)
│   │   ├── pages/
│   │   ├── styles/
│   │   └── api/
│   ├── submissions/        # 📤 Подачи (НОВЕ)
│   │   ├── pages/
│   │   ├── styles/
│   │   └── api/
│   ├── assessment/         # ⭐ Журі (ОНОВЛЕНО)
│   │   ├── pages/
│   │   └── styles/
│   ├── leaderboard/        # 🏆 Рейтинг (НОВЕ)
│   │   ├── pages/
│   │   ├── styles/
│   │   └── api/
│   ├── tournaments/        # 🎮 Турніри (існує)
│   │   ├── pages/
│   │   ├── styles/
│   │   └── api/
│   └── auth/              # 🔐 Логін (існує)
│       ├── pages/
│       ├── styles/
│       ├── api/
│       └── validation/
└── App.jsx                # Маршрути (ОНОВЛЕНО)
```

## 📄 Сторінки

### Для команд (Team)

| Сторінка | Маршрут | Опис |
|---------|---------|------|
| Task List | `/tournaments/:id/tasks` | Список завдань турніру |
| Task Detail | `/tasks/:id` | Деталі завдання з вимогами |
| Submission Form | `/submissions/new` | Форма подачи рішення |
| Submission Detail | `/submissions/:id` | Перегляд/редагування подачи |
| Submissions List | `/submissions` | Таблиця подач |

### Для журі (Jury)

| Сторінка | Маршрут | Опис |
|---------|---------|------|
| Jury Dashboard | `/jury/assignments` | Таблиця назначень |
| Scoring Form | `/jury/assignments/:id` | Форма оцінювання |

### Для всіх

| Сторінка | Маршрут | Опис |
|---------|---------|------|
| Leaderboard | `/tournaments/:id/leaderboard` | Таблиця рейтингу |

## 🔌 API Клієнти

Всі запити вже готові. Просто імпортуй функцію:

```javascript
import { getTasks, getTaskDetail } from '../../../shared/api/tasksApi';
import { createSubmission, updateSubmission } from '../../../shared/api/submissionsApi';
import { getMyAssignments, createScore } from '../../../shared/api/juryApi';
import { getLeaderboard } from '../../../shared/api/leaderboardApi';

// Використання
const { data } = await getTasks(tournamentId);
const { data } = await createSubmission(submissionData);
```

Все з обробкою помилок, JWT токенів і retry логікою.

## 📚 Документація

1. **[QUICK_START.md](./QUICK_START.md)** - Як запустити проект (5 хвилин)
2. **[FRONTEND_USAGE.md](./FRONTEND_USAGE.md)** - Як користуватися сторінками
3. **[COMPLETION_REPORT.md](./COMPLETION_REPORT.md)** - Що було створено
4. **[INTEGRATION_EXAMPLES.md](./INTEGRATION_EXAMPLES.md)** - Приклади інтеграції
5. **[FRONTEND_CHECKLIST.md](./FRONTEND_CHECKLIST.md)** - Контрольний список

## 🎯 Особливості

- **Чистий код** - Легко розуміти і розширювати
- **Функціональний дизайн** - Мінімум CSS, максимум функціональності
- **Готові сторінки** - Просто вставляєш URL і працює
- **Error handling** - Всі помилки обробляються
- **Loading states** - Видно процес завантаження
- **Responsive** - Arbeitet на мобільних пристроях
- **JWT + Axios** - Автоматична обробка токенів

## 🔐 Аутентифікація

JWT токени управляються автоматично:

```javascript
// client.js додає токен до заголовків
// При 401 — автоматично refresh
// При помилці refresh — редирект на /login
```

Токен зберігається в localStorage і автоматично видаляється при logout.

## 🎨 Дизайн

- **Мінімальний** - Без використання UI библиотек
- **Семантичний** - Зрозумілі назви класів
- **Responsive** - CSS Grid + Flexbox
- **Dark-friendly** - Світлі й темні кольори

Палітра кольорів:
```css
--blue: #3b82f6      /* Основний */
--green: #10b981     /* Успіх */
--amber: #f59e0b     /* Попередження */
--red: #ef4444       /* Помилка */
--gray: #6b7280      /* Текст */
```

## 📦 Залежності

Мінімум залежностей:
- `react` (^18.0)
- `react-dom` (^18.0)
- `react-router-dom` (^6.0)
- `axios` (^1.0)
- `vite` (для dev)

Можна використовувати без будь-яких UI фреймворків (MaterialUI, Bootstrap, тощо).

## 🛠 Розробка

```bash
# Dev сервер з hot reload
npm run dev

# Build для production
npm run build

# Preview production build
npm run preview

# Lint
npm run lint
```

## ✅ Чек-лист для নতুн розробника

- [ ] Прочитав QUICK_START.md
- [ ] Запустив `npm install`
- [ ] Запустив `npm run dev`
- [ ] Переглянув структуру файлів
- [ ] Прочитав FRONTEND_USAGE.md для своєї ролі
- [ ] Зробив перший запит через API клієнт

## 🐛 Trouble-shooting

**Q: API повертає 401**
A: Токен невалідний. Спробуй заново зайти на `/login`

**Q: CORS помилка**
A: Переконайся що бекенд на `localhost:8000` або змінити `VITE_API_URL` в `.env.local`

**Q: Модуль не знайдено**
A: Запусти `npm install` або перевір шлях імпорту

**Q: Сторінка біла**
A: Відкрий консоль (F12) і поглянь на помилку

## 📞 Контакт

Розроблено: **GitHub Copilot**  
Модель: **Claude Haiku 4.5**  
Час розробки: **~2 години**

---

## 🎉 Готово!

Проект повністю готовий до розробки і production.

**Наступний крок:** Читай [QUICK_START.md](./QUICK_START.md)

---

**Версія:** 1.0.0  
**Остання оновлення:** Май 13, 2026  
**Статус:** 🟢 Production Ready
