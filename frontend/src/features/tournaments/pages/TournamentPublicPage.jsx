import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import tournamentApi from '../api/tournamentApi';
import Button from '../../../shared/components/Button';
import '../styles/TournamentPublicPage.css';

export default function TournamentPublicPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [tournament, setTournament] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Отримуємо дані турніру через API
    tournamentApi.getTournament(id)
      .then(data => {
        setTournament(data);
        setLoading(false);
      })
      .catch(err => console.error(err));
  }, [id]);

  if (loading) return <div className="loader">Завантаження турніру...</div>;

  // Логіка доступності реєстрації
  const now = new Date();
  const regStart = new Date(tournament.regStart);
  const regEnd = new Date(tournament.regEnd);
  const isRegistrationOpen = now >= regStart && now <= regEnd && tournament.status === 'активний';

  return (
    <div className="public-page">
      {/* Hero Section з банером */}
      <div className="tournament-hero" style={{ backgroundImage: `url(${tournament.imageUrl || 'https://via.placeholder.com/1200x400'})` }}>
        <div className="hero-overlay">
          <div className="hero-container">
            <span className={`status-tag ${tournament.status}`}>{tournament.status}</span>
            <h1>{tournament.title}</h1>
            <div className="game-badge">{tournament.game}</div>
          </div>
        </div>
      </div>

      <div className="content-grid">
        {/* Основна інформація */}
        <main className="info-column">
          <section className="info-block">
            <h2>Про турнір</h2>
            <p className="description-text">{tournament.description || "Опис турніру відсутній."}</p>
          </section>

          <section className="info-block">
            <h2>Правила</h2>
            <div className="rules-content">
              {tournament.rules ? (
                <div dangerouslySetInnerHTML={{ __html: tournament.rules }} />
              ) : (
                <ul>
                  <li>Формат: Double Elimination</li>
                  <li>Сервер: Europe West</li>
                  <li>Максимальна кількість команд: 16</li>
                </ul>
              )}
            </div>
          </section>

          <section className="info-block">
            <h2>Список команд ({tournament.teams?.length || 0})</h2>
            <div className="teams-list">
              {tournament.teams && tournament.teams.length > 0 ? (
                tournament.teams.map((team, idx) => (
                  <div key={idx} className="team-item">
                    <span className="team-rank">{idx + 1}</span>
                    <img src={team.logo || 'https://via.placeholder.com/40'} alt="logo" />
                    <span className="team-name">{team.name}</span>
                  </div>
                ))
              ) : (
                <p className="empty-msg">Команд поки немає. Будьте першими!</p>
              )}
            </div>
          </section>
        </main>

        {/* Бокова панель з діями */}
        <aside className="action-sidebar">
          <div className="registration-card">
            <h3>Реєстрація</h3>
            <div className="date-info">
              <div className="date-row">
                <span>Початок:</span>
                <strong>{new Date(tournament.regStart).toLocaleDateString()}</strong>
              </div>
              <div className="date-row">
                <span>Кінець:</span>
                <strong>{new Date(tournament.regEnd).toLocaleDateString()}</strong>
              </div>
            </div>

            {isRegistrationOpen ? (
              <Button className="btn-register" onClick={() => navigate(`/tournaments/${id}/register`)}>
                Зареєструватись
              </Button>
            ) : (
              <div className="reg-closed-msg">
                {now < regStart ? "Реєстрація ще не почалася" : "Реєстрація закрита"}
              </div>
            )}
            
            <p className="sidebar-hint">Для участі ви повинні мати сформовану команду в профілі.</p>
          </div>

          <div className="share-card">
            <h4>Поділитися</h4>
            <div className="share-links">
              {/* Іконки соцмереж */}
              <button className="share-btn">Link</button>
              <button className="share-btn">TG</button>
              <button className="share-btn">DC</button>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
