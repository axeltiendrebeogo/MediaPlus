import React, { useState } from 'react';
import api from '../../../services/api';

const TYPE_OPTIONS = ['presse', 'television', 'radio', 'web'];

export default function ModalAjouterMedia({ onClose, onCreated }) {
  const [form, setForm] = useState({ nom: '', url: '', type_media: 'presse' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k, v) => setForm(prev => ({ ...prev, [k]: v }));

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (process.env.REACT_APP_USE_MOCK === 'true') {
        const mock = { id: Date.now(), ...form, statut: 'actif', gestionnaire_id: null, gestionnaire_nom: null, visiteurs_mois: 0, pages_indexees: 0 };
        onCreated(mock);
        return;
      }
      const res = await api.post('/medias/', form);
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
        <h2 className="modal-title">Ajouter un média</h2>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div className="form-group">
            <label className="form-label">Nom du média</label>
            <input className="form-input" placeholder="ex. RTB Online" value={form.nom} onChange={e => set('nom', e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label">URL principale</label>
            <input className="form-input" placeholder="ex. rtb.bf" value={form.url} onChange={e => set('url', e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label">Type de média</label>
            <select className="form-select" value={form.type_media} onChange={e => set('type_media', e.target.value)}>
              {TYPE_OPTIONS.map(t => (
                <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>
              ))}
            </select>
          </div>
          {error && <div className="login-error">{error}</div>}
          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Annuler</button>
            <button type="submit" className="btn btn-blue" disabled={loading}>
              {loading ? 'Création…' : 'Ajouter le média'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
