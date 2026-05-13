import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getLeaderboard } from '../../../shared/api/leaderboardApi';
import '../styles/LeaderboardPage.css';

export default function LeaderboardPage() {
  const { tournamentId } = useParams();
  const navigate = useNavigate();

  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!tournamentId) {
      setError('Tournament ID is required');
      setLoading(false);
      return;
    }

    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        const { data } = await getLeaderboard(parseInt(tournamentId));
        setLeaderboard(data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to load leaderboard');
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, [tournamentId]);

  const getMedalEmoji = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  const getScoreColor = (score) => {
    if (score >= 90) return '#10b981'; // green
    if (score >= 80) return '#3b82f6'; // blue
    if (score >= 70) return '#f59e0b'; // amber
    return '#ef4444'; // red
  };

  if (loading) return <div className="leaderboard-container"><p>Завантаження лідербордом...</p></div>;
  if (error) return <div className="leaderboard-container"><p style={{ color: 'red' }}>Помилка: {error}</p></div>;

  return (
    <div className="leaderboard-container">
      <div className="leaderboard-header">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate(-1)}
        >
          ← Назад
        </button>
        <h1>Лідербордом</h1>
      </div>

      {leaderboard.length === 0 ? (
        <div className="empty-state">
          <p>Немає результатів</p>
        </div>
      ) : (
        <div className="leaderboard-content">
          <div className="top-3">
            {leaderboard.slice(0, 3).map((entry, idx) => (
              <div key={entry.rank} className={`podium-place place-${idx + 1}`}>
                <div className="medal">{getMedalEmoji(entry.rank)}</div>
                <div className="team-id">Команда #{entry.team_id}</div>
                <div className="score" style={{ color: getScoreColor(entry.total_score) }}>
                  {entry.total_score.toFixed(1)}
                </div>
              </div>
            ))}
          </div>

          <table className="leaderboard-table">
            <thead>
              <tr>
                <th className="rank-col">Місце</th>
                <th className="team-col">Команда</th>
                <th className="score-col">Оцінка</th>
                <th className="date-col">Розраховано</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry) => (
                <tr key={entry.rank} className={`rank-${entry.rank}`}>
                  <td className="rank-col">
                    <span className="medal-badge">{getMedalEmoji(entry.rank)}</span>
                  </td>
                  <td className="team-col">
                    <strong>Команда #{entry.team_id}</strong>
                  </td>
                  <td className="score-col">
                    <div className="score-bar">
                      <div 
                        className="score-fill" 
                        style={{ 
                          width: `${(entry.total_score / 100) * 100}%`,
                          backgroundColor: getScoreColor(entry.total_score)
                        }}
                      />
                      <span className="score-text">{entry.total_score.toFixed(1)}/100</span>
                    </div>
                  </td>
                  <td className="date-col">
                    {new Date(entry.calculated_at).toLocaleDateString('uk-UA', {
                      day: '2-digit',
                      month: '2-digit',
                      year: 'numeric'
                    })}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
