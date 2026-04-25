import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/LoginPage.css'; // той самий CSS
import Input from '../../../shared/components/Input';
import Button from '../../../shared/components/Button';
import { register } from '../api/authApi';
import { validateRegistrationForm } from '../validation/authValidation';
import Logo from '../../../assets/Logo.svg';

export default function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
    // Скидаємо помилку поля при редагуванні
    if (errors[field]) setErrors((prev) => ({ ...prev, [field]: '' }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = validateRegistrationForm(form);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    try {
      await register({
        firstName: form.firstName,
        lastName: form.lastName,
        email: form.email,
        password: form.password,
      });

      // Після успішної реєстрації — редирект на логін
      navigate('/login');
    } catch (err) {
      setApiError(err.response?.data?.message || err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        <div className="logo">
          <img src={Logo} alt="Innovators Lab" />
        </div>
        <h2>Create your account</h2>

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

        <form onSubmit={handleRegister} noValidate>
          <div style={{ display: 'flex', gap: '10px' }}>
            <Input
              type="text"
              placeholder="First name"
              value={form.firstName}
              onChange={handleChange('firstName')}
              error={errors.firstName}
            />
            <Input
              type="text"
              placeholder="Last name"
              value={form.lastName}
              onChange={handleChange('lastName')}
              error={errors.lastName}
            />
          </div>

          <Input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={handleChange('email')}
            error={errors.email}
          />
          <Input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange('password')}
            error={errors.password}
          />
          <Input
            type="password"
            placeholder="Confirm password"
            value={form.confirmPassword}
            onChange={handleChange('confirmPassword')}
            error={errors.confirmPassword}
          />

          <Button type="submit" className="btn-login" disabled={loading}>
            {loading ? 'Creating account...' : 'Create account'}
          </Button>
        </form>

        <div className="links-text">
          Already have an account? <a href="/login" className="bold">Sign in</a>
        </div>

        <Button className="btn-google">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
          </svg>
          Sign up with Google
        </Button>
      </div>
    </div>
  );
}
