import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/LoginPage.css'; // Підключаємо стилі сторінки
import Input from '../components/Input';   // Беремо наш інпут
import Button from '../components/Button'; // Беремо нашу кнопку
import { login } from '../api/auth';

export default function LoginPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setApiError('');

    if (!form.email || !form.password) {
      setApiError('Email and password are required');
      return;
    }

    setLoading(true);
    try {
      await login({ email: form.email, password: form.password });
      navigate('/dashboard');
    } catch (err) {
      setApiError(err.response?.data?.message ?? err.message ?? 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        
        <div className="logo">
          <img src="https://via.placeholder.com/80x80.png?text=Logo" alt="Innovators Lab" />
        </div>

        <h2>Sign in to ChatoPotamus</h2>

        <form onSubmit={handleLogin}>
          {apiError && (
            <div style={{
              background: '#fff5f5',
              border: '1px solid #fed7d7',
              borderRadius: '6px',
              padding: '10px 14px',
              marginBottom: '16px',
              fontSize: '13px',
              color: '#c53030',
              textAlign: 'left',
            }}>
              {apiError}
            </div>
          )}

          {/* Використовуємо наш компонент Input */}
          <Input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange('email')}
            required={true}
          />
          <Input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange('password')}
            required={true}
          />

          {/* Використовуємо наш компонент Button */}
          <Button type="submit" className="btn-login" disabled={loading}>
            {loading ? 'Signing in...' : 'Log in'}
          </Button>
        </form>

        <div className="links-text">
          Forgot password? Don't worry <a href="#reset">reset it here!</a>
        </div>

        <div className="links-text">
          Don't have an account ? <a href="#signup" className="bold">Sign Up.</a>
        </div>

        <Button className="btn-google">
          <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google" />
          Log In with Google
        </Button>

      </div>
    </div>
  );
}