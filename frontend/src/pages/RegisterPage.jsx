import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../pages/styles/LoginPage.css'; // той самий CSS
import Input from '../components/Input';
import Button from '../components/Button';
import { register } from '../api/auth';

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

  const validateForm = () => {
    const newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!form.firstName.trim()) newErrors.firstName = 'First name is required';
    if (!form.lastName.trim()) newErrors.lastName = 'Last name is required';

    if (!form.email) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(form.email)) {
      newErrors.email = 'Enter a valid email address';
    }

    if (!form.password) {
      newErrors.password = 'Password is required';
    } else if (form.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!form.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (form.password !== form.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    return newErrors;
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setApiError('');

    const validationErrors = validateForm();
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
          <img src="https://via.placeholder.com/80x80.png?text=Logo" alt="Innovators Lab" />
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
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg"
            alt="Google"
          />
          Sign up with Google
        </Button>
      </div>
    </div>
  );
}