import { Routes, Route, Navigate } from 'react-router-dom';

// Auth pages
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';
import Verify2FA from './features/auth/pages/Verify2FA';

// Tournament pages
import TournamentListPage from './features/tournaments/pages/TournamentListPage';
import TournamentFormPage from './features/tournaments/pages/TournamentFormPage';
import TournamentPublicPage from './features/tournaments/pages/TournamentPublicPage';

function App() {
  return (
    <Routes>
      {/* Redirect root to login */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* Auth */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/verify-2fa" element={<Verify2FA />} />

      {/* Tournaments */}
      <Route path="/tournaments" element={<TournamentListPage />} />
      <Route path="/tournaments/new" element={<TournamentFormPage />} />
      <Route path="/tournaments/:id" element={<TournamentPublicPage />} />
      <Route path="/tournaments/:id/edit" element={<TournamentFormPage />} />
    </Routes>
  );
}

export default App;