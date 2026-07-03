import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

export default function ControleurPlaceholder() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/connexion');
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 16, background: '#f5f5f4' }}>
      <div style={{ background: 'white', border: '1px solid #e5e7eb', borderRadius: 12, padding: 40, textAlign: 'center', maxWidth: 400 }}>
        <div style={{ fontSize: 32, marginBottom: 12 }}>🎛️</div>
        <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8 }}>Espace Contrôleur</h2>
        <p style={{ color: '#6b7280', fontSize: 14, marginBottom: 20 }}>
          Bienvenue, <strong>{user?.nom}</strong>. Cette section sera développée prochainement.
        </p>
        <button
          onClick={handleLogout}
          style={{ padding: '8px 20px', border: '1.5px solid #e5e7eb', borderRadius: 8, background: 'white', cursor: 'pointer', fontSize: 14 }}
        >
          Se déconnecter
        </button>
      </div>
    </div>
  );
}
