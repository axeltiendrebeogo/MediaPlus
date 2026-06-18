import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function NotFoundPage() {
  const navigate = useNavigate();
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f5f4' }}>
      <div style={{ textAlign: 'center' }}>
        <div style={{ fontSize: 48, fontWeight: 700, color: '#2563eb', marginBottom: 8 }}>404</div>
        <h1 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8 }}>Page introuvable</h1>
        <p style={{ color: '#6b7280', marginBottom: 20 }}>Cette page n'existe pas ou vous n'y avez pas accès.</p>
        <button
          className="btn btn-secondary"
          onClick={() => navigate('/')}
          style={{ padding: '8px 20px', border: '1.5px solid #e5e7eb', borderRadius: 8, background: 'white', cursor: 'pointer', fontSize: 14 }}
        >
          Retour à l'accueil
        </button>
      </div>
    </div>
  );
}
