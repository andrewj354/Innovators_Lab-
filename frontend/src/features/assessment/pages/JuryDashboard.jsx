import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getMyAssignments, getPendingAssignments } from '../../../shared/api/juryApi';
import '../styles/JuryDashboard.css';

export default function JuryDashboard() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tab, setTab] = useState('pending');

  useEffect(() => {
    const fetchAssignments = async () => {
      try {
        setLoading(true);
        let res;

        if (tab === 'pending') {
          res = await getPendingAssignments();
          setAssignments(res.data.assignments || res.data);
        } else {
          res = await getMyAssignments();
          setAssignments(res.data);
        }

        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load assignments');
      } finally {
        setLoading(false);
      }
    };

    fetchAssignments();
  }, [tab]);

  const evaluatedCount = assignments.filter(a => a.is_evaluated).length;
  const totalCount = assignments.length;

  if (loading) return <div className="jury-dashboard-container"><p>Завантаження...</p></div>;
  if (error) return <div className="jury-dashboard-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;

  return (
    <div className="jury-dashboard-container">
      <div className="dashboard-header">
        <h1>Панель журі</h1>
        <div className="header-stats">
          <div className="stat">
            <span className="stat-label">Оцінено:</span>
            <span className="stat-value">{evaluatedCount}/{totalCount}</span>
          </div>
        </div>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${tab === 'pending' ? 'active' : ''}`}
          onClick={() => setTab('pending')}
        >
          ⏳ Очікують оцінки ({assignments.filter(a => !a.is_evaluated).length})
        </button>
        <button 
          className={`tab ${tab === 'all' ? 'active' : ''}`}
          onClick={() => setTab('all')}
        >
          📋 Всі призначення ({totalCount})
        </button>
      </div>

      {assignments.length === 0 ? (
        <div className="empty-state">
          <p>{tab === 'pending' ? 'Немає невиконаних завдань' : 'Немає призначень'}</p>
        </div>
      ) : (
        <table className="assignments-table">
          <thead>
            <tr>
              <th>Подача</th>
              <th>Завдання</th>
              <th>Команда</th>
              <th>Статус</th>
              <th>Призначено</th>
              <th>Дія</th>
            </tr>
          </thead>
          <tbody>
            {assignments.map(assignment => (
              <tr key={assignment.id} className={assignment.is_evaluated ? 'evaluated' : 'pending'}>
                <td>#{assignment.submission}</td>
                <td>{assignment.submission_info?.task_title || assignment.submission_details?.task_title || 'Завдання'}</td>
                <td>#{assignment.team_id}</td>
                <td>
                  <span className={`badge ${assignment.is_evaluated ? 'evaluated' : 'pending'}`}>
                    {assignment.is_evaluated ? '✓ Оцінено' : '⏳ Очікує'}
                  </span>
                </td>
                <td>{new Date(assignment.assigned_at).toLocaleDateString('uk-UA')}</td>
                <td>
                  <Link 
                    to={`/jury/assignments/${assignment.id}`}
                    className="link-action"
                  >
                    {assignment.is_evaluated ? 'Переглянути' : 'Оцінити'} →
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