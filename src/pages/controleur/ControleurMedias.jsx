import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ControleurLayout from '../../components/ControleurLayout';
import { mockControleurDashboard } from '../../services/mockDataControleur';
import './ControleurMedias.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const MEDIA_COLORS = { 1: '#2563eb', 2: '#16a34a', 3: '#7c3aed', 4: '#f59e0b' };

export default function ControleurMedias() {
  const [medias, setMedias] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) setMedias(mockControleurDashboard.tableau);
    // else: api.get('/medias/?include_stats=true').then(r => setMedias(r.data.results))
  }, []);

  return (
    <ControleurLayout pageTitle="Tous les médias">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Tous les médias</h1>
      <p className="page-subtitle">Performances individuelles · Mars 2025</p>

      <div className="medias-list" style={{ marginTop: 24 }}>
        {medias.map((m, i) => (
          <div key={m.id} className="media-row-card card">
            <div className="media-row-left">
              <div className="media-color-dot" style={{ background: MEDIA_COLORS[m.id] || '#6b7280' }} />
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
                  <div
                    className="scroll-bar-fill"
                    style={{ width: `${m.scroll_moy}%`, background: MEDIA_COLORS[m.id] || '#6b7280' }}
                  />
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
