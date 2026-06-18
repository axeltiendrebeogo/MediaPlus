import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ControleurLayout from '../../components/ControleurLayout';
import { mockRapports } from '../../services/mockDataControleur';
import './ControleurRapports.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

export default function ControleurRapports() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) setData(mockRapports);
    // else: api.get('/rapports/').then(r => setData(r.data))
  }, []);

  if (!data) return (
    <ControleurLayout pageTitle="Tous les rapports">
      <div className="loading-state">Chargement…</div>
    </ControleurLayout>
  );

  const { quota, rapports } = data;
  const quotaPct = Math.round((quota.utilise / quota.max) * 100);

  const formatDate = d => new Date(d).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  });

  return (
    <ControleurLayout pageTitle="Tous les rapports">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Tous les rapports</h1>
      <p className="page-subtitle">Historique des rapports générés</p>

      {/* Quota */}
      <div className="card quota-card" style={{ marginTop: 24 }}>
        <div className="quota-header">
          <div>
            <div className="quota-title">Quota de génération</div>
            <div className="quota-sub">{quota.utilise} rapport{quota.utilise > 1 ? 's' : ''} utilisé{quota.utilise > 1 ? 's' : ''} sur {quota.max} max / 4h · Réinitialisation dans {quota.reset_dans}</div>
          </div>
          <button className="btn btn-blue btn-sm" onClick={() => navigate('/controleur/rapports/generer')}>
            + Générer un rapport
          </button>
        </div>
        <div className="quota-bar-track">
          <div className="quota-bar-fill" style={{ width: `${quotaPct}%` }} />
        </div>
        <div className="quota-labels">
          <span>{quota.utilise} utilisé{quota.utilise > 1 ? 's' : ''}</span>
          <span>{quota.max - quota.utilise} restant{quota.max - quota.utilise > 1 ? 's' : ''}</span>
        </div>
      </div>

      {/* Liste rapports */}
      <div className="rapports-list" style={{ marginTop: 20 }}>
        {rapports.map(r => (
          <div key={r.id} className="rapport-row card">
            <div className="rapport-row-left">
              <div className="rapport-icon">📄</div>
              <div>
                <div className="rapport-titre">{r.titre}</div>
                <div className="rapport-meta">
                  {r.medias.join(' · ')} · {r.periode}
                </div>
                <div className="rapport-date text-muted">Généré le {formatDate(r.cree_le)}</div>
              </div>
            </div>
            <div className="rapport-row-right">
              <span className={`badge ${r.statut === 'pret' ? 'badge-actif' : 'badge-inactif'}`}>
                {r.statut === 'pret' ? '• Prêt' : '⏳ En cours'}
              </span>
              {r.statut === 'pret' && (
                <button className="btn btn-secondary btn-sm">
                  ↓ Télécharger
                </button>
              )}
            </div>
          </div>
        ))}

        {rapports.length === 0 && (
          <div className="empty-state">Aucun rapport généré pour le moment.</div>
        )}
      </div>
    </ControleurLayout>
  );
}
