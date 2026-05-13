import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getTaskDetail } from '../../../shared/api/tasksApi';
import { createSubmission } from '../../../shared/api/submissionsApi';
import '../styles/SubmissionFormPage.css';

export default function SubmissionFormPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const taskId = searchParams.get('task');

  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    task: taskId ? parseInt(taskId) : null,
    team_id: localStorage.getItem('teamId') || '',
    github_url: '',
    video_url: '',
    live_demo_url: '',
    description: ''
  });

  useEffect(() => {
    if (!taskId) {
      setError('Task ID is required');
      setLoading(false);
      return;
    }

    const fetchTask = async () => {
      try {
        setLoading(true);
        const { data } = await getTaskDetail(parseInt(taskId));
        setTask(data);
        
        if (data.is_deadline_passed) {
          setError('Дедлайн цього завдання пройшов');
        }
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load task');
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.team_id) {
      setError('Будь ласка, укажіть ID команди');
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const submitData = {
        ...formData,
        team_id: parseInt(formData.team_id)
      };

      const { data } = await createSubmission(submitData);
      
      // Save team ID for future submissions
      localStorage.setItem('teamId', formData.team_id);
      
      navigate(`/submissions/${data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to submit');
      console.error('Error submitting:', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="submission-form-container"><p>Завантаження завдання...</p></div>;
  if (error && !task) return <div className="submission-form-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;

  return (
    <div className="submission-form-container">
      <div className="form-header">
        <h1>Подати рішення</h1>
        {task && <p className="task-title">Завдання: {task.title}</p>}
      </div>

      {error && <div className="error-alert">{error}</div>}

      {task && task.is_deadline_passed && (
        <div className="warning-alert">⚠️ Дедлайн цього завдання пройшов</div>
      )}

      <form onSubmit={handleSubmit} className="submission-form">
        <div className="form-group">
          <label htmlFor="team_id">ID команди *</label>
          <input
            type="number"
            id="team_id"
            name="team_id"
            value={formData.team_id}
            onChange={handleChange}
            required
            placeholder="Введіть ID вашої команди"
          />
        </div>

        <div className="form-group">
          <label htmlFor="github_url">GitHub посилання *</label>
          <input
            type="url"
            id="github_url"
            name="github_url"
            value={formData.github_url}
            onChange={handleChange}
            required
            placeholder="https://github.com/team/project"
          />
          <small>Лінк до репозиторію вашого проекту</small>
        </div>

        <div className="form-group">
          <label htmlFor="video_url">Посилання на відео (опціонально)</label>
          <input
            type="url"
            id="video_url"
            name="video_url"
            value={formData.video_url}
            onChange={handleChange}
            placeholder="https://youtube.com/watch?v=..."
          />
          <small>Презентація або демонстрація проекту</small>
        </div>

        <div className="form-group">
          <label htmlFor="live_demo_url">Посилання на live демо (опціонально)</label>
          <input
            type="url"
            id="live_demo_url"
            name="live_demo_url"
            value={formData.live_demo_url}
            onChange={handleChange}
            placeholder="https://yourapp.com"
          />
          <small>Працюючий прототип вашого проекту</small>
        </div>

        <div className="form-group">
          <label htmlFor="description">Опис проекту (опціонально)</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="6"
            placeholder="Розповідьте про ваш підхід, технології, вирішені проблеми..."
          />
          <small>Максимум 2000 символів</small>
        </div>

        {task && (
          <div className="task-requirements">
            <h3>Вимоги до проекту:</h3>
            <ul>
              {task.requirements?.map(req => (
                <li key={req.id}>
                  <span className={req.is_required ? 'badge-required' : 'badge-optional'}>
                    {req.is_required ? '✓ Обов\'язково' : '○ Опціонально'}
                  </span>
                  {req.title}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="form-actions">
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => navigate(-1)}
            disabled={submitting}
          >
            Скасувати
          </button>
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={submitting || (task && task.is_deadline_passed)}
          >
            {submitting ? 'Подання...' : 'Подати'}
          </button>
        </div>
      </form>
    </div>
  );
}
