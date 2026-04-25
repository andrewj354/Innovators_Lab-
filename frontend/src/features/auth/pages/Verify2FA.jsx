import { useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../styles/Verify2FA.css';
import Logo from '../../../assets/Logo.svg';

export default function Verify2FA() {
  const navigate = useNavigate();
  const location = useLocation();
  const inputsRef = useRef([]);

  const email = location.state?.email || '';

  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [secondsLeft, setSecondsLeft] = useState(60);
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    if (!email) {
      toast.warn('Please complete registration first');
      navigate('/register');
    }
  }, [email, navigate]);

  useEffect(() => {
    if (secondsLeft === 0) {
      setCanResend(true);
      return;
    }

    const timer = setInterval(() => {
      setSecondsLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [secondsLeft]);

  const formatTime = (seconds) => {
    const min = String(Math.floor(seconds / 60)).padStart(2, '0');
    const sec = String(seconds % 60).padStart(2, '0');
    return `${min}:${sec}`;
  };

  const handleChange = (value, index) => {
    if (!/^\d?$/.test(value)) return;

    const next = [...otp];
    next[index] = value;
    setOtp(next);

    if (value && index < 5) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
    if (!pasted) return;

    const next = ['', '', '', '', '', ''];
    pasted.split('').forEach((digit, idx) => {
      next[idx] = digit;
    });

    setOtp(next);
    inputsRef.current[Math.min(pasted.length, 5)]?.focus();
  };

  const isOtpComplete = otp.every((d) => d !== '');

  const handleVerify = () => {
    const code = otp.join('');
    if (code.length !== 6) {
      toast.warn('Please enter the full 6-digit code');
      return;
    }

    // TODO: виклик API для перевірки OTP
    console.log('OTP code:', code);
    toast.success('Account verified successfully!');
    navigate('/login');
  };

  const handleResend = () => {
    setOtp(['', '', '', '', '', '']);
    setSecondsLeft(60);
    setCanResend(false);
    inputsRef.current[0]?.focus();
    toast.info('OTP has been resent to your email');
  };

  if (!email) return null;

  return (
    <div className="verify-page">
      <div className="verify-card">
        <button type="button" className="back-btn" onClick={() => navigate('/login')}>
          ←
        </button>

        <div className="verify-logo">
          <img src={Logo} alt="Innovators Lab" />
        </div>

        <h1 className="verify-title">OTP Verification</h1>
        <p className="verify-text">
          We will send you a one time password to your email address
        </p>
        <p className="verify-email">{email}</p>

        <div className="otp-row">
          {otp.map((digit, index) => (
            <input
              key={index}
              ref={(el) => (inputsRef.current[index] = el)}
              className={`otp-input ${digit ? 'otp-filled' : ''}`}
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(e.target.value, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
              onPaste={index === 0 ? handlePaste : undefined}
            />
          ))}
        </div>

        <div className="timer">{formatTime(secondsLeft)}</div>

        <div className="resend-line">
          Didn't you receive the OTP?{' '}
          <button
            type="button"
            className="resend-btn"
            onClick={handleResend}
            disabled={!canResend}
          >
            Resend OTP
          </button>
        </div>

        <button
          className={`verify-btn ${!isOtpComplete ? 'verify-btn-disabled' : ''}`}
          onClick={handleVerify}
          disabled={!isOtpComplete}
        >
          Verify
        </button>
      </div>
    </div>
  );
}
