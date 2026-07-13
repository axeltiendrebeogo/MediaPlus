import React, { useState, useEffect } from 'react';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import api from '../../services/api';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const PERIODES = [
  { label: '7 jours',     jours: 7   },
  { label: '30 jours',    jours: 30  },
  { label: '3 mois',      jours: 90  },
  { label: 'Cette année', jours: 365 },
];

function formatDuree(s) {
  const sec = Math.round(s || 0);
  if (sec >= 3600) return `${Math.floor(sec/3600)}h ${Math.floor((sec%3600)/60)}m`;
  return `${Math.floor(sec/60)}m ${(sec%60).toString().padStart(2,'0')}s`;
}

function couleurCompletion(pct) {
  if (pct >= 70) return '#16a34a';
  if (pct >= 40) return '#f59e0b';
  return '#ef4444';
}

function KPICard({ label, value, sub }) {
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {sub && <div className="kpi-sub">{sub}</div>}
    </div>
  );
}

const MOCK_DATA = {
  kpi: { total_contenus: 12, total_lectures: 3240, duree_moy_ecoute: 872, completion_moy: 61 },
  contenus: [
    { page_id: 1, titre: 'JT 20h — édition du jour', type: 'video', duree_contenu: 1800, nb_lectures: 1240, duree_moy_ecoute: 1100, taux_completion: 61 },
    { page_id: 2, titre: 'Podcast : actualités de la semaine', type: 'audio', duree_contenu: 2700, nb_lectures: 890, duree_moy_ecoute: 1620, taux_completion: 60 },
    { page_id: 3, titre: 'Reportage : vie quotidienne', type: 'video', duree_contenu: 900, nb_lectures: 640, duree_moy_ecoute: 765, taux_completion: 85 },
    { page_id: 4, titre: 'Interview exclusive du ministre', type: 'video', duree_contenu: 1200, nb_lectures: 310, duree_moy_ecoute: 360, taux_completion: 30 },
  ],
};

export default function GestionnaireAudio() {
  const [data, setData] = useState(null);
  const [periode, setPeriode] = useState(30);

  useEffect(() => {
    if (USE_MOCK) { setData(MOCK_DATA); return; }
    api.get(`/stats/audio-video/?period=${periode}`).then(r => setData(r.data));
  }, [periode]);

  if (!data) return (
    <GestionnaireLayout pageTitle="Audio / Vidéo">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  const { kpi, contenus } = data;

  return (
    <GestionnaireLayout pageTitle="Audio / Vidéo">
      <div className="page-eyebrow">MON MÉDIA</div>
      <h1 className="page-title">Contenus Audio &amp; Vidéo</h1>
      <p className="page-subtitle">Performance des contenus multimédias</p>

      {/* Sélecteur de période */}
      <div className="periode-selector" style={{ marginTop: 20 }}>
        {PERIODES.map(p => (
          <button
            key={p.jours}
            className={`periode-btn${periode === p.jours ? ' active' : ''}`}
            onClick={() => setPeriode(p.jours)}
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* KPI */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4,1fr)', marginTop: 20 }}>
        <KPICard label="CONTENUS TOTAL"     value={kpi.total_contenus} />
        <KPICard label="LECTURES / VISIONS" value={kpi.total_lectures.toLocaleString('fr-FR')} />
        <KPICard label="DURÉE MOY. ÉCOUTE"  value={formatDuree(kpi.duree_moy_ecoute)} />
        <KPICard label="COMPLÉTION MOY."    value={`${kpi.completion_moy}%`} sub={kpi.completion_moy >= 70 ? '✓ Bonne rétention' : kpi.completion_moy >= 40 ? 'Rétention moyenne' : '⚠ Faible rétention'} />
      </div>

      {/* G6 — Taux de complétion par contenu */}
      {contenus.length === 0 ? (
        <div className="card empty-state" style={{ marginTop: 20 }}>
          Aucun contenu audio ou vidéo trouvé sur ce média pour la période sélectionnée.
        </div>
      ) : (
        <div className="card" style={{ marginTop: 20, padding: 20 }}>
          <div className="chart-title" style={{ marginBottom: 16 }}>
            Taux de complétion par contenu (G6)
          </div>

          {/* Graphique en barres horizontales CSS */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {contenus.map(c => (
              <div key={c.page_id}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: 13 }}>
                  <div>
                    <span style={{ fontWeight: 600 }}>{c.titre.length > 45 ? c.titre.slice(0, 45) + '…' : c.titre}</span>
                    <span style={{ marginLeft: 8, fontSize: 11, padding: '2px 8px', borderRadius: 12,
                      background: c.type === 'video' ? '#dbeafe' : '#fce7f3',
                      color: c.type === 'video' ? '#1d4ed8' : '#9d174d' }}>
                      {c.type === 'video' ? '▶ Vidéo' : '♪ Audio'}
                    </span>
                  </div>
                  <span style={{ fontWeight: 700, color: couleurCompletion(c.taux_completion) }}>
                    {c.taux_completion}%
                  </span>
                </div>
                <div style={{ background: '#e5e7eb', borderRadius: 6, height: 10, overflow: 'hidden' }}>
                  <div style={{
                    width: `${c.taux_completion}%`,
                    height: '100%',
                    background: couleurCompletion(c.taux_completion),
                    borderRadius: 6,
                    transition: 'width 0.5s ease',
                  }} />
                </div>
                <div style={{ display: 'flex', gap: 20, marginTop: 5, fontSize: 12, color: '#6b7280' }}>
                  <span>📺 {c.nb_lectures.toLocaleString('fr-FR')} lectures</span>
                  <span>⏱ Durée moy. : {formatDuree(c.duree_moy_ecoute)}</span>
                  <span>⏳ Durée totale : {formatDuree(c.duree_contenu)}</span>
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginTop: 20, fontSize: 12, color: '#9ca3af', borderTop: '1px solid #f1f5f9', paddingTop: 12 }}>
            🟢 ≥ 70% bonne rétention · 🟡 40–70% rétention moyenne · 🔴 &lt; 40% abandon prématuré
          </div>
        </div>
      )}

      {/* Tableau détaillé */}
      {contenus.length > 0 && (
        <div className="card" style={{ marginTop: 16 }}>
          <div className="chart-title" style={{ marginBottom: 12 }}>Détail par contenu</div>
          <table className="table">
            <thead>
              <tr>
                <th>CONTENU</th>
                <th>TYPE</th>
                <th>LECTURES</th>
                <th>DURÉE TOTALE</th>
                <th>DURÉE MOY. ÉCOUTE</th>
                <th>COMPLÉTION</th>
              </tr>
            </thead>
            <tbody>
              {contenus.map(c => (
                <tr key={c.page_id}>
                  <td className="font-medium">{c.titre.length > 40 ? c.titre.slice(0, 40) + '…' : c.titre}</td>
                  <td>
                    <span style={{ fontSize: 11, padding: '2px 8px', borderRadius: 12,
                      background: c.type === 'video' ? '#dbeafe' : '#fce7f3',
                      color: c.type === 'video' ? '#1d4ed8' : '#9d174d' }}>
                      {c.type === 'video' ? '▶ Vidéo' : '♪ Audio'}
                    </span>
                  </td>
                  <td>{c.nb_lectures.toLocaleString('fr-FR')}</td>
                  <td>{formatDuree(c.duree_contenu)}</td>
                  <td>{formatDuree(c.duree_moy_ecoute)}</td>
                  <td>
                    <span style={{ fontWeight: 700, color: couleurCompletion(c.taux_completion) }}>
                      {c.taux_completion}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </GestionnaireLayout>
  );
}