import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getTasks } from '../../../shared/api/tasksApi';
import '../styles/TaskListPage.css';

export default function TaskListPage() {
  const { tournamentId } = useParams();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('published');

  useEffect(() => {
    if (!tournamentId) {
      setError('Tournament ID is required');
      setLoading(false);
      return;
    }

    const fetchTasks = async () => {
      try {
        setLoading(true);
        const { data } = await getTasks(parseInt(tournamentId), filter);
        setTasks(data.results || data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [tournamentId, filter]);

  const getStatusColor = (status) => {
    const colors = {
      draft: '#fbbf24',
      published: '#10b981',
      closed: '#ef4444'
    };
    return colors[status] || '#6b7280';
  };

  const formatDeadline = (deadline) => {
    return new Date(deadline).toLocaleString('uk-UA', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <div className="task-list-container"><p>Завантаження завдань...</p></div>;
  if (error) return <div className="task-list-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;

  return (
    <div className="task-list-container">
      <div className="task-list-header">
        <h1>Завдання турніру</h1>
        <button 
          className="btn btn-secondary"
          onClick={() => navigate(`/tournaments/${tournamentId}`)}
        >
          ← Назад до турніру
        </button>
      </div>

      <div className="filters">
        <label>Фільтр за статусом:</label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="">Усі</option>
          <option value="draft">Чернетка</option>
          <option value="published">Опубліковане</option>
          <option value="closed">Закрите</option>
        </select>
      </div>

      {tasks.length === 0 ? (
        <p className="empty-state">Немає завдань</p>
      ) : (
        <div className="task-list">
          {tasks.map(task => (
            <Link 
              key={task.id} 
              to={`/tasks/${task.id}`}
              className="task-card"
            >
              <div className="task-card-header">
                <h3>{task.title}</h3>
                <span 
                  className="status-badge"
                  style={{ backgroundColor: getStatusColor(task.status) }}
                >
                  {task.status}
                </span>
              </div>
              <div className="task-card-body">
                <p className="deadline">
                  📅 Дедлайн: {formatDeadline(task.deadline)}
                </p>
                <p className="time-remaining">
                  ⏱️ {task.time_remaining || 'Час закінчився'}
                </p>
                {task.requirements_count && (
                  <p className="requirements">
                    📋 Вимог: {task.requirements_count}
                  </p>
                )}
                {task.submissions_count !== undefined && (
                  <p className="submissions">
                    📤 Подач: {task.submissions_count}
                  </p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
