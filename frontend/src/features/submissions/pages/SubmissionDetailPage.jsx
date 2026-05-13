import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getSubmissionDetail, updateSubmission, lockSubmission, unlockSubmission } from '../../../shared/api/submissionsApi';
import '../styles/SubmissionDetailPage.css';

export default function SubmissionDetailPage() {
  const { submissionId } = useParams();
  const navigate = useNavigate();

  const [submission, setSubmission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [updating, setUpdating] = useState(false);

  const [formData, setFormData] = useState({
    github_url: '',
    video_url: '',
    live_demo_url: '',
    description: ''
  });

  useEffect(() => {
    if (!submissionId) {
      setError('Submission ID is required');
      setLoading(false);
      return;
    }

    const fetchSubmission = async () => {
      try {
        setLoading(true);
        const { data } = await getSubmissionDetail(parseInt(submissionId));
        setSubmission(data);
        setFormData({
          github_url: data.github_url || '',
          video_url: data.video_url || '',
          live_demo_url: data.live_demo_url || '',
          description: data.description || ''
        });
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load submission');
      } finally {
        setLoading(false);
      }
    };

    fetchSubmission();
  }, [submissionId]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async (e) => {
    e.preventDefault();

    try {
      setUpdating(true);
      setError(null);

      const { data } = await updateSubmission(submission.id, formData);
      setSubmission(data);
      setIsEditing(false);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to update submission');
    } finally {
      setUpdating(false);
    }
  };

  const handleLock = async () => {
    try {
      await lockSubmission(submission.id);
      setSubmission(prev => ({ ...prev, is_locked: true }));
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUnlock = async () => {
    try {
      await unlockSubmission(submission.id);
      setSubmission(prev => ({ ...prev, is_locked: false }));
    } catch (err) {
      setError(err.message);
    }
  };

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString('uk-UA', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <div className="submission-detail-container"><p>Завантаження подачи...</p></div>;
  if (error && !submission) return <div className="submission-detail-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;
  if (!submission) return <div className="submission-detail-container"><p>Подачу не знайдено</p></div>;

  return (
    <div className="submission-detail-container">
      <div className="detail-header">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate(-1)}
        >
          ← Назад
        </button>
        <div className="header-info">
          <h1>Подача #{submission.id}</h1>
          {submission.is_locked && <span className="locked-badge">🔒 Заблокована</span>}
        </div>
      </div>

      {error && <div className="error-alert">{error}</div>}

      <div className="detail-body">
        <section className="section">
          <h2>Інформація про задачу</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Завдання:</span>
              <span className="value">{submission.task_details?.title}</span>
            </div>
            <div className="info-item">
              <span className="label">Команда:</span>
              <span className="value">#{submission.team_id}</span>
            </div>
            <div className="info-item">
              <span className="label">Подано:</span>
              <span className="value">{formatDateTime(submission.submitted_at)}</span>
            </div>
            <div className="info-item">
              <span className="label">Оновлено:</span>
              <span className="value">{formatDateTime(submission.updated_at)}</span>
            </div>
          </div>
        </section>

        {!isEditing ? (
          <section className="section">
            <div className="section-header">
              <h2>Посилання та опис</h2>
              {submission.can_edit && !submission.is_locked && (
                <button 
                  className="btn btn-secondary btn-small"
                  onClick={() => setIsEditing(true)}
                >
                  ✏️ Редагувати
                </button>
              )}
            </div>

            <div className="links-grid">
              <div className="link-item">
                <span className="link-label">GitHub:</span>
                {submission.github_url ? (
                  <a href={submission.github_url} target="_blank" rel="noopener noreferrer" className="link">
                    Перейти до репозиторію →
                  </a>
                ) : (
                  <span className="empty">Не вказано</span>
                )}
              </div>

              {submission.video_url && (
                <div className="link-item">
                  <span className="link-label">Відео:</span>
                  <a href={submission.video_url} target="_blank" rel="noopener noreferrer" className="link">
                    Переглянути відео →
                  </a>
                </div>
              )}

              {submission.live_demo_url && (
                <div className="link-item">
                  <span className="link-label">Live Демо:</span>
                  <a href={submission.live_demo_url} target="_blank" rel="noopener noreferrer" className="link">
                    Отворити демо →
                  </a>
                </div>
              )}
            </div>

            {submission.description && (
              <div className="description-box">
                <h3>Опис проекту:</h3>
                <p>{submission.description}</p>
              </div>
            )}
          </section>
        ) : (
          <form onSubmit={handleSave} className="edit-form">
            <div className="form-group">
              <label htmlFor="github_url">GitHub посилання</label>
              <input
                type="url"
                id="github_url"
                name="github_url"
                value={formData.github_url}
                onChange={handleChange}
                placeholder="https://github.com/..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="video_url">Посилання на відео</label>
              <input
                type="url"
                id="video_url"
                name="video_url"
                value={formData.video_url}
                onChange={handleChange}
                placeholder="https://youtube.com/..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="live_demo_url">Посилання на live демо</label>
              <input
                type="url"
                id="live_demo_url"
                name="live_demo_url"
                value={formData.live_demo_url}
                onChange={handleChange}
                placeholder="https://..."
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Опис проекту</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                rows="6"
                placeholder="Опис проекту..."
              />
            </div>

            <div className="form-actions">
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => setIsEditing(false)}
                disabled={updating}
              >
                Скасувати
              </button>
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={updating}
              >
                {updating ? 'Зберігання...' : 'Зберегти'}
              </button>
            </div>
          </form>
        )}

        {submission.task_details?.requirements && submission.task_details.requirements.length > 0 && (
          <section className="section">
            <h2>Вимоги до проекту</h2>
            <ul className="requirements-list">
              {submission.task_details.requirements.map(req => (
                <li key={req.id} className={req.is_required ? 'required' : 'optional'}>
                  <span className="badge">{req.is_required ? 'ОБОВ\'ЯЗКОВО' : 'ОПЦІОНАЛЬНО'}</span>
                  {req.title}
                </li>
              ))}
            </ul>
          </section>
        )}

        {submission.is_locked && (
          <div className="status-info locked">
            🔒 Ця подача заблокована адміністратором і не може бути змінена
          </div>
        )}

        {!submission.can_edit && !submission.is_locked && (
          <div className="status-info deadline-passed">
            ⚠️ Дедлайн цього завдання пройшов. Редагування більше не можливо.
          </div>
        )}
      </div>
    </div>
  );
}
