import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import tournamentApi from '../api/tournamentApi';
import Button from '../../../shared/components/Button';
import Input from '../../../shared/components/Input';
import '../styles/TournamentFormPage.css';

export default function TournamentFormPage() {
  const { id } = useParams(); // Якщо є ID, значить це редагування
  const navigate = useNavigate();
  const isEditMode = Boolean(id);

  const [formData, setFormData] = useState({
    title: '',
    game: 'CS2',
    status: 'майбутній',
    regStart: '',
    regEnd: '',
    description: '',
    imageUrl: ''
  });

  useEffect(() => {
    if (isEditMode) {
      // Завантажуємо дані турніру для редагування
      tournamentApi.getTournament(id).then(data => setFormData(data));
    }
  }, [id, isEditMode]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (isEditMode) {
        await tournamentApi.updateTournament(id, formData);
      } else {
        await tournamentApi.createTournament(formData);
      }
      navigate('/tournaments'); // Повертаємось до списку
    } catch (error) {
      alert("Помилка при збереженні: " + error.message);
    }
  };

  return (
    <div className="form-page-wrapper">
      <header className="form-header">
        <button className="back-link" onClick={() => navigate(-1)}>← Назад до турнірів</button>
        <h1>{isEditMode ? 'Редагувати турнір' : 'Створити новий турнір'}</h1>
      </header>

      <div className="form-container">
        <form onSubmit={handleSubmit} className="tournament-form">
          <section className="form-section">
            <h3>Основна інформація</h3>
            <label>Назва турніру</label>
            <Input 
              name="title"
              value={formData.title} 
              onChange={handleChange} 
              placeholder="Наприклад: Весняний Кубок" 
              required 
            />

            <div className="form-row">
              <div className="form-group">
                <label>Гра</label>
                <select name="game" value={formData.game} onChange={handleChange}>
                  <option value="CS2">CS2</option>
                  <option value="Dota 2">Dota 2</option>
                  <option value="Valorant">Valorant</option>
                  <option value="Fortnite">Fortnite</option>
                </select>
              </div>
              <div className="form-group">
                <label>Поточний статус</label>
                <select name="status" value={formData.status} onChange={handleChange}>
                  <option value="активний">Активний</option>
                  <option value="майбутній">Майбутній</option>
                  <option value="завершений">Завершений</option>
                </select>
              </div>
            </div>
          </section>

          <section className="form-section">
            <h3>Період реєстрації</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Дата початку</label>
                <input 
                  type="date" 
                  name="regStart" 
                  className="custom-date-input"
                  value={formData.regStart} 
                  onChange={handleChange} 
                />
              </div>
              <div className="form-group">
                <label>Дата закінчення</label>
                <input 
                  type="date" 
                  name="regEnd" 
                  className="custom-date-input"
                  value={formData.regEnd} 
                  onChange={handleChange} 
                />
              </div>
            </div>
          </section>

          <section className="form-section">
            <h3>Медіа та опис</h3>
            <label>Посилання на банер (URL)</label>
            <Input 
              name="imageUrl"
              value={formData.imageUrl} 
              onChange={handleChange} 
              placeholder="https://..." 
            />
            <label>Додаткова інформація</label>
            <textarea 
              name="description"
              rows="4" 
              value={formData.description} 
              onChange={handleChange}
              placeholder="Правила, призовий фонд тощо..."
            />
          </section>

          <div className="form-actions">
            <Button type="button" className="btn-secondary" onClick={() => navigate(-1)}>Скасувати</Button>
            <Button type="submit" className="btn-primary">
              {isEditMode ? 'Зберегти зміни' : 'Опублікувати турнір'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
