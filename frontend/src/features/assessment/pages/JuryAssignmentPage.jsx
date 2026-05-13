import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getAssignmentDetail, markAssignmentAsEvaluated } from '../../../shared/api/juryApi';
import { createScore, updateScore } from '../../../shared/api/juryApi';
import './JuryAssignmentPage.css';

export default function JuryAssignmentPage() {
  const { assignmentId } = useParams();
  const navigate = useNavigate();

  const [assignment, setAssignment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const [scores, setScores] = useState({
    backend_code: 0,
    database: 0,
    frontend_code: 0,
    functionality: 0,
    usability: 0,
    comment: ''
  });

  useEffect(() => {
    if (!assignmentId) {
      setError('Assignment ID is required');
      setLoading(false);
      return;
    }

    const fetchAssignment = async () => {
      try {
        setLoading(true);
        const { data } = await getAssignmentDetail(parseInt(assignmentId));
        setAssignment(data);

        if (data.score) {
          setScores({
            backend_code: data.score.backend_code,
            database: data.score.database,
            frontend_code: data.score.frontend_code,
            functionality: data.score.functionality,
            usability: data.score.usability,
            comment: data.score.comment
          });
        }

        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load assignment');
      } finally {
        setLoading(false);
      }
    };

    fetchAssignment();
  }, [assignmentId]);

  const handleScoreChange = (field, value) => {
    const numValue = Math.max(0, Math.min(100, parseInt(value) || 0));
    setScores(prev => ({
      ...prev,
      [field]: numValue
    }));
  };

  const calculateAverage = () => {
    const values = [
      scores.backend_code,
      scores.database,
      scores.frontend_code,
      scores.functionality,
      scores.usability
    ];
    return (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1);
  };

  const handleSubmitScore = async (e) => {
    e.preventDefault();

    try {
      setSubmitting(true);
      setError(null);

      const scoreData = {
        assignment: assignmentId,
        ...scores
      };

      if (assignment.score) {
        await updateScore(assignment.score.id, scoreData);
      } else {
        await createScore(scoreData);
      }

      await markAssignmentAsEvaluated(assignmentId);
      navigate('/jury/assignments');
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to submit score');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="jury-assignment-container"><p>Завантаження завдання...</p></div>;
  if (error && !assignment) return <div className="jury-assignment-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;
  if (!assignment) return <div className="jury-assignment-container"><p>Завдання не знайдено</p></div>;

  const submissionInfo = assignment.submission_details || assignment.submission_info;

  return (
    <div className="jury-assignment-container">
      <div className="assignment-header">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate(-1)}
        >
          ← Назад
        </button>
        <h1>Оцінка подачи #{assignment.submission}</h1>
      </div>

      {error && <div className="error-alert">{error}</div>}

      <div className="assignment-body">
        <section className="section">
          <h2>Інформація про проект</h2>
          <div className="info-grid">
            <div className="info-item">
              <span className="label">Завдання:</span>
              <span className="value">{submissionInfo?.task_title || assignment.submission_details?.task_title}</span>
            </div>
            <div className="info-item">
              <span className="label">Команда:</span>
              <span className="value">#{assignment.team_id}</span>
            </div>
            <div className="info-item">
              <span className="label">Статус:</span>
              <span className="value">{assignment.is_evaluated ? '✓ Оцінено' : '⏳ Очікує оцінки'}</span>
            </div>
          </div>

          <div className="links-grid">
            {submissionInfo?.github_url && (
              <a href={submissionInfo.github_url} target="_blank" rel="noopener noreferrer" className="link-btn">
                📦 Переглянути GitHub
              </a>
            )}
            {submissionInfo?.video_url && (
              <a href={submissionInfo.video_url} target="_blank" rel="noopener noreferrer" className="link-btn">
                📹 Переглянути відео
              </a>
            )}
            {submissionInfo?.live_demo_url && (
              <a href={submissionInfo.live_demo_url} target="_blank" rel="noopener noreferrer" className="link-btn">
                🌐 Переглянути демо
              </a>
            )}
          </div>
        </section>

        {submissionInfo?.task_description && (
          <section className="section">
            <h2>Опис завдання</h2>
            <p>{submissionInfo.task_description}</p>
          </section>
        )}

        {submissionInfo?.requirements && submissionInfo.requirements.length > 0 && (
          <section className="section">
            <h2>Вимоги</h2>
            <ul className="requirements-list">
              {submissionInfo.requirements.map(req => (
                <li key={req.id} className={req.is_required ? 'required' : 'optional'}>
                  <span className="badge">{req.is_required ? 'ОБОВ\'ЯЗКОВО' : 'ОПЦІОНАЛЬНО'}</span>
                  {req.title}
                </li>
              ))}
            </ul>
          </section>
        )}

        <form onSubmit={handleSubmitScore} className="scoring-form">
          <section className="section">
            <h2>Критерії оцінювання</h2>

            <div className="score-grid">
              <div className="score-item">
                <label htmlFor="backend_code">Backend код</label>
                <div className="score-input-group">
                  <input
                    type="range"
                    id="backend_code"
                    min="0"
                    max="100"
                    value={scores.backend_code}
                    onChange={(e) => handleScoreChange('backend_code', e.target.value)}
                    className="score-slider"
                  />
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={scores.backend_code}
                    onChange={(e) => handleScoreChange('backend_code', e.target.value)}
                    className="score-number"
                  />
                  <span className="score-unit">/100</span>
                </div>
              </div>

              <div className="score-item">
                <label htmlFor="database">База даних</label>
                <div className="score-input-group">
                  <input
                    type="range"
                    id="database"
                    min="0"
                    max="100"
                    value={scores.database}
                    onChange={(e) => handleScoreChange('database', e.target.value)}
                    className="score-slider"
                  />
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={scores.database}
                    onChange={(e) => handleScoreChange('database', e.target.value)}
                    className="score-number"
                  />
                  <span className="score-unit">/100</span>
                </div>
              </div>

              <div className="score-item">
                <label htmlFor="frontend_code">Frontend код</label>
                <div className="score-input-group">
                  <input
                    type="range"
                    id="frontend_code"
                    min="0"
                    max="100"
                    value={scores.frontend_code}
                    onChange={(e) => handleScoreChange('frontend_code', e.target.value)}
                    className="score-slider"
                  />
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={scores.frontend_code}
                    onChange={(e) => handleScoreChange('frontend_code', e.target.value)}
                    className="score-number"
                  />
                  <span className="score-unit">/100</span>
                </div>
              </div>

              <div className="score-item">
                <label htmlFor="functionality">Функціональність</label>
                <div className="score-input-group">
                  <input
                    type="range"
                    id="functionality"
                    min="0"
                    max="100"
                    value={scores.functionality}
                    onChange={(e) => handleScoreChange('functionality', e.target.value)}
                    className="score-slider"
                  />
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={scores.functionality}
                    onChange={(e) => handleScoreChange('functionality', e.target.value)}
                    className="score-number"
                  />
                  <span className="score-unit">/100</span>
                </div>
              </div>

              <div className="score-item">
                <label htmlFor="usability">Юзабіліті</label>
                <div className="score-input-group">
                  <input
                    type="range"
                    id="usability"
                    min="0"
                    max="100"
                    value={scores.usability}
                    onChange={(e) => handleScoreChange('usability', e.target.value)}
                    className="score-slider"
                  />
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={scores.usability}
                    onChange={(e) => handleScoreChange('usability', e.target.value)}
                    className="score-number"
                  />
                  <span className="score-unit">/100</span>
                </div>
              </div>
            </div>

            <div className="average-score">
              <span className="label">Середня оцінка:</span>
              <span className="value">{calculateAverage()}/100</span>
            </div>
          </section>

          <section className="section">
            <h2>Коментар</h2>
            <textarea
              value={scores.comment}
              onChange={(e) => setScores(prev => ({ ...prev, comment: e.target.value }))}
              rows="6"
              placeholder="Залиште коментар про роботу..."
              className="comment-textarea"
            />
          </section>

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
              disabled={submitting}
            >
              {submitting ? 'Збереження...' : 'Подати оцінку'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
