import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ControleurLayout from '../../components/ControleurLayout';
import api from '../../services/api';
import { mockControleurDashboard } from '../../services/mockDataControleur';
import './ControleurMedias.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';
const PALETTE = ['#2563eb', '#16a34a', '#7c3aed', '#f59e0b', '#ef4444', '#06b6d4'];

function formatDuree(s) {
  const sec = Math.round(s || 0);
  return `${Math.floor(sec / 60)}m ${(sec % 60).toString().padStart(2, '0')}s`;
}

export default function ControleurMedias() {
  const [medias, setMedias] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setMedias(mockControleurDashboard.tableau.map((m, i) => ({ ...m, color: PALETTE[i % PALETTE.length] })));
    } else {
      // Charge la liste des médias + stats globales en parallèle, puis fusionne
      Promise.all([
        api.get('/medias/'),
        api.get('/stats/global/?period=30'),
      ]).then(([mediasRes, statsRes]) => {
        const statsParId = {};
        (statsRes.data.par_media || []).forEach(m => { statsParId[m.media_id] = m; });

        const merged = mediasRes.data.results.map((m, i) => {
          const s = statsParId[m.id] || {};
          return {
            id: m.id,
            nom: m.nom,
            type_media: m.type_media,
            statut: m.statut,
            gestionnaire_nom: m.gestionnaire_nom,
            visiteurs: s.visiteurs || 0,
            pages_vues: s.pages_vues || 0,
            duree_moy: formatDuree(s.duree_moyenne || 0),
            scroll_moy: s.scroll_moyen || 0,
            color: PALETTE[i % PALETTE.length],
          };
        });
        setMedias(merged);
      });
    }
  }, []);

  return (
    <ControleurLayout pageTitle="Tous les médias">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Tous les médias</h1>
      <p className="page-subtitle">Performances individuelles · 30 derniers jours</p>

      <div className="medias-list" style={{ marginTop: 24 }}>
        {medias.map(m => (
          <div key={m.id} className="media-row-card card">
            <div className="media-row-left">
              <div className="media-color-dot" style={{ background: m.color }} />
              <div>
                <div className="media-row-name">{m.nom}</div>
                <span className={`badge badge-${m.type_media}`}>
                  {m.type_media.charAt(0).toUpperCase() + m.type_media.slice(1)}
                </span>
              </div>
            </div>

            <div className="media-row-stats">
              <div className="media-row-stat">
                <div className="media-row-stat-label">Visiteurs</div>
                <div className="media-row-stat-val">{m.visiteurs.toLocaleString('fr-FR')}</div>
              </div>
              <div className="media-row-stat">
                <div className="media-row-stat-label">Pages vues</div>
                <div className="media-row-stat-val">{m.pages_vues.toLocaleString('fr-FR')}</div>
              </div>
              <div className="media-row-stat">
                <div className="media-row-stat-label">Durée moy.</div>
                <div className="media-row-stat-val">{m.duree_moy}</div>
              </div>
              <div className="media-row-stat">
                <div className="media-row-stat-label">Scroll moy.</div>
                <div className="media-row-stat-val">{m.scroll_moy}%</div>
              </div>
              <div className="media-row-stat" style={{ minWidth: 120 }}>
                <div className="media-row-stat-label">Progression scroll</div>
                <div className="scroll-bar-track">
                  <div className="scroll-bar-fill" style={{ width: `${m.scroll_moy}%`, background: m.color }} />
                </div>
              </div>
            </div>

            <div className="media-row-actions">
              <button
                className="btn btn-secondary btn-sm"
                onClick={() => navigate(`/controleur/rapports/generer?media=${m.id}`)}
              >
                Rapport
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="ctrl-actions-bar" style={{ marginTop: 20 }}>
        <button className="btn btn-secondary" onClick={() => navigate('/controleur/comparaison')}>
          ⇄ Comparer des médias
        </button>
        <button className="btn btn-secondary" onClick={() => navigate('/controleur/rapports/generer')}>
          Générer un rapport global
        </button>
      </div>
    </ControleurLayout>
  );
}