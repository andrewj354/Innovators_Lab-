import { Routes, Route, Navigate } from 'react-router-dom';

// Auth pages
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/registration/RegisterPage';
import RegisterStep2Page from './features/auth/pages/registration/RegisterStep2Page';
import Verify2FA from './features/auth/pages/Verify2FA';
import ForgotPasswordPage from './features/auth/pages/password-reset/ForgotPasswordPage';
import ForgotPasswordSentPage from './features/auth/pages/password-reset/ForgotPasswordSentPage';
import ResetPasswordPage from './features/auth/pages/password-reset/ResetPasswordPage';

// Dashboard
import DashboardPage from './features/dashboard/pages/DashboardPage';

// Tournament pages
import TournamentListPage from './features/tournaments/pages/TournamentListPage';
import TournamentFormPage from './features/tournaments/pages/TournamentFormPage';
import TournamentPublicPage from './features/tournaments/pages/TournamentPublicPage';

// Task pages
import TaskListPage from './features/tasks/pages/TaskListPage';
import TaskDetailPage from './features/tasks/pages/TaskDetailPage';

// Submission pages
import SubmissionFormPage from './features/submissions/pages/SubmissionFormPage';
import SubmissionDetailPage from './features/submissions/pages/SubmissionDetailPage';
import SubmissionsListPage from './features/submissions/pages/SubmissionsListPage';

// Jury pages
import JuryDashboard from './features/assessment/pages/JuryDashboard';
import JuryAssignmentPage from './features/assessment/pages/JuryAssignmentPage';

// Leaderboard pages
import LeaderboardPage from './features/leaderboard/pages/LeaderboardPage';

// Profile & Settings pages
import ProfilePage from './features/profile/pages/ProfilePage';
import SettingsPage from './features/settings/pages/SettingsPage';

// Protected Route
import ProtectedRoute from './shared/components/ProtectedRoute';

function App() {
  return (
    <Routes>
      {/* Auth routes */}
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/register/step2" element={<RegisterStep2Page />} />
      <Route path="/verify-2fa" element={<Verify2FA />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/forgot-password/sent" element={<ForgotPasswordSentPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      {/* Dashboard route */}
      <Route 
        path="/dashboard" 
        element={<DashboardPage />}
      />

      {/* Tournament routes */}
      <Route path="/tournaments" element={<TournamentListPage />} />
      <Route path="/tournaments/new" element={<TournamentFormPage />} />
      <Route path="/tournaments/:id" element={<TournamentPublicPage />} />
      <Route path="/tournaments/:id/edit" element={<TournamentFormPage />} />

      {/* Task routes */}
      <Route path="/tournaments/:tournamentId/tasks" element={<TaskListPage />} />
      <Route path="/tasks/:taskId" element={<TaskDetailPage />} />

      {/* Submission routes */}
      <Route path="/submissions/new" element={<SubmissionFormPage />} />
      <Route path="/submissions/:submissionId" element={<SubmissionDetailPage />} />
      <Route path="/submissions" element={<SubmissionsListPage />} />

      {/* Jury routes */}
      <Route path="/jury/dashboard" element={<JuryDashboard />} />
      <Route path="/jury/assignments" element={<JuryDashboard />} />
      <Route path="/jury/assignments/:assignmentId" element={<JuryAssignmentPage />} />

      {/* Leaderboard routes */}
      <Route path="/tournaments/:tournamentId/leaderboard" element={<LeaderboardPage />} />

      {/* Profile & Settings routes */}
      <Route 
        path="/profile" 
        element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        } 
      />
      <Route 
        path="/settings" 
        element={
          <ProtectedRoute>
            <SettingsPage />
          </ProtectedRoute>
        } 
      />

      {/* Fallback route */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}

export default App;