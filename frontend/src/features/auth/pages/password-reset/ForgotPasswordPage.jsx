import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { forgotPassword } from '../../api/authApi';
import { validateForgotPassword } from '../../validation/authValidation';
import '../../styles/password-reset/ResetPassword.css';
import Logo from '../../../../assets/Logo.svg';

export default function ForgotPasswordPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [touched, setTouched] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const value = e.target.value;
    setEmail(value);
    if (touched) {
      setError(validateForgotPassword(value) || '');
    }
  };

  const handleBlur = () => {
    setTouched(true);
    setError(validateForgotPassword(email) || '');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setTouched(true);

    const validationError = validateForgotPassword(email);
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    try {
      await forgotPassword(email);
      navigate('/forgot-password/sent', { state: { email } });
    } catch (err) {
      toast.error('Failed to send reset link. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-container">
        <button type="button" className="back-btn" onClick={() => navigate('/login')}>
          ←
        </button>

        <div className="logo">
          <img src={Logo} alt="Innovators Lab" />
        </div>

        <h2>Reset password to Innovators lab</h2>

        <p style={{ textAlign: 'center', fontSize: '14px', color: '#555', marginBottom: '32px' }}>
          Enter your email and we'll send you a link to create new password
        </p>

        <form onSubmit={handleSubmit} noValidate>
          <div className="field-group">
            <label className={touched && error ? 'label-error' : ''}>
              Email
            </label>
            <input
              type="email"
              placeholder="Enter email"
              className={touched && error ? 'input-error-border' : ''}
              value={email}
              onChange={handleChange}
              onBlur={handleBlur}
            />
            {touched && error && (
              <span className="field-error">{error}</span>
            )}
          </div>

          <button
            type="submit"
            className={`btn-next ${loading || !!error || !email ? 'btn-disabled' : ''}`}
            disabled={loading || !!error || !email}
          >
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
}
