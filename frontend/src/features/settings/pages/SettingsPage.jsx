import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../styles/SettingsPage.css';
import Button from '../../../shared/components/Button';
import Navbar from '../../../shared/components/Navbar';
import { useAuth } from '../../../shared/context/AuthContext';

export default function SettingsPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [settings, setSettings] = useState({
    notifications_enabled: true,
    email_notifications: true,
    dark_mode: false,
    language: 'uk'
  });

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleChange = (e) => {
    const { name, type, checked, value } = e.target;
    setSettings({
      ...settings,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSaveSettings = async (e) => {
    e.preventDefault();
    try {
      // TODO: Implement save settings API call
      toast.success('Налаштування збережено');
    } catch (err) {
      toast.error('Помилка при збереженні налаштувань');
    }
  };

  return (
    <div className="page-wrapper">
      <Navbar user={user} onLogout={handleLogout} />

      <main className="page-main">
        <div className="container">
          <div className="settings-header">
            <h1>Налаштування</h1>
          </div>

          <div className="settings-content">
            <form onSubmit={handleSaveSettings} className="settings-form">
              <div className="settings-section">
                <h3>Сповіщення</h3>
                <div className="form-group checkbox-group">
                  <label>
                    <input
                      type="checkbox"
                      name="notifications_enabled"
                      checked={settings.notifications_enabled}
                      onChange={handleChange}
                    />
                    <span>Включити сповіщення</span>
                  </label>
                </div>

                <div className="form-group checkbox-group">
                  <label>
                    <input
                      type="checkbox"
                      name="email_notifications"
                      checked={settings.email_notifications}
                      onChange={handleChange}
                    />
                    <span>Отримувати листи про оновлення</span>
                  </label>
                </div>
              </div>

              <div className="settings-section">
                <h3>Дизайн</h3>
                <div className="form-group">
                  <label htmlFor="language">Мова:</label>
                  <select
                    id="language"
                    name="language"
                    value={settings.language}
                    onChange={handleChange}
                  >
                    <option value="uk">Українська</option>
                    <option value="en">English</option>
                  </select>
                </div>

                <div className="form-group checkbox-group">
                  <label>
                    <input
                      type="checkbox"
                      name="dark_mode"
                      checked={settings.dark_mode}
                      onChange={handleChange}
                    />
                    <span>Темна тема (скоро)</span>
                  </label>
                </div>
              </div>

              <div className="settings-section">
                <h3>Безпека</h3>
                <Button type="button" className="btn-secondary">
                  Змінити Пароль
                </Button>
              </div>

              <div className="settings-actions">
                <Button type="submit" className="btn-primary">
                  Зберегти Налаштування
                </Button>
                <Button
                  type="button"
                  onClick={() => navigate('/dashboard')}
                  className="btn-secondary"
                >
                  Повернутися
                </Button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
