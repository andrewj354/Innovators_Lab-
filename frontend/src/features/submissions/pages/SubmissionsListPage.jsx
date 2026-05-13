import { useEffect, useState } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import { getSubmissions, getTeamSubmissions } from '../../../shared/api/submissionsApi';
import '../styles/SubmissionsListPage.css';

export default function SubmissionsListPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const taskId = searchParams.get('task');
  const teamId = searchParams.get('team');

  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        setLoading(true);
        let res;

        if (teamId) {
          res = await getTeamSubmissions(parseInt(teamId));
        } else if (taskId) {
          res = await getSubmissions(parseInt(taskId));
        } else {
          setError('Task ID або Team ID повинні бути вказані');
          setLoading(false);
          return;
        }

        setSubmissions(res.data.results || res.data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load submissions');
      } finally {
        setLoading(false);
      }
    };

    fetchSubmissions();
  }, [taskId, teamId]);

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString('uk-UA', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) return <div className="submissions-list-container"><p>Завантаження подач...</p></div>;
  if (error) return <div className="submissions-list-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;

  return (
    <div className="submissions-list-container">
      <div className="list-header">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate(-1)}
        >
          ← Назад
        </button>
        <h1>Подачи</h1>
        <Link to="/submissions/new" className="btn btn-primary">
          + Нова подача
        </Link>
      </div>

      {submissions.length === 0 ? (
        <div className="empty-state">
          <p>Немає подач</p>
          <Link to="/submissions/new" className="btn btn-primary">
            Подати рішення
          </Link>
        </div>
      ) : (
        <table className="submissions-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Завдання</th>
              <th>Команда</th>
              <th>Статус</th>
              <th>Подано</th>
              <th>Дія</th>
            </tr>
          </thead>
          <tbody>
            {submissions.map(submission => (
              <tr key={submission.id}>
                <td>#{submission.id}</td>
                <td>{submission.task_title}</td>
                <td>#{submission.team_id}</td>
                <td>
                  <span className={`badge ${submission.is_locked ? 'locked' : 'active'}`}>
                    {submission.is_locked ? '🔒 Заблокована' : '✓ Активна'}
                  </span>
                </td>
                <td>{formatDateTime(submission.submitted_at)}</td>
                <td>
                  <Link 
                    to={`/submissions/${submission.id}`}
                    className="link-action"
                  >
                    Переглянути →
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
