import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../styles/TournamentListPage.css';
import Button from '../../../shared/components/Button';
import { getTournaments } from '../api/tournamentApi';
import Navbar from '../../../shared/components/Navbar';
import { useAuth } from '../../../shared/context/AuthContext';

export default function TournamentListPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [tournaments, setTournaments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchTournaments();
  }, []);

  const fetchTournaments = async () => {
    try {
      setLoading(true);
      const response = await getTournaments();
      // API returns paginated response: {count, next, previous, results: [...]}
      const tournamentData = response.data?.results || response.results || response.data || [];
      setTournaments(Array.isArray(tournamentData) ? tournamentData : []);
    } catch (err) {
      setError(err.message);
      toast.error('Не вдалось завантажити турніри');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const getStatusBadgeColor = (status) => {
    const statusMap = {
      'draft': 'badge-draft',
      'registration': 'badge-registration',
      'running': 'badge-running',
      'finished': 'badge-finished'
    };
    return statusMap[status] || 'badge-draft';
  };

  const filteredTournaments = tournaments.filter(t => {
    const matchesFilter = activeFilter === 'all' || t.status === activeFilter;
    const matchesSearch = t.title.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const filters = [
    { value: 'all', label: 'Всі Турніри' },
    { value: 'registration', label: 'Реєстрація' },
    { value: 'running', label: 'Проводяться' },
    { value: 'finished', label: 'Завершені' }
  ];

  return (
    <div className="page-wrapper">
      <Navbar user={user} onLogout={handleLogout} />

      <main className="page-main">
        <div className="container">
          <div className="page-header">
            <h1>Турніри</h1>
            <p className="page-subtitle">Переглядайте та участвуйте в турнірах</p>
          </div>

          {/* Search & Filters */}
          <div className="controls-section">
            <div className="search-box">
              <input
                type="text"
                placeholder="Пошук турніру..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            <div className="filter-chips">
              {filters.map(f => (
                <button
                  key={f.value}
                  className={`chip ${activeFilter === f.value ? 'active' : ''}`}
                  onClick={() => setActiveFilter(f.value)}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>

          {/* Content */}
          {loading ? (
            <div className="loading-state">
              <p>Завантажуємо турніри...</p>
            </div>
          ) : error ? (
            <div className="error-state">
              <p>❌ Помилка: {error}</p>
              <Button onClick={fetchTournaments}>Спробувати ще</Button>
            </div>
          ) : filteredTournaments.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🏆</div>
              <p>Турнірів не знайдено</p>
              <small>Спробуйте змінити фільтр або пошуковий запит</small>
            </div>
          ) : (
            <div className="tournament-grid">
              {filteredTournaments.map(tournament => (
                <div key={tournament.id} className="tournament-card">
                  <div className="card-image">
                    <img
                      src={tournament.image_url || 'https://via.placeholder.com/300x150'}
                      alt={tournament.title}
                    />
                    <span className={`status-badge ${getStatusBadgeColor(tournament.status)}`}>
                      {tournament.status}
                    </span>
                  </div>
                  <div className="card-content">
                    <h3>{tournament.title}</h3>
                    <p className="card-description">{tournament.description}</p>
                    <div className="card-meta">
                      <span>👥 {tournament.registered_teams || 0} команд</span>
                      <span>📊 Макс: {tournament.max_teams || '-'}</span>
                    </div>
                    <div className="card-actions">
                      <Button
                        onClick={() => navigate(`/tournaments/${tournament.id}`)}
                        className="btn-primary"
                      >
                        Переглянути →
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
