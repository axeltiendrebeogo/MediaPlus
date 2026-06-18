import React, { useState, useEffect } from 'react';
import api from '../../../services/api';
import { mockMedias } from '../../../services/mockData';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

export default function ModalCreerCompte({ onClose, onCreated }) {
  const [form, setForm] = useState({ nom: '', email: '', role: 'controleur', media_id: '', password: '' });
  const [medias, setMedias] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (USE_MOCK) {
      setMedias(mockMedias.results);
    } else {
      api.get('/medias/').then(r => setMedias(r.data.results)).catch(() => {});
    }
  }, []);

  const set = (k, v) => setForm(prev => ({ ...prev, [k]: v }));

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const body = { ...form };
      if (form.role !== 'gestionnaire') delete body.media_id;
      if (!body.password) {
        body.password = Math.random().toString(36).slice(-10) + 'A1!';
      }
      if (USE_MOCK) {
        const mock = {
          id: Date.now(), ...form,
          media_nom: medias.find(m => m.id === Number(form.media_id))?.nom || null,
          date_creation: new Date().toISOString(), is_active: true,
        };
        onCreated(mock);
        return;
      }
      const res = await api.post('/users/', body);
      onCreated(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Une erreur est survenue.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <h2 className="modal-title">Créer un compte utilisateur</h2>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14, marginTop: 16 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div className="form-group">
              <label className="form-label">Nom complet</label>
              <input className="form-input" placeholder="Prénom Nom" value={form.nom} onChange={e => set('nom', e.target.value)} required />
            </div>
            <div className="form-group">
              <label className="form-label">Adresse email</label>
              <input className="form-input" type="email" placeholder="email@media.bf" value={form.email} onChange={e => set('email', e.target.value)} required />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div className="form-group">
              <label className="form-label">Rôle</label>
              <select className="form-select" value={form.role} onChange={e => set('role', e.target.value)}>
                <option value="gestionnaire">Gestionnaire</option>
                <option value="controleur">Contrôleur</option>
              </select>
            </div>
            {form.role === 'gestionnaire' && (
              <div className="form-group">
                <label className="form-label">Média affecté</label>
                <select className="form-select" value={form.media_id} onChange={e => set('media_id', e.target.value)} required>
                  <option value="">Sélectionner…</option>
                  {medias.map(m => (
                    <option key={m.id} value={m.id}>{m.nom}</option>
                  ))}
                </select>
              </div>
            )}
          </div>

          <div className="form-group">
            <label className="form-label">Mot de passe temporaire</label>
            <input className="form-input" type="text" placeholder="Sera envoyé par email (laisser vide pour auto-génération)" value={form.password} onChange={e => set('password', e.target.value)} />
          </div>

          {error && <div className="login-error">{error}</div>}

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Annuler</button>
            <button type="submit" className="btn btn-blue" disabled={loading}>
              {loading ? 'Création…' : 'Créer le compte'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
