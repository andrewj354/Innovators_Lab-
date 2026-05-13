import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getTaskDetail, getTaskRequirements } from '../../../shared/api/tasksApi';
import '../styles/TaskDetailPage.css';

export default function TaskDetailPage() {
  const { taskId } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [requirements, setRequirements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!taskId) {
      setError('Task ID is required');
      setLoading(false);
      return;
    }

    const fetchTaskData = async () => {
      try {
        setLoading(true);
        const [taskRes, reqsRes] = await Promise.all([
          getTaskDetail(parseInt(taskId)),
          getTaskRequirements(parseInt(taskId))
        ]);
        setTask(taskRes.data);
        setRequirements(reqsRes.data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load task');
        console.error('Error fetching task:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTaskData();
  }, [taskId]);

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString('uk-UA', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <div className="task-detail-container"><p>Завантаження завдання...</p></div>;
  if (error) return <div className="task-detail-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;
  if (!task) return <div className="task-detail-container"><p>Завдання не знайдено</p></div>;

  return (
    <div className="task-detail-container">
      <div className="task-detail-header">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate(-1)}
        >
          ← Назад
        </button>
        <h1>{task.title}</h1>
        <span className="status-badge">{task.status}</span>
      </div>

      <div className="task-detail-body">
        <section className="section">
          <h2>Опис</h2>
          <p>{task.description}</p>
        </section>

        {task.tech_requirements && Object.keys(task.tech_requirements).length > 0 && (
          <section className="section">
            <h2>Технічні вимоги</h2>
            <div className="tech-requirements">
              {Object.entries(task.tech_requirements).map(([key, value]) => (
                <div key={key} className="requirement-item">
                  <strong>{key}:</strong> {JSON.stringify(value)}
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="section">
          <h2>Терміни</h2>
          <div className="timeline">
            <div className="timeline-item">
              <span className="label">Початок:</span>
              <span className="value">{formatDateTime(task.start_time)}</span>
            </div>
            <div className="timeline-item">
              <span className="label">Дедлайн:</span>
              <span className="value" style={{ color: task.is_deadline_passed ? 'red' : 'green' }}>
                {formatDateTime(task.deadline)}
              </span>
            </div>
            {task.time_remaining && (
              <div className="timeline-item">
                <span className="label">Залишилось:</span>
                <span className="value">{task.time_remaining}</span>
              </div>
            )}
          </div>
        </section>

        {requirements.length > 0 && (
          <section className="section">
            <h2>Вимоги до проекту</h2>
            <ul className="requirements-list">
              {requirements.map(req => (
                <li key={req.id} className={req.is_required ? 'required' : 'optional'}>
                  <span className="badge">{req.is_required ? 'ОБОВ\'ЯЗКОВО' : 'ОПЦІОНАЛЬНО'}</span>
                  {req.title}
                </li>
              ))}
            </ul>
          </section>
        )}

        <section className="section">
          <h2>Статистика</h2>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Статус</span>
              <span className="stat-value">{task.status}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Активне</span>
              <span className="stat-value">{task.is_active ? 'Так' : 'Ні'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Подач</span>
              <span className="stat-value">{task.submissions_count}</span>
            </div>
            {task.requirements_count && (
              <div className="stat-item">
                <span className="stat-label">Вимог</span>
                <span className="stat-value">{task.requirements_count}</span>
              </div>
            )}
          </div>
        </section>

        <section className="section action-section">
          <Link 
            to={`/submissions/new?task=${task.id}`}
            className="btn btn-primary"
          >
            Подати рішення
          </Link>
          <Link 
            to={`/submissions?task=${task.id}`}
            className="btn btn-secondary"
          >
            Переглянути подачи
          </Link>
        </section>
      </div>
    </div>
  );
}
