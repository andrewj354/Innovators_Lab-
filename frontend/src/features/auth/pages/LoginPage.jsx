import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import '../styles/LoginPage.css';
import Input from '../../../shared/components/Input';
import Button from '../../../shared/components/Button';
import { login } from '../api/authApi';
import { useAuth } from '../../../shared/context/AuthContext';
import Logo from '../../../assets/Logo.svg';

export default function LoginPage() {
  // This runs on component mount - should always execute
  window.loginPageMounted = true;
  
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (e) => {
    setForm((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    window.loginAttempt = (window.loginAttempt || 0) + 1;
    console.log('[LoginPage] handleLogin called, attempt #' + window.loginAttempt);

    if (!form.email || !form.password) {
      toast.warn('Email and password are required');
      return;
    }

    setLoading(true);
    try {
      const response = await login({ email: form.email, password: form.password });
      console.log('[LoginPage] Login response:', response);
      console.log('[LoginPage] User data:', response.user);
      console.log('[LoginPage] Tokens:', {
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken')
      });
      
      console.log('[LoginPage] Response received:', response);
      authLogin(response.user);
      console.log('[LoginPage] Auth context updated');
      
      // Log something to window object to detect execution
      window.lastLoginTime = new Date().toISOString();
      
      toast.success('Welcome back!');
      
      // Try navigating using navigate() from react-router
      console.log('[LoginPage] Attempting navigation via navigate() hook');
      navigate('/dashboard');
    } catch (err) {
      const message = err.response?.data?.message ?? err.message ?? 'Login failed';
      toast.error(message);
      console.error('[LoginPage] Login error:', err);
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

        <h2>Sign in to Innovators Lab</h2>

        <form onSubmit={handleLogin}>
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

          <Button type="submit" className="btn-login" disabled={loading}>
            {loading ? 'Signing in...' : 'Log in'}
          </Button>
        </form>

        <div className="links-text">
          Forgot password? Don't worry <a href="/forgot-password">reset it here!</a>
        </div>

        <div className="links-text">
          Don't have an account ? <a href="/register" className="bold">Sign Up.</a>
        </div>

        <Button className="btn-google">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
          </svg>
          Log In with Google
        </Button>

      </div>
    </div>
  );
}
