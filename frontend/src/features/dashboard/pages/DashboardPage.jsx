import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../shared/context/AuthContext';
import Navbar from '../../../shared/components/Navbar';
import { getTournaments } from '../../../features/tournaments/api/tournamentApi';
import { getSubmissions } from '../../../shared/api/submissionsApi';
import '../styles/DashboardPage.css';

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, logout, isAuthenticated, loading } = useAuth();
  const [stats, setStats] = useState({
    activeTournaments: 0,
    completedTournaments: 0,
    totalPoints: 0,
    submissionCount: 0
  });
  const [dashboardLoading, setDashboardLoading] = useState(true);

  // Check if user is authenticated
  useEffect(() => {
    if (!loading && !isAuthenticated) {
      navigate('/login', { replace: true });
    }
  }, [isAuthenticated, loading, navigate]);

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        setDashboardLoading(true);
        
        // Fetch tournaments
        const tournamentsRes = await getTournaments();
        const tournaments = tournamentsRes.data?.results || tournamentsRes.results || tournamentsRes.data || [];
        
        // Count active vs completed tournaments
        const activeTournaments = tournaments.filter(t => t.status === 'active' || t.status === 'running').length;
        const completedTournaments = tournaments.filter(t => t.status === 'completed' || t.status === 'finished').length;
        
        // Fetch submissions
        const submissionsRes = await getSubmissions();
        const submissions = submissionsRes.data?.results || submissionsRes.results || submissionsRes.data || [];
        const submissionCount = submissions.length;
        
        // Calculate total points from submissions
        const totalPoints = submissions.reduce((sum, sub) => sum + (sub.score || 0), 0);
        
        setStats({
          activeTournaments,
          completedTournaments,
          totalPoints,
          submissionCount
        });
      } catch (error) {
        console.error('Error loading dashboard data:', error);
        setStats({
          activeTournaments: 0,
          completedTournaments: 0,
          totalPoints: 0,
          submissionCount: 0
        });
      } finally {
        setDashboardLoading(false);
      }
    };

    if (user) {
      loadDashboardData();
    }
  }, [user]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="dashboard-wrapper">
      <Navbar user={user} onLogout={handleLogout} />
      
      <div className="dashboard-container">
        <div className="welcome-section">
          <h1>Ласкаво просимо, {user?.first_name || user?.email}! 👋</h1>
          <p>До платформи Innovators Lab</p>
        </div>

        <div className="dashboard-grid">
          {/* Tournament Card */}
          <div className="dashboard-card">
            <div className="card-icon">🏆</div>
            <h3>Турніри</h3>
            <p>Переглядайте та участвуйте в турнірах</p>
            <button 
              className="card-button"
              onClick={() => handleNavigate('/tournaments')}
            >
              Перейти →
            </button>
          </div>

          {/* My Tournaments Card */}
          <div className="dashboard-card">
            <div className="card-icon">📋</div>
            <h3>Мої Турніри</h3>
            <p>Турніри, в яких ви беруть участь</p>
            <button 
              className="card-button"
              onClick={() => handleNavigate('/tournaments')}
            >
              Переглянути →
            </button>
          </div>

          {/* Submissions Card */}
          <div className="dashboard-card">
            <div className="card-icon">📤</div>
            <h3>Мої Відповіді</h3>
            <p>Ваші надіслані рішення та статус</p>
            <button 
              className="card-button"
              onClick={() => handleNavigate('/submissions')}
            >
              Переглянути →
            </button>
          </div>

          {/* Leaderboard Card */}
          <div className="dashboard-card">
            <div className="card-icon">🏅</div>
            <h3>Рейтинги</h3>
            <p>Дивіться рейтинги учасників</p>
            <button 
              className="card-button"
              onClick={() => handleNavigate('/tournaments')}
            >
              Переглянути →
            </button>
          </div>

          {/* Profile Card */}
          <div className="dashboard-card">
            <div className="card-icon">👤</div>
            <h3>Профіль</h3>
            <p>Управління вашим профілем</p>
            <button 
              className="card-button"
              onClick={() => handleNavigate('/profile')}
            >
              Перейти →
            </button>
          </div>

          {/* Settings Card */}
          <div className="dashboard-card">
            <div className="card-icon">⚙️</div>
            <h3>Параметри</h3>
            <p>Налаштуйте ваш акаунт</p>
            <button 
              className="card-button"
              onClick={() => handleNavigate('/settings')}
            >
              Перейти →
            </button>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="quick-stats">
          <div className="stat-item">
            <span className="stat-label">Активні турніри:</span>
            <span className="stat-value">{loading ? '...' : stats.activeTournaments}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Завершені:</span>
            <span className="stat-value">{loading ? '...' : stats.completedTournaments}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Очки:</span>
            <span className="stat-value">{loading ? '...' : stats.totalPoints}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
