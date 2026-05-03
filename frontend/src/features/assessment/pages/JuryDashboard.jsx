import React from 'react';
import '../styles/JuryDashboard.css'; // Зверни увагу на шлях
import Button from '../components/Button';

// Приклад даних, які прийдуть з бекенду
const assignedWorks = [
  { id: 1, teamName: 'Cyber Pandas', github: 'https://github.com/1', video: 'https://youtube.com/1', status: 'rated' },
  { id: 2, teamName: 'Binary Beasts', github: 'https://github.com/2', video: 'https://youtube.com/2', status: 'not_rated' },
  { id: 3, teamName: 'Eco Coders', github: 'https://github.com/3', video: 'https://youtube.com/3', status: 'not_rated' },
];

export default function JuryDashboard({ userRole = 'jury' }) {
  // Проста перевірка ProtectedRoute (якщо не журі — доступ закритий)
  if (userRole !== 'jury') {
    return <div className="error-access">Access Denied. Jury only.</div>;
  }

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h2>Jury Dashboard</h2>
          <p>Assigned Projects for Review</p>
        </div>

        <div className="works-list">
          {assignedWorks.map((work) => (
            <div key={work.id} className="work-card">
              <div className="work-info">
                <span className="team-name">{work.teamName}</span>
                <div className="links-group">
                  <a href={work.github} target="_blank" rel="noreferrer" className="link-item">GitHub</a>
                  <a href={work.video} target="_blank" rel="noreferrer" className="link-item">Video</a>
                </div>
              </div>

              <div className="work-actions">
                <span className={`badge ${work.status}`}>
                  {work.status === 'rated' ? 'Оцінено' : 'Не оцінено'}
                </span>
                <Button className="btn-review">
                  {work.status === 'rated' ? 'Edit Score' : 'Review'}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}