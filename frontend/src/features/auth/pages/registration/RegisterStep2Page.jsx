import React, { useState, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../../styles/registration/RegisterPage.css';
import '../../styles/registration/RegisterStep2Page.css';
import { register } from '../../api/authApi';
import { validateProfileForm, validateProfileField } from '../../validation/authValidation';
import Logo from '../../../../assets/Logo.svg';

export default function RegisterStep2Page() {
  const navigate = useNavigate();
  const location = useLocation();

  const step1Data = location.state?.step1Data;

  if (!step1Data) {
    return (
      <div className="register-wrapper">
        <div className="register-container" style={{ textAlign: 'center', paddingTop: '100px' }}>
          <p>Registration data is missing.</p>
          <button
            className="btn-next"
            style={{ marginTop: '20px' }}
            onClick={() => navigate('/register')}
          >
            Go back to Step 1
          </button>
        </div>
      </div>
    );
  }

  const [form, setForm] = useState({
    firstName: '',
    lastName: '',
    dateOfBirth: '',
  });
  const [avatar, setAvatar] = useState(null);
  const [avatarPreview, setAvatarPreview] = useState(null);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleChange = (field) => (e) => {
    const value = e.target.value;
    setForm((prev) => ({ ...prev, [field]: value }));

    if (touched[field]) {
      const error = validateProfileField(field, value);
      setErrors((prev) => ({ ...prev, [field]: error || '' }));
    }
  };

  const handleBlur = (field) => () => {
    setTouched((prev) => ({ ...prev, [field]: true }));
    const error = validateProfileField(field, form[field]);
    setErrors((prev) => ({ ...prev, [field]: error || '' }));
  };

  const handleAvatarClick = () => {
    fileInputRef.current?.click();
  };

  const handleAvatarChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.type.startsWith('image/')) {
      toast.error('Please select an image file');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      toast.error('Image must be less than 5 MB');
      return;
    }

    setAvatar(file);
    const reader = new FileReader();
    reader.onload = (ev) => setAvatarPreview(ev.target.result);
    reader.readAsDataURL(file);
  };

  const isFormFilled = form.firstName && form.lastName && form.dateOfBirth;
  const hasErrors = Object.values(errors).some((e) => e);

  // RegisterStep2Page.js

  const handleSubmit = async (e) => {
    e.preventDefault();

    setTouched({ firstName: true, lastName: true, dateOfBirth: true });

    const validationErrors = validateProfileForm(form);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      toast.error('Please fix the errors before continuing');
      return;
    }

    setErrors({});
    setLoading(true);

    try {
      // ТУТ ВАЖЛИВА ПРАВКА:
      // Перетворюємо дані у формат, який розуміє Django (snake_case)
      const registrationData = {
        username: step1Data.username,
        email: step1Data.email,
        password: step1Data.password,
        password_confirm: step1Data.password, // Додаємо підтвердження (копія пароля)
        first_name: form.firstName,           // firstName -> first_name
        last_name: form.lastName,             // lastName -> last_name
        date_of_birth: form.dateOfBirth,      // dateOfBirth -> date_of_birth
      };

      await register(registrationData);

      navigate('/verify-2fa', {
        state: { email: step1Data.email },
      });
    } catch (err) {
      // Витягуємо конкретну помилку з сервера, якщо вона є
      const serverErrors = err.response?.data;
      if (serverErrors) {
        // Якщо сервер повернув об'єкт з помилками полів, виведемо першу ліпшу
        const firstErrorField = Object.keys(serverErrors)[0];
        const message = `${firstErrorField}: ${serverErrors[firstErrorField][0]}`;
        toast.error(message);
      } else {
        toast.error(err.message || 'Registration failed');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-wrapper">
      <div className="register-container">
        <button className="back-btn" onClick={() => navigate('/register')}>
          ←
        </button>

        <div className="logo">
          <img src={Logo} alt="Innovators Lab" />
        </div>

        <h2>Create An Account and Sign Up</h2>

        <div className="avatar-upload" onClick={handleAvatarClick}>
          {avatarPreview ? (
            <img src={avatarPreview} alt="Avatar" className="avatar-preview" />
          ) : (
            <div className="avatar-placeholder">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#999" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" />
                <circle cx="12" cy="13" r="4" />
              </svg>
            </div>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleAvatarChange}
            style={{ display: 'none' }}
          />
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <div className="field-group">
            <label className={touched.firstName && errors.firstName ? 'label-error' : ''}>
              Your Name
            </label>
            <input
              type="text"
              placeholder="Enter your name"
              value={form.firstName}
              onChange={handleChange('firstName')}
              onBlur={handleBlur('firstName')}
              className={touched.firstName && errors.firstName ? 'input-error-border' : ''}
            />
            {touched.firstName && errors.firstName && (
              <span className="field-error">{errors.firstName}</span>
            )}
          </div>

          <div className="field-group">
            <label className={touched.lastName && errors.lastName ? 'label-error' : ''}>
              Your Last Name
            </label>
            <input
              type="text"
              placeholder="Enter your last name"
              value={form.lastName}
              onChange={handleChange('lastName')}
              onBlur={handleBlur('lastName')}
              className={touched.lastName && errors.lastName ? 'input-error-border' : ''}
            />
            {touched.lastName && errors.lastName && (
              <span className="field-error">{errors.lastName}</span>
            )}
          </div>

          <div className="field-group">
            <label className={touched.dateOfBirth && errors.dateOfBirth ? 'label-error' : ''}>
              Date of Birth
            </label>
            <input
              type="date"
              placeholder="Your Birthday (dd-mm-yyyy)"
              value={form.dateOfBirth}
              onChange={handleChange('dateOfBirth')}
              onBlur={handleBlur('dateOfBirth')}
              className={`date-input ${touched.dateOfBirth && errors.dateOfBirth ? 'input-error-border' : ''}`}
            />
            {touched.dateOfBirth && errors.dateOfBirth && (
              <span className="field-error">{errors.dateOfBirth}</span>
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
