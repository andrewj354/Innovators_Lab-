import { Routes, Route, Navigate } from 'react-router-dom';

import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/registration/RegisterPage';
import RegisterStep2Page from './features/auth/pages/registration/RegisterStep2Page';
import Verify2FA from './features/auth/pages/Verify2FA';
import ForgotPasswordPage from './features/auth/pages/password-reset/ForgotPasswordPage';
import ForgotPasswordSentPage from './features/auth/pages/password-reset/ForgotPasswordSentPage';
import ResetPasswordPage from './features/auth/pages/password-reset/ResetPasswordPage';
import Navbar from "./components/Navbar";

import TournamentListPage from './features/tournaments/pages/TournamentListPage';
import TournamentFormPage from './features/tournaments/pages/TournamentFormPage';
import TournamentPublicPage from './features/tournaments/pages/TournamentPublicPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
     <Navbar user={user} onLogout={handleLogout} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/register/step2" element={<RegisterStep2Page />} />
      <Route path="/verify-2fa" element={<Verify2FA />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/forgot-password/sent" element={<ForgotPasswordSentPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      <Route path="/tournaments" element={<TournamentListPage />} />
      <Route path="/tournaments/new" element={<TournamentFormPage />} />
      <Route path="/tournaments/:id" element={<TournamentPublicPage />} />
      <Route path="/tournaments/:id/edit" element={<TournamentFormPage />} />
    </Routes>
  );
}

export default App;