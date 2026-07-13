import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';

const ROLES = [
  { key: 'admin', label: 'Admin', sub: 'Gestion' },
  { key: 'gestionnaire', label: 'Gestionnaire', sub: 'Mon média' },
  { key: 'controleur', label: 'Contrôleur', sub: 'Tous médias' },
];

const REDIRECT = {
  admin: '/admin',
  gestionnaire: '/gestionnaire',
  controleur: '/controleur',
};

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [role, setRole] = useState('gestionnaire');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const user = await login(email, password, role);
      navigate(REDIRECT[user.role] || '/');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Identifiants incorrects. Veuillez réessayer.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-bg">
      <div className="login-card">
        {/* Brand */}
        <div className="login-brand">
          <h1 className="login-brand-name">FasoMedia Insights</h1>
          <p className="login-brand-sub">Plateforme d'analyse d'audience</p>
        </div>

        {/* Form header */}
        <div className="login-header">
          <h2 className="login-title">Connexion à votre espace</h2>
          <p className="login-subtitle">Sélectionnez votre rôle pour accéder à la plateforme</p>
        </div>

        {/* Role selector */}
        <div className="role-selector">
          {ROLES.map(r => (
            <button
              key={r.key}
              type="button"
              className={`role-btn${role === r.key ? ' active' : ''}`}
              onClick={() => setRole(r.key)}
            >
              <span className="role-btn-label">{r.label}</span>
              <span className="role-btn-sub">{r.sub}</span>
            </button>
          ))}
        </div>

        {/* Form */}
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Adresse email</label>
            <input
              className="form-input"
              type="email"
              placeholder="votre@email.bf"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Mot de passe</label>
            <input
              className="form-input"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={e => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
            <div className="login-forgot">
              <button type="button" className="forgot-link">Mot de passe oublié ?</button>
            </div>
          </div>

          {error && <div className="login-error">{error}</div>}

          <button
            type="submit"
            className="btn btn-primary btn-full btn-lg"
            disabled={loading}
          >
            {loading ? 'Connexion…' : 'Se connecter'}
          </button>

          <p className="login-note">Accès réservé aux utilisateurs autorisés</p>
        </form>
      </div>
    </div>
  );
}
