import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

// Public
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';

// Admin
import AdminDashboard from './pages/admin/AdminDashboard';
import AdminMedias from './pages/admin/AdminMedias';
import AdminComptes from './pages/admin/AdminComptes';

// Contrôleur
import ControleurDashboard from './pages/controleur/ControleurDashboard';
import ControleurMedias from './pages/controleur/ControleurMedias';
import ControleurComparaison from './pages/controleur/ControleurComparaison';
import ControleurAffectations from './pages/controleur/ControleurAffectations';
import ControleurRapports from './pages/controleur/ControleurRapports';
import ControleurGenererRapport from './pages/controleur/ControleurGenererRapport';

// Gestionnaire
import GestionnaireDashboard from './pages/gestionnaire/GestionnaireDashboard';
import GestionnairePages from './pages/gestionnaire/GestionnairePages';
import GestionnaireAnalysePage from './pages/gestionnaire/GestionnaireAnalysePage';
import GestionnaireRapports from './pages/gestionnaire/GestionnaireRapports';

function LoginGuard() {
  const { user, loading } = useAuth();
  if (loading) return null;
  if (user) {
    const redirect = { admin: '/admin', gestionnaire: '/gestionnaire', controleur: '/controleur' };
    return <Navigate to={redirect[user.role] || '/'} replace />;
  }
  return <LoginPage />;
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* ── Public ── */}
          <Route path="/" element={<HomePage />} />
          <Route path="/connexion" element={<LoginGuard />} />

          {/* ── Admin ── */}
          <Route path="/admin"         element={<ProtectedRoute roles={['admin']}><AdminDashboard /></ProtectedRoute>} />
          <Route path="/admin/medias"  element={<ProtectedRoute roles={['admin']}><AdminMedias /></ProtectedRoute>} />
          <Route path="/admin/comptes" element={<ProtectedRoute roles={['admin']}><AdminComptes /></ProtectedRoute>} />

          {/* ── Contrôleur ── */}
          <Route path="/controleur"                  element={<ProtectedRoute roles={['controleur']}><ControleurDashboard /></ProtectedRoute>} />
          <Route path="/controleur/medias"           element={<ProtectedRoute roles={['controleur']}><ControleurMedias /></ProtectedRoute>} />
          <Route path="/controleur/comparaison"      element={<ProtectedRoute roles={['controleur']}><ControleurComparaison /></ProtectedRoute>} />
          <Route path="/controleur/affectations"     element={<ProtectedRoute roles={['controleur']}><ControleurAffectations /></ProtectedRoute>} />
          <Route path="/controleur/rapports"         element={<ProtectedRoute roles={['controleur']}><ControleurRapports /></ProtectedRoute>} />
          <Route path="/controleur/rapports/generer" element={<ProtectedRoute roles={['controleur']}><ControleurGenererRapport /></ProtectedRoute>} />

          {/* ── Gestionnaire ── */}
          <Route path="/gestionnaire"              element={<ProtectedRoute roles={['gestionnaire']}><GestionnaireDashboard /></ProtectedRoute>} />
          <Route path="/gestionnaire/pages"        element={<ProtectedRoute roles={['gestionnaire']}><GestionnairePages /></ProtectedRoute>} />
          <Route path="/gestionnaire/pages/:id"    element={<ProtectedRoute roles={['gestionnaire']}><GestionnaireAnalysePage /></ProtectedRoute>} />
          <Route path="/gestionnaire/rapports"     element={<ProtectedRoute roles={['gestionnaire']}><GestionnaireRapports /></ProtectedRoute>} />

          {/* ── 404 ── */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
