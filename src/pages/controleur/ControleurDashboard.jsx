import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts';
import ControleurLayout from '../../components/ControleurLayout';
import api from '../../services/api';
import { mockControleurDashboard } from '../../services/mockDataControleur';
import './ControleurDashboard.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';
const PALETTE = ['#2563eb', '#16a34a', '#7c3aed', '#f59e0b', '#ef4444', '#06b6d4'];

function formatDuree(secondes) {
  const s = Math.round(secondes || 0);
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${m}m ${r.toString().padStart(2, '0')}s`;
}

function KPICard({ label, value, sub }) {
  const fmt = v => v >= 1000000 ? `${(v / 1000000).toFixed(1)}M` : v >= 1000 ? `${Math.round(v / 1000)}k` : v;
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{fmt(value)}</div>
      {sub && <div className="kpi-sub">{sub}</div>}
    </div>
  );
}

function normaliser(raw) {
  return {
    medias_suivis: raw.totaux.medias_actifs,
    visiteurs_total: raw.totaux.visiteurs_total,
    pages_vues_total: raw.totaux.pages_vues_total,
    rapports_generes: raw.totaux.rapports_generes,
    par_media: raw.par_media.map((m, i) => ({
      id: m.media_id,
      nom: m.media_nom,
      type_media: m.type_media,
      visiteurs: m.visiteurs,
      pages_vues: m.pages_vues,
      duree_moy: formatDuree(m.duree_moyenne),
      scroll_moy: m.scroll_moyen,
      color: PALETTE[i % PALETTE.length],
    })),
  };
}

// Adapte l'ancien mock à la même forme normalisée (approximatif — le mock
// n'a pas exactement les mêmes champs, c'est un dépannage d'affichage)
function normaliserMock(mock) {
  return {
    medias_suivis: mock.medias_suivis,
    visiteurs_total: mock.visiteurs_total,
    pages_vues_total: mock.pages_vues_total,
    rapports_generes: mock.rapports_generes,
    par_media: mock.tableau.map((m, i) => ({ ...m, color: PALETTE[i % PALETTE.length] })),
  };
}

export default function ControleurDashboard() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setData(normaliserMock(mockControleurDashboard));
    } else {
      api.get('/stats/global/?period=30').then(r => setData(normaliser(r.data)));
    }
  }, []);

  if (!data) return (
    <ControleurLayout pageTitle="Dashboard">
      <div className="loading-state">Chargement…</div>
    </ControleurLayout>
  );

  return (
    <ControleurLayout pageTitle="Dashboard">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Vue d'ensemble — Tous les médias</h1>
      <p className="page-subtitle">Performances consolidées · 30 derniers jours</p>

      <div className="kpi-grid" style={{ marginTop: 24, gridTemplateColumns: 'repeat(4,1fr)' }}>
        <KPICard label="MÉDIAS SUIVIS"     value={data.medias_suivis}     sub="Actifs" />
        <KPICard label="VISITEURS TOTAL"   value={data.visiteurs_total}   sub="Période actuelle" />
        <KPICard label="PAGES VUES TOTAL"  value={data.pages_vues_total}  sub="Période actuelle" />
        <KPICard label="RAPPORTS GÉNÉRÉS"  value={data.rapports_generes}  sub="Sur la période" />
      </div>

      <div className="charts-row" style={{ marginTop: 20 }}>
        <div className="card chart-card">
          <div className="chart-title">Visiteurs par média</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data.par_media} barCategoryGap="30%">
              <XAxis dataKey="nom" tick={{ fontSize: 11, fill: '#6b7280' }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                formatter={v => v.toLocaleString('fr-FR')}
              />
              <Bar dataKey="visiteurs" radius={[3,3,0,0]}>
                {data.par_media.map((m, i) => <Bar key={i} dataKey="visiteurs" fill={m.color} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card perf-mini-card">
          <div className="chart-title">Performances par média</div>
          <div className="perf-mini-grid">
            {data.par_media.map(m => (
              <div key={m.id} className="perf-mini">
                <div className="perf-mini-name">{m.nom}</div>
                <div className="perf-mini-row">
                  <span className="perf-mini-label">Visiteurs</span>
                  <span className="perf-mini-val">{m.visiteurs.toLocaleString('fr-FR')}</span>
                </div>
                <div className="perf-mini-bar-track">
                  <div className="perf-mini-bar-fill" style={{ width: `${m.scroll_moy}%`, background: m.color }} />
                </div>
                <div className="perf-mini-scroll">Scroll moy. {m.scroll_moy}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="perf-header">
          <div className="chart-title" style={{ margin: 0 }}>Tableau comparatif — tous médias</div>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/controleur/comparaison')}>
            Comparer
          </button>
        </div>
        <table className="table" style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>MÉDIA</th>
              <th>TYPE</th>
              <th>VISITEURS</th>
              <th>PAGES VUES</th>
              <th>DURÉE MOY.</th>
              <th>SCROLL MOY.</th>
              <th>RAPPORT</th>
            </tr>
          </thead>
          <tbody>
            {data.par_media.map(m => (
              <tr key={m.id}>
                <td className="font-medium">{m.nom}</td>
                <td><span className={`badge badge-${m.type_media}`}>{m.type_media.charAt(0).toUpperCase() + m.type_media.slice(1)}</span></td>
                <td>{m.visiteurs.toLocaleString('fr-FR')}</td>
                <td>{m.pages_vues.toLocaleString('fr-FR')}</td>
                <td>{m.duree_moy}</td>
                <td>{m.scroll_moy}%</td>
                <td>
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => navigate(`/controleur/rapports/generer?media=${m.id}`)}
                  >
                    Voir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </ControleurLayout>
  );
}