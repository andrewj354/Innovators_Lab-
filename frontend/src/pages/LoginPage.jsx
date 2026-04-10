import React from 'react';
import '../pages/styles/LoginPage.css'; // Підключаємо стилі сторінки
import Input from '../components/Input';   // Беремо наш інпут
import Button from '../components/Button'; // Беремо нашу кнопку

export default function LoginPage() {
  const handleLogin = (e) => {
    e.preventDefault();
    console.log('Вхід...');
  };

  return (
    <div className="login-wrapper">
      <div className="login-container">
        
        <div className="logo">
          <img src="https://via.placeholder.com/80x80.png?text=Logo" alt="Innovators Lab" />
        </div>

        <h2>Sign in to ChatoPotamus</h2>

        <form onSubmit={handleLogin}>
          {/* Використовуємо наш компонент Input */}
          <Input type="email" placeholder="Email" required={true} />
          <Input type="password" placeholder="Password" required={true} />

          {/* Використовуємо наш компонент Button */}
          <Button type="submit" className="btn-login">
            Log in
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