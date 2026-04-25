import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import { forgotPassword } from '../../api/authApi';
import '../../styles/password-reset/ResetPassword.css';
import Logo from '../../../../assets/Logo.svg';

export default function ForgotPasswordSentPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const email = location.state?.email || '';

  const [resending, setResending] = useState(false);

  const handleLogoClick = () => {
    navigate(`/reset-password?token=demo-token-123`);
  };

  const handleResend = async () => {
    if (!email) {
      toast.error('Email is missing. Please go back and try again.');
      return;
    }

    setResending(true);
    try {
      await forgotPassword(email);
      toast.success('Reset link resent to your email!');
    } catch (err) {
      toast.error('Failed to resend link.');
    } finally {
      setResending(false);
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-container">
        <button type="button" className="back-btn" onClick={() => navigate('/login')}>
          ←
        </button>

        <div className="logo" onClick={handleLogoClick} style={{ cursor: 'pointer' }} title="Click for demo reset step">
          <img src={Logo} alt="Innovators Lab" />
        </div>

        <h2>Reset password to Innovators lab</h2>

        <div style={{ textAlign: 'center', fontSize: '14px', color: '#333', marginBottom: '32px' }}>
          <p style={{ marginBottom: '16px' }}>
            We sent you an email with link to create new password. Check your inbox
          </p>
          <p>
            Didn't receive the link?{' '}
            <button
              type="button"
              className="reset-link-btn"
              onClick={handleResend}
              disabled={resending}
              style={{ color: '#00c3df' }}
            >
              {resending ? 'Sending...' : 'Resend email'}
            </button>
          </p>
        </div>

        <button
          type="button"
          className="btn-next"
          onClick={() => navigate('/login')}
        >
          Back to login
        </button>
      </div>
    </div>
  );
}
