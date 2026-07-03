import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ControleurLayout from '../../components/ControleurLayout';
import api from '../../services/api';
import { mockRapports } from '../../services/mockDataControleur';
import './ControleurRapports.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export default function ControleurRapports() {
  const [rapports, setRapports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setRapports(mockRapports.rapports || []);
      setLoading(false);
    } else {
      api.get('/rapports/?ordering=-date_generation').then(r => {
        setRapports(r.data.results || []);
      }).finally(() => setLoading(false));
    }
  }, []);

  const handleDownload = async (rapport) => {
    if (USE_MOCK) { alert('Téléchargement PDF non disponible en mode démo.'); return; }
    setDownloading(rapport.id);
    try {
      const r = await api.get(`/rapports/${rapport.id}/export/`, { responseType: 'blob' });
      const url = URL.createObjectURL(new Blob([r.data], { type: 'application/pdf' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = `${rapport.titre || `rapport-${rapport.id}`}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert('Erreur lors du téléchargement. Le rapport est peut-être encore en cours de génération.');
    } finally {
      setDownloading(null);
    }
  };

  if (loading) return (
    <ControleurLayout pageTitle="Tous les rapports">
      <div className="loading-state">Chargement…</div>
    </ControleurLayout>
  );

  return (
    <ControleurLayout pageTitle="Tous les rapports">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Tous les rapports</h1>
      <p className="page-subtitle">Historique des rapports générés</p>

      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 16 }}>
        <button className="btn btn-blue btn-sm" onClick={() => navigate('/controleur/rapports/generer')}>
          + Générer un rapport
        </button>
      </div>

      <div className="rapports-list" style={{ marginTop: 16 }}>
        {rapports.length === 0 && (
          <div className="empty-state">Aucun rapport généré pour le moment.</div>
        )}
        {rapports.map(r => (
          <div key={r.id} className="rapport-row card">
            <div className="rapport-row-left">
              <div className="rapport-icon">📄</div>
              <div>
                <div className="rapport-titre">{r.titre}</div>
                <div className="rapport-meta">
                  {r.media_nom || 'Rapport global'} · du {r.periode_debut} au {r.periode_fin}
                </div>
                <div className="rapport-date text-muted">
                  Généré le {formatDate(r.date_generation)} par {r.genere_par_nom}
                </div>
              </div>
            </div>
            <div className="rapport-row-right">
              <span className={`badge ${r.statut === 'pret' ? 'badge-actif' : r.statut === 'erreur' ? 'badge-inactif' : 'badge-inactif'}`}>
                {r.statut === 'pret' ? '• Prêt' : r.statut === 'erreur' ? '✗ Erreur' : '⏳ En cours'}
              </span>
              {r.statut === 'pret' && (
                <button
                  className="btn btn-secondary btn-sm"
                  onClick={() => handleDownload(r)}
                  disabled={downloading === r.id}
                >
                  {downloading === r.id ? '…' : '↓ PDF'}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </ControleurLayout>
  );
}