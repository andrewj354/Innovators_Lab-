# Приклади інтеграції

Цей файл показує як інтегрувати фронтенд сторінки в існуючий код.

## 1. Логіка навігації в TournamentPublicPage

```javascript
// src/features/tournaments/pages/TournamentPublicPage.jsx

import { useParams, useNavigate } from 'react-router-dom';

export default function TournamentPublicPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const handleViewTasks = () => {
    // Перейти до списку завдань турніру
    navigate(`/tournaments/${id}/tasks`);
  };

  const handleViewLeaderboard = () => {
    // Перейти до лідербордом
    navigate(`/tournaments/${id}/leaderboard`);
  };

  return (
    <div>
      <h1>Турнір #{id}</h1>
      <button onClick={handleViewTasks}>📋 Переглянути завдання</button>
      <button onClick={handleViewLeaderboard}>🏆 Лідербордом</button>
    </div>
  );
}
```

## 2. Логіка в TaskListPage для переходу до деталей

```javascript
// Вже реалізовано в TaskListPage.jsx
// Коли користувач клікає на карту завдання, він переходить на:
// /tasks/:taskId

// Можна також вставити посилання в інші місця:
import { Link } from 'react-router-dom';

<Link to={`/tasks/${task.id}`} className="task-link">
  {task.title}
</Link>
```

## 3. Логіка для команди в Navbar

```javascript
// src/shared/components/Navbar.jsx

import { Link } from 'react-router-dom';

export default function Navbar({ user }) {
  if (user?.role === 'team') {
    return (
      <nav>
        <Link to="/tournaments">Турніри</Link>
        <Link to="/submissions">Мої подачи</Link>
      </nav>
    );
  }

  if (user?.role === 'jury') {
    return (
      <nav>
        <Link to="/jury/assignments">Мої оцінки</Link>
      </nav>
    );
  }

  return null;
}
```

## 4. Контекст для управління користувачем

```javascript
// src/shared/context/AuthContext.jsx

import { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const { data } = await authApi.getMe();
        setUser(data);
      } catch (err) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// Використання в компонентах:
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export default function MyComponent() {
  const { user } = useContext(AuthContext);
  
  return <div>Привіт, {user?.name}</div>;
}
```

## 5. Protected Route для журі

```javascript
// src/shared/components/ProtectedRoute.jsx

import { Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export function ProtectedRoute({ component: Component, requiredRole }) {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <div>Завантаження...</div>;

  if (!user) return <Navigate to="/login" />;

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" />;
  }

  return <Component />;
}

// Використання в App.jsx:
<Route 
  path="/jury/assignments" 
  element={<ProtectedRoute component={JuryDashboard} requiredRole="jury" />} 
/>
```

## 6. Інтеграція з формою створення завдання (Admin)

```javascript
// src/features/tasks/pages/TaskFormPage.jsx (нова сторінка)

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createTask } from '../../../shared/api/tasksApi';

export default function TaskFormPage() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    tournament_id: '',
    title: '',
    description: '',
    deadline: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const { data } = await createTask(formData);
      navigate(`/tasks/${data.id}`);
    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        placeholder="Назва завдання"
        value={formData.title}
        onChange={(e) => setFormData({...formData, title: e.target.value})}
      />
      <textarea 
        placeholder="Опис"
        value={formData.description}
        onChange={(e) => setFormData({...formData, description: e.target.value})}
      />
      <input 
        type="datetime-local"
        value={formData.deadline}
        onChange={(e) => setFormData({...formData, deadline: e.target.value})}
      />
      <button type="submit">Створити завдання</button>
    </form>
  );
}
```

## 7. Hook для отримання даних подачи

```javascript
// src/shared/hooks/useSubmission.js

import { useState, useEffect } from 'react';
import { getSubmissionDetail } from '../api/submissionsApi';

export function useSubmission(submissionId) {
  const [submission, setSubmission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const { data } = await getSubmissionDetail(submissionId);
        setSubmission(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetch();
  }, [submissionId]);

  return { submission, loading, error };
}

// Використання:
export default function MyPage({ submissionId }) {
  const { submission, loading, error } = useSubmission(submissionId);
  
  if (loading) return <div>Завантаження...</div>;
  if (error) return <div>Помилка: {error}</div>;
  
  return <div>{submission?.title}</div>;
}
```

## 8. Мок-дані для тестування (якщо API недоступна)

```javascript
// src/shared/api/mockData.js

export const mockTasks = [
  {
    id: 1,
    tournament_id: 1,
    title: 'Побудова REST API',
    deadline: '2026-05-20T18:00:00Z',
    status: 'published',
    is_active: true,
    time_remaining: '2d 5h',
    requirements_count: 3,
    submissions_count: 5
  }
];

export const mockSubmission = {
  id: 1,
  task: 1,
  team_id: 10,
  github_url: 'https://github.com/team/project',
  is_locked: false,
  can_edit: true,
  submitted_at: '2026-05-18T15:30:00Z'
};

// Потім у API клієнтах:
export const getTasks = async (tournamentId) => {
  // return client.get(`/tasks/?tournament_id=${tournamentId}`);
  return Promise.resolve({ data: mockTasks });
};
```

## 9. Testing в компонентах

```javascript
// src/features/tasks/__tests__/TaskDetailPage.test.jsx

import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import TaskDetailPage from '../pages/TaskDetailPage';

// Mock API
jest.mock('../../../shared/api/tasksApi');

describe('TaskDetailPage', () => {
  it('показує назву завдання', () => {
    render(
      <BrowserRouter>
        <TaskDetailPage />
      </BrowserRouter>
    );

    expect(screen.getByText(/завдання/i)).toBeInTheDocument();
  });
});
```

## 10. Розширення: Додати фільтр до SubmissionsListPage

```javascript
// Вже реалізовано в SubmissionsListPage.jsx
// Але можна розширити на сортування:

const [sort, setSort] = useState('-submitted_at'); // нові спочатку

const fetchSubmissions = async () => {
  const { data } = await getSubmissions(taskId, null, null, sort);
  setSubmissions(data.results);
};

// Додати кнопки сортування:
<button onClick={() => setSort('-submitted_at')}>Нові спочатку</button>
<button onClick={() => setSort('submitted_at')}>Старі спочатку</button>
```

---

## Корисні посилання

- [React Router Docs](https://reactrouter.com/)
- [React Hooks Docs](https://react.dev/reference/react)
- [Axios Docs](https://axios-http.com/)
- API Documentation: `/API_DOCUMENTATION.md`
- Frontend Usage: `/FRONTEND_USAGE.md`

---

**Версія:** 1.0.0  
**Остання оновлення:** Май 13, 2026
