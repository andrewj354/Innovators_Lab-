import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../styles/ProfilePage.css';
import Button from '../../../shared/components/Button';
import Navbar from '../../../shared/components/Navbar';
import { useAuth } from '../../../shared/context/AuthContext';

export default function ProfilePage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    email: user?.email || '',
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
  });

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // TODO: Implement update profile API call
      toast.success('Профіль оновлено');
      setIsEditing(false);
    } catch (err) {
      toast.error('Помилка при оновленні профілю');
    }
  };

  return (
    <div className="page-wrapper">
      <Navbar user={user} onLogout={handleLogout} />

      <main className="page-main">
        <div className="container">
          <div className="profile-header">
            <h1>Мій Профіль</h1>
          </div>

          <div className="profile-content">
            <div className="profile-card">
              <div className="profile-avatar">
                <div className="avatar-placeholder">👤</div>
              </div>

              {!isEditing ? (
                <div className="profile-view">
                  <div className="profile-info">
                    <div className="info-row">
                      <label>Email:</label>
                      <p>{user?.email}</p>
                    </div>
                    <div className="info-row">
                      <label>Ім'я:</label>
                      <p>{user?.first_name || 'Не вказано'}</p>
                    </div>
                    <div className="info-row">
                      <label>Прізвище:</label>
                      <p>{user?.last_name || 'Не вказано'}</p>
                    </div>
                  </div>

                  <div className="profile-actions">
                    <Button onClick={() => setIsEditing(true)} className="btn-primary">
                      Редагувати Профіль
                    </Button>
                    <Button onClick={handleLogout} className="btn-secondary">
                      Вийти
                    </Button>
                  </div>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="profile-form">
                  <div className="form-group">
                    <label>Email:</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      disabled
                    />
                  </div>

                  <div className="form-group">
                    <label>Ім'я:</label>
                    <input
                      type="text"
                      name="first_name"
                      value={formData.first_name}
                      onChange={handleChange}
                    />
                  </div>

                  <div className="form-group">
                    <label>Прізвище:</label>
                    <input
                      type="text"
                      name="last_name"
                      value={formData.last_name}
                      onChange={handleChange}
                    />
                  </div>

                  <div className="form-actions">
                    <Button type="submit" className="btn-primary">
                      Зберегти
                    </Button>
                    <Button
                      type="button"
                      onClick={() => setIsEditing(false)}
                      className="btn-secondary"
                    >
                      Скасувати
                    </Button>
                  </div>
                </form>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
