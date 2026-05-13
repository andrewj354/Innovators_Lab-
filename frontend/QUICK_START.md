# 🚀 Швидкий старт Frontend

**Час для старту:** ~5 хвилин

## Кроки для запуску

### 1. Встановити залежності
```bash
cd frontend
npm install
```

### 2. Встановити環境 змінні
Створити `.env.local` у папці `frontend`:
```env
VITE_API_URL=http://localhost:8000/api
```

### 3. Запустити dev сервер
```bash
npm run dev
```

Сервер запуститься на `http://localhost:5173`

## Тестування сторінок

### 1️⃣ Турніри → Завдання → Подача
```
http://localhost:5173/tournaments
  → Click на турнір → /tournaments/:id
  → Click "Завдання" → /tournaments/:id/tasks
  → Click на завдання → /tasks/:taskId
  → Click "Подати рішення" → /submissions/new?task=:taskId
```

### 2️⃣ Журі (вимагає JWT токена для журі)
```
http://localhost:5173/jury/assignments
  → Таблиця всіх назначень
  → Click "Оцінити" → /jury/assignments/:assignmentId
  → Заповнити форму оцінки → Submit
```

### 3️⃣ Лідербордом
```
http://localhost:5173/tournaments/:id/leaderboard
  → Показує топ 3 команди
  → Таблиця всіх команд з оцінками
```

## Тестові маршрути (для разработки без бекенду)

Якщо API недоступна, можна тестувати UI сторінок так:

```bash
# Зайти на прямо на сторінку (навіть без логіну)
http://localhost:5173/submissions/new?task=1
http://localhost:5173/tasks/1
http://localhost:5173/jury/assignments/1
http://localhost:5173/tournaments/1/leaderboard
```

## Структура проекту

```
frontend/
├── src/
│   ├── shared/
│   │   ├── api/           ← Всі API запити сюди
│   │   ├── components/    ← Спільні компоненти
│   │   └── utils/         ← Helper функції
│   ├── features/
│   │   ├── tasks/         ← Завдання (нове)
│   │   ├── submissions/   ← Подачи (нове)
│   │   ├── assessment/    ← Журі (оновлено)
│   │   ├── leaderboard/   ← Рейтинг (нове)
│   │   ├── tournaments/   ← Турніри (існує)
│   │   └── auth/          ← Логіну (існує)
│   └── App.jsx            ← Маршрути (оновлено)
├── package.json
├── vite.config.js
└── README.md
```

## Важні файли для розуміння

1. **API запити:** `src/shared/api/*.js`
   - Тут шаблони для всіх запитів до бекенду

2. **Сторінки:** `src/features/*/pages/*.jsx`
   - Готові до використання компоненти

3. **Маршрути:** `src/App.jsx`
   - Усі маршрути визначені тут

## Типові помилки при розробці

### ❌ `Cannot find module 'axios'`
```bash
npm install axios
```

### ❌ `Cannot find module 'react-router-dom'`
```bash
npm install react-router-dom
```

### ❌ API повертає 401
- JWT токен невалідний або видалено з localStorage
- Необхідно заново зайти (`/login`)

### ❌ CORS помилка
- Переконатися що бекенд запущено на тому ж localhost:8000
- Або змінити `VITE_API_URL` у `.env.local`

## Швидкий debug

### Перевірити токен
```javascript
// У браузерній консолі
console.log(localStorage.getItem('accessToken'));
```

### Перевірити API URL
```javascript
import client from './src/shared/api/client.js';
console.log(client.defaults.baseURL);
```

### Перевірити маршрут
```bash
# Це виведе всі маршрути в консолі
# (якщо додано в App.jsx)
```

## Як додати нову сторінку

### Мінімальний приклад:

1. **Створити компонент:**
```javascript
// src/features/myfeature/pages/MyPage.jsx
import { useState, useEffect } from 'react';
import '../styles/MyPage.css';

export default function MyPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data тут
  }, []);

  return <div className="container">{/* вміст */}</div>;
}
```

2. **Створити стилі:**
```css
/* src/features/myfeature/styles/MyPage.css */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
```

3. **Додати маршрут:**
```javascript
// У App.jsx
import MyPage from './features/myfeature/pages/MyPage';

<Route path="/myfeature/:id" element={<MyPage />} />
```

## Команди для розробки

```bash
# Dev сервер (горячий reload)
npm run dev

# Build для production
npm run build

# Preview production build
npm run preview

# Lint код
npm run lint

# Format код (якщо налаштовано)
npm run format
```

## Тестування з різними даними

### Логіну як команда
```
Email: team@example.com
Password: password123
Role: team
```

### Логіну як журі
```
Email: jury@example.com
Password: password123
Role: jury
```

### Логіну як адміністратор
```
Email: admin@example.com
Password: password123
Role: admin
```

## Документація

- **FRONTEND_USAGE.md** - Детальна інструкція по сторінкам
- **COMPLETION_REPORT.md** - Що було створено
- **INTEGRATION_EXAMPLES.md** - Приклади інтеграції
- **API_DOCUMENTATION.md** (на рівні проекту) - API ендпоїнти

## Контакт / Питання

Якщо виникнуть проблеми:

1. Перевірити консоль браузера (F12 → Console)
2. Перевірити Network tab для помилок API
3. Читати FRONTEND_USAGE.md розділи

---

## Готово!

Ви можете тепер:
- ✅ Переглядати список завдань
- ✅ Переглядати деталі завдання
- ✅ Подавати рішення
- ✅ Оцінювати (як журі)
- ✅ Переглядати рейтинг

**Всё запущено і готово до розробки.**

---

**Версія:** 1.0.0  
**Остання оновлення:** Май 13, 2026  
**Статус:** 🟢 Ready to develop
