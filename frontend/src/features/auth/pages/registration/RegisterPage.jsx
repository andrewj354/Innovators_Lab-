import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../../styles/registration/RegisterPage.css';
import { register } from '../../api/authApi';
import { validateRegistrationForm, validateRegistrationField } from '../../validation/authValidation';
import Logo from '../../../../assets/Logo.svg';

export default function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleChange = (field) => (e) => {
    let value = e.target.value;

    if (field === 'username') {
      value = value.replace(/[^a-zA-Z0-9_]/g, '');
    }

    setForm((prev) => ({ ...prev, [field]: value }));

    if (touched[field]) {
      const error = validateRegistrationField(field, value, { ...form, [field]: value });
      setErrors((prev) => ({ ...prev, [field]: error || '' }));
    }
  };

  const handleBlur = (field) => () => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    const error = validateRegistrationField(field, form[field], form);
    setErrors((prev) => ({ ...prev, [field]: error || '' }));
  };

  const isFormFilled = form.username && form.email && form.password && form.confirmPassword;

  const hasErrors = Object.values(errors).some((e) => e);

  const handleRegister = async (e) => {
    e.preventDefault();

    setTouched({ username: true, email: true, password: true, confirmPassword: true });

    const validationErrors = validateRegistrationForm(form);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      toast.error('Please fix the errors before continuing');
      return;
    }

    navigate('/register/step2', {
      state: {
        step1Data: {
          username: form.username,
          email: form.email,
          password: form.password,
        },
      },
    });
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

        <h2>Create An Account and Sign Up</h2>

        <form onSubmit={handleRegister} noValidate>
          <div className="field-group">
            <label className={touched.username && errors.username ? 'label-error' : ''}>
              Username
            </label>
            <input
              type="text"
              placeholder="Enter your username"
              value={form.username}
              onChange={handleChange('username')}
              onBlur={handleBlur('username')}
              className={touched.username && errors.username ? 'input-error-border' : ''}
            />
            {touched.username && errors.username && (
              <span className="field-error">{errors.username}</span>
            )}
          </div>

          <div className="field-group">
            <label className={touched.email && errors.email ? 'label-error' : ''}>
              Email
            </label>
            <input
              type="email"
              placeholder="Enter email"
              value={form.email}
              onChange={handleChange('email')}
              onBlur={handleBlur('email')}
              className={touched.email && errors.email ? 'input-error-border' : ''}
            />
            {touched.email && errors.email && (
              <span className="field-error">{errors.email}</span>
            )}
          </div>

          <div className="field-group">
            <label className={touched.password && errors.password ? 'label-error' : ''}>
              Password
            </label>
            <div className="password-wrapper">
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange('password')}
                onBlur={handleBlur('password')}
                className={touched.password && errors.password ? 'input-error-border' : ''}
              />
              <button
                type="button"
                className="eye-btn"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex={-1}
              >
                {showPassword ? (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                )}
              </button>
            </div>
            {touched.password && errors.password && (
              <span className="field-error">{errors.password}</span>
            )}
          </div>

          <div className="field-group">
            <label className={touched.confirmPassword && errors.confirmPassword ? 'label-error' : ''}>
              Confirm password
            </label>
            <div className="password-wrapper">
              <input
                type={showConfirm ? 'text' : 'password'}
                placeholder="Confirm password"
                value={form.confirmPassword}
                onChange={handleChange('confirmPassword')}
                onBlur={handleBlur('confirmPassword')}
                className={touched.confirmPassword && errors.confirmPassword ? 'input-error-border' : ''}
              />
              <button
                type="button"
                className="eye-btn"
                onClick={() => setShowConfirm(!showConfirm)}
                tabIndex={-1}
              >
                {showConfirm ? (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                    <line x1="1" y1="1" x2="23" y2="23" />
                  </svg>
                )}
              </button>
            </div>
            {touched.confirmPassword && errors.confirmPassword && (
              <span className="field-error">{errors.confirmPassword}</span>
            )}
          </div>

          <button
            type="submit"
            className={`btn-next ${!isFormFilled || hasErrors ? 'btn-disabled' : ''}`}
            disabled={!isFormFilled || hasErrors || loading}
          >
            {loading ? 'Creating...' : 'Next'}
          </button>
        </form>
      </div>
    </div>
  );
}
