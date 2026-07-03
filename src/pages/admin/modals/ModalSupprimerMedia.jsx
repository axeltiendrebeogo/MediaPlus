import React, { useState } from 'react';
import api from '../../../services/api';
import './ModalSupprimerMedia.css';

export default function ModalSupprimerMedia({ media, onClose, onDeleted }) {
  const [mode, setMode] = useState('soft');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDelete = async () => {
    setError('');
    setLoading(true);
    try {
      if (process.env.REACT_APP_USE_MOCK === 'true') {
        onDeleted(media.id);
        return;
      }
      await api.delete(`/medias/${media.id}/?mode=${mode}`);
      onDeleted(media.id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Une erreur est survenue.');
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal modal-delete">
        <div className="modal-delete-icon">⚠️</div>
        <h2 className="modal-title">Supprimer {media.nom} ?</h2>
        <p className="modal-desc">
          Cette action est irréversible. Choisissez ce qu'il advient des données associées.
        </p>

        <div className="delete-options">
          <label className={`delete-option${mode === 'soft' ? ' selected' : ''}`}>
            <input
              type="radio" name="mode" value="soft"
              checked={mode === 'soft'} onChange={() => setMode('soft')}
            />
            <div className="delete-option-content">
              <div className="delete-option-title">Conserver les données (soft delete)</div>
              <div className="delete-option-desc">
                Le média est archivé. Pages, visiteurs, événements et rapports sont conservés.
              </div>
            </div>
          </label>

          <label className={`delete-option${mode === 'hard' ? ' selected' : ''}`}>
            <input
              type="radio" name="mode" value="hard"
              checked={mode === 'hard'} onChange={() => setMode('hard')}
            />
            <div className="delete-option-content">
              <div className="delete-option-title">Tout supprimer (hard delete)</div>
              <div className="delete-option-desc">
                Le média ET toutes ses données associées sont <strong>définitivement supprimés</strong>.
              </div>
            </div>
          </label>
        </div>

        {error && <div className="login-error" style={{ marginTop: 12 }}>{error}</div>}

        <div className="modal-actions">
          <button className="btn btn-secondary" onClick={onClose}>Annuler</button>
          <button className="btn btn-danger" onClick={handleDelete} disabled={loading}>
            {loading ? 'Suppression…' : 'Supprimer'}
          </button>
        </div>
      </div>
    </div>
  );
}
