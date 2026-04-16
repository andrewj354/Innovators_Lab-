import React, { useState } from 'react';
import '../styles/TournamentListPage.css';
import Button from '../components/Button'; // Використовуємо ваш компонент кнопки

export default function TournamentListPage() {
  const [activeFilter, setActiveFilter] = useState('Всі Турніри');

  const tournaments = [
    {
      id: 1,
      game: 'CS2',
      title: 'Весняний Чемпіонат по CS2',
      status: 'активний',
      regDate: '01.04.2024 - 15.04.2024',
      image: 'https://via.placeholder.com/300x150?text=CS2',
      btnText: 'Реєструватися'
    },
    {
      id: 2,
      game: 'League of Legends',
      title: 'Ліга Геймерів League of Legends',
      status: 'майбутній',
      regDate: '10.05.2024 - 25.05.2024',
      image: 'https://via.placeholder.com/300x150?text=LoL',
      btnText: 'В очікуванні'
    },
    {
      id: 3,
      game: 'Dota 2',
      title: 'Кубок України Dota 2',
      status: 'завершений',
      regDate: '15.02.2024 - 28.02.2024',
      image: 'https://via.placeholder.com/300x150?text=Dota2',
      btnText: 'Результати'
    },
    {
        id: 4,
        game: 'VALORANT',
        title: 'Відкритий Турнір по Valorant',
        status: 'активний',
        regDate: '20.03.2024 - 10.04.2024',
        image: 'https://via.placeholder.com/300x150?text=Valorant',
        btnText: 'Реєструватися'
      },
      {
        id: 5,
        game: 'FORTNITE',
        title: 'Фінал Сезону Fortnite',
        status: 'майбутній',
        regDate: '05.06.2024 - 20.06.2024',
        image: 'https://via.placeholder.com/300x150?text=Fortnite',
        btnText: 'В очікуванні'
      }
  ];

  const filters = ['Реєстрація', 'Проводяться', 'Завершені', 'Всі Турніри'];

  return (
    <div className="hub-wrapper">
      {/* Навігаційна панель */}
      <header className="hub-header">
        <div className="header-content">
          <div className="hub-logo">TOURNAMENT HUB</div>
          <nav className="hub-nav">
            <a href="#home">Головна</a>
            <a href="#my">Мої Турніри</a>
            <a href="#profile">Профіль</a>
            <span className="lang-switch">UA/EN</span>
            <div className="user-info">
              <img src="https://via.placeholder.com/32" alt="Avatar" className="avatar" />
              <span>Іван К.</span>
            </div>
          </nav>
        </div>
      </header>

      <main className="hub-main">
        <div className="content-container">
          
          {/* Основна частина з турнірами */}
          <section className="tournaments-section">
            <div className="section-header">
              <h1>Список Турнірів</h1>
              <div className="search-box">
                <input type="text" placeholder="Пошук" />
              </div>
            </div>

            <div className="filter-bar">
              {filters.map(f => (
                <button 
                  key={f} 
                  className={`filter-chip ${activeFilter === f ? 'active' : ''}`}
                  onClick={() => setActiveFilter(f)}
                >
                  {f}
                </button>
              ))}
            </div>

            <div className="tournament-grid">
              {tournaments.map(t => (
                <div key={t.id} className="tournament-card">
                  <div className="card-banner" style={{backgroundImage: `url(${t.image})`}}>
                    <span className="game-label">{t.game}</span>
                  </div>
                  <div className="card-body">
                    <div className="title-row">
                      <h3>{t.title}</h3>
                      <span className={`status-badge ${t.status}`}>{t.status}</span>
                    </div>
                    <p className="reg-info">Реєстрація: {t.regDate}</p>
                    <div className="card-actions">
                      <Button className="btn-action">{t.btnText}</Button>
                      <button className="btn-folder">📁</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Бокова панель Empty State */}
          <aside className="empty-state-sidebar">
            <h3>Empty State</h3>
            <div className="sidebar-filters">
              <span>Реєстрація</span>
              <span>Проводяться</span>
              <span className="active">Завершені</span>
            </div>
            <div className="empty-content">
              <div className="empty-icon">🏆🔍</div>
              <h4>Ой! Наразі завершених турнірів немає.</h4>
              <p>Перевірте інші вкладки або поверніться пізніше.</p>
            </div>
          </aside>

        </div>
      </main>
    </div>
  );
}