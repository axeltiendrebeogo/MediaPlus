import React from 'react';

export default function ModalConfirmReaffectation({ media, ancienGestionnaire, nouveauGestionnaire, onConfirm, onClose }) {
  return (
    <div className="modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <h2 className="modal-title">Confirmer la réaffectation</h2>

        <div style={{
          background: '#f9fafb',
          border: '1px solid var(--color-border)',
          borderRadius: 'var(--radius-md)',
          padding: '14px',
          marginTop: 16,
          fontSize: 14,
          lineHeight: 1.6,
        }}>
          Vous êtes sur le point de réaffecter <strong>{media.nom}</strong> à <strong>{nouveauGestionnaire}</strong>.
          {ancienGestionnaire && (
            <> <br />{ancienGestionnaire} n'aura plus accès au tableau de bord de ce média.</>
          )}
        </div>

        <div className="modal-actions">
          <button className="btn btn-secondary" onClick={onClose}>Annuler</button>
          <button className="btn btn-blue" onClick={onConfirm}>Confirmer la réaffectation</button>
        </div>
      </div>
    </div>
  );
}
