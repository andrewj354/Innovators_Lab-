# Инструкция по использованию Frontend

## Сторонки для команд (Team)

### 1. Список завдань турніру
**Шлях:** `/tournaments/:tournamentId/tasks`
**Компонент:** `TaskListPage.jsx`

```javascript
// Переход со сторони турніру
navigate(`/tournaments/${tournamentId}/tasks`)
```

Показує:
- Список всіх завдань турніру
- Фільтрацію за статусом
- Дедлайн і час що залишився
- Ссилку на деталі завдання

---

### 2. Деталі завдання
**Шлях:** `/tasks/:taskId`
**Компонент:** `TaskDetailPage.jsx`

Показує:
- Опис завдання
- Технічні вимоги
- Терміни початку/дедлайну
- Обов'язкові вимоги (вимоги проекту)
- Кнопки для подачи рішення

---

### 3. Подача рішення (форма)
**Шлях:** `/submissions/new?task=<taskId>`
**Компонент:** `SubmissionFormPage.jsx`

Форма для введення:
- ID команди (обов'язково)
- GitHub посилання (обов'язково)
- Посилання на відео (опціонально)
- Посилання на live демо (опціонально)
- Опис проекту (опціонально)

```javascript
// Перейти на форму подачи
navigate(`/submissions/new?task=${taskId}`)
```

Автоматично:
- Зберігає ID команди у localStorage
- При успіху перенаправляє на деталі подачи

---

### 4. Деталі подачи (перегляд/редагування)
**Шлях:** `/submissions/:submissionId`
**Компонент:** `SubmissionDetailPage.jsx`

Показує:
- Інформацію про завдання і команду
- Посилання (GitHub, відео, демо)
- Вимоги проекту
- Опцію редагування (якщо дедлайн не пройшов)
- Статус блокування

Функціонал:
- Редагування подачи до дедлайну
- Блокування (для адміністраторів)

---

### 5. Список подач команди
**Шлях:** `/submissions?team=<teamId>`
**Компонент:** `SubmissionsListPage.jsx`

Таблиця з:
- ID подачи
- Завдання
- ID команди
- Статус
- Дата подачи
- Ссилку на деталі

---

## Сторонки для журі (Jury)

### 1. Панель журі
**Шлях:** `/jury/assignments`
**Компонент:** `JuryDashboard.jsx`

Показує:
- Таблицю назначений подач
- Статистика (оцінено/всього)
- Таби для фільтрації (очікують/всі)
- Статус кожного завдання

---

### 2. Оцінка подачи
**Шлях:** `/jury/assignments/:assignmentId`
**Компонент:** `JuryAssignmentPage.jsx`

Форма для оцінювання з критеріями:
- Backend код (0-100)
- База даних (0-100)
- Frontend код (0-100)
- Функціональність (0-100)
- Юзабіліті (0-100)
- Коментар (текст)

Особливості:
- Слайдери і числові поля для оцінок
- Автоматичний розрахунок середньої оцінки
- Ссилки на GitHub, відео, демо подачи
- При сохраненні позначає завдання як оцінене

---

## Сторонки для спостерігачів

### Лідербордом турніру
**Шлях:** `/tournaments/:tournamentId/leaderboard`
**Компонент:** `LeaderboardPage.jsx`

Показує:
- Топ 3 команди (з емодзі медалей)
- Таблицю всіх команд з оцінками
- Візуальну шкалу оцінок
- Дату розрахунку

---

## Як додати нову сторінку

1. **Створити сторінку в папці features**
```
/src/features/feature-name/pages/FeaturePage.jsx
/src/features/feature-name/styles/FeaturePage.css
```

2. **Додати API клієнт (якщо потрібно)**
```
/src/shared/api/featureApi.js
```

3. **Додати маршрут в App.jsx**
```javascript
import FeaturePage from './features/feature-name/pages/FeaturePage';

// У Routes
<Route path="/feature/:id" element={<FeaturePage />} />
```

4. **Структура компонента:**
```javascript
import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getFeatureData } from '../../../shared/api/featureApi';
import '../styles/FeaturePage.css';

export default function FeaturePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const { data } = await getFeatureData(id);
        setData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading) return <div>Завантаження...</div>;
  if (error) return <div>Помилка: {error}</div>;

  return <div className="page-container">{/* вміст */}</div>;
}
```

---

## API клієнти

Всі API клієнти розташовані в `/src/shared/api/` або `/src/features/*/api/`

### Використання:
```javascript
import { getTasks, getTaskDetail } from '../../../shared/api/tasksApi';

// Get запит
const { data } = await getTasks(tournamentId, status);

// Post запит
const { data } = await createSubmission(submissionData);

// Put запит
const { data } = await updateSubmission(id, updateData);
```

### Обработка помилок:
```javascript
try {
  const { data } = await getSubmissionDetail(id);
} catch (err) {
  const errorMessage = err.response?.data?.detail || err.message;
  setError(errorMessage);
}
```

---

## Локальне сховище (localStorage)

Для деяких даних використовується localStorage:

- `accessToken` - JWT токен (управління в client.js)
- `teamId` - ID команди користувача (зберігається при подачи)

```javascript
// Прочитати
const teamId = localStorage.getItem('teamId');

// Записати
localStorage.setItem('teamId', '10');

// Видалити
localStorage.removeItem('accessToken');
```

---

## CSS архітектура

Всі сторінки мають мінімальний, функціональний дизайн без залежностей від UI-фреймворків.

Змінні кольорів:
- Основний: `#3b82f6` (синій)
- Успіх: `#10b981` (зелений)
- Попередження: `#f59e0b` (помаранчевий)
- Помилка: `#ef4444` (червоний)

### Класи утилітарні:
```css
.section { /* Контейнер секції */ }
.error-alert { /* Повідомлення про помилку */ }
.empty-state { /* Порожній стан */ }
.badge { /* Лейбл статусу */ }
.btn { /* Кнопка */ }
```

---

## Рекомендації

1. **Для адміністраторів:** Додати сторінки для:
   - Створення турнірів
   - Розподілу завдань журі
   - Управління користувачами
   
2. **Для команд:** Додати:
   - Сторінку профілю команди
   - Історію подач
   
3. **Для журі:** Додати:
   - Порівняння оцінок для однієї подачи
   - Статистику оцінювання

---

**Версія:** 1.0.0  
**Остання оновлення:** Май 2026
