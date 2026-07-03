import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import api from '../../services/api';
import { mockGestionnaireDashboard } from '../../services/mockDataGestionnaire';
import './GestionnaireDashboard.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const PERIODES = [
  { value: '7j',    label: '7 jours',      jours: 7 },
  { value: '30j',   label: '30 jours',     jours: 30 },
  { value: '3mois', label: '3 mois',       jours: 90 },
  { value: 'annee', label: 'Cette année',  jours: 365 },
];

const COULEUR_APPAREIL = { mobile: '#2563eb', desktop: '#8b5cf6', tablette: '#f59e0b' };

// Formate des secondes en "Xm Ys" pour l'affichage
function formatDuree(secondes) {
  const s = Math.round(secondes || 0);
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${m}m ${r.toString().padStart(2, '0')}s`;
}

function formatDateLabel(isoDate) {
  const [, mm, dd] = isoDate.split('-');
  return `${dd}/${mm}`;
}

function KPICard({ label, value, delta }) {
  const isNeg = delta?.startsWith('-');
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {delta && (
        <div className={`kpi-delta ${isNeg ? 'kpi-delta-neg' : ''}`}>
          {isNeg ? '▼' : '▲'} {delta} vs période précédente
        </div>
      )}
    </div>
  );
}

// Transforme la réponse API (ou le mock) vers la forme attendue par l'UI
function normaliser(raw) {
  return {
    media_nom: raw.media_nom,
    kpis: {
      visiteurs: raw.kpi.visiteurs_uniques.valeur.toLocaleString('fr-FR'),
      visiteurs_delta: `${raw.kpi.visiteurs_uniques.delta_pct}%`,
      pages_vues: raw.kpi.pages_vues.valeur.toLocaleString('fr-FR'),
      pages_delta: `${raw.kpi.pages_vues.delta_pct}%`,
      duree_moy: formatDuree(raw.kpi.duree_moyenne.valeur),
      duree_delta: `${raw.kpi.duree_moyenne.delta_pct}%`,
      scroll_moy: raw.kpi.scroll_moyen.valeur,
      scroll_delta: `${raw.kpi.scroll_moyen.delta_pct}%`,
    },
    trafic: raw.trafic_journalier.map(j => ({
      label: formatDateLabel(j.date),
      pages_vues: j.vues,
      visiteurs: j.visiteurs,
    })),
    appareils: raw.appareils.map(a => ({
      label: a.type.charAt(0).toUpperCase() + a.type.slice(1),
      pct: a.pct,
      color: COULEUR_APPAREIL[a.type] || '#94a3b8',
    })),
    sources: raw.sources.map(s => ({ label: s.source, pct: s.pct })),
    top_pages: raw.top_pages.map(p => ({
      id: p.id,
      titre: p.nom,
      vues: p.vues,
      duree: formatDuree(p.duree_moyenne),
      scroll: p.scroll_moyen,
      tendance: p.tendance === 'up' ? 'hausse' : 'baisse',
    })),
  };
}

// Adapte l'ancien mock (déjà découpé par période) à la même forme normalisée
function normaliserMock(mock, periode) {
  const k = mock.kpis[periode];
  return {
    media_nom: mock.media_nom,
    kpis: k,
    trafic: mock.trafic[periode],
    appareils: mock.appareils,
    sources: mock.sources,
    top_pages: mock.top_pages,
  };
}

export default function GestionnaireDashboard() {
  const [data, setData] = useState(null);
  const [periode, setPeriode] = useState('30j');
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setData(normaliserMock(mockGestionnaireDashboard, periode));
    } else {
      const jours = PERIODES.find(p => p.value === periode)?.jours || 30;
      api.get(`/stats/dashboard/?period=${jours}`).then(r => setData(normaliser(r.data)));
    }
  }, [periode]);

  if (!data) return (
    <GestionnaireLayout pageTitle="Dashboard">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  const { kpis, trafic } = data;

  return (
    <GestionnaireLayout pageTitle="Dashboard">
      <div className="page-eyebrow">{data.media_nom.toUpperCase()}</div>
      <h1 className="page-title">Tableau de bord</h1>
      <p className="page-subtitle">Performances de votre média</p>

      <div className="periode-selector">
        {PERIODES.map(p => (
          <button
            key={p.value}
            className={`periode-btn${periode === p.value ? ' active' : ''}`}
            onClick={() => setPeriode(p.value)}
          >
            {p.label}
          </button>
        ))}
      </div>

      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4,1fr)', marginTop: 20 }}>
        <KPICard label="VISITEURS UNIQUES" value={kpis.visiteurs} delta={kpis.visiteurs_delta} />
        <KPICard label="PAGES VUES"        value={kpis.pages_vues} delta={kpis.pages_delta} />
        <KPICard label="DURÉE MOYENNE"     value={kpis.duree_moy}   delta={kpis.duree_delta} />
        <KPICard label="SCROLL MOYEN"      value={`${kpis.scroll_moy}%`} delta={kpis.scroll_delta} />
      </div>

      <div className="charts-row" style={{ marginTop: 20 }}>
        <div className="card chart-card">
          <div className="chart-title">Visiteurs &amp; Pages vues — {PERIODES.find(p => p.value === periode)?.label}</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={trafic} barGap={4} barCategoryGap="35%">
              <XAxis dataKey="label" tick={{ fontSize: 12, fill: '#6b7280' }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                formatter={v => v.toLocaleString('fr-FR')}
              />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12, paddingTop: 8 }} />
              <Bar dataKey="pages_vues" name="Pages vues" fill="#bfdbfe" radius={[3,3,0,0]} />
              <Bar dataKey="visiteurs"  name="Visiteurs"  fill="#dbeafe" radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card chart-card">
          <div className="chart-title" style={{ marginBottom: 12 }}>Répartition par appareil</div>
          <div className="barres-list">
            {data.appareils.map(a => (
              <div key={a.label} className="barre-row">
                <span className="barre-label">{a.label}</span>
                <div className="barre-track">
                  <div className="barre-fill" style={{ width: `${a.pct}%`, background: a.color }} />
                </div>
                <span className="barre-pct">{a.pct}%</span>
              </div>
            ))}
          </div>

          <div className="sources-title">SOURCES DE TRAFIC</div>
          <div className="sources-list">
            {data.sources.map(s => (
              <div key={s.label} className="source-row">
                <span>{s.label}</span>
                <span className="font-medium">{s.pct}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="perf-header">
          <div className="chart-title" style={{ margin: 0 }}>Pages les plus consultées</div>
          <button className="btn btn-secondary btn-sm" onClick={() => navigate('/gestionnaire/pages')}>
            Toutes les pages →
          </button>
        </div>
        <table className="table" style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>TITRE</th>
              <th>VUES</th>
              <th>DURÉE MOY.</th>
              <th>SCROLL</th>
              <th>TENDANCE</th>
            </tr>
          </thead>
          <tbody>
            {data.top_pages.map(p => (
              <tr key={p.id}>
                <td className="font-medium">{p.titre}</td>
                <td>{p.vues.toLocaleString('fr-FR')}</td>
                <td>{p.duree}</td>
                <td>
                  <div className="scroll-inline">
                    <div className="barre-track" style={{ width: 80 }}>
                      <div className="barre-fill" style={{ width: `${p.scroll}%`, background: '#2563eb' }} />
                    </div>
                    <span>{p.scroll}%</span>
                  </div>
                </td>
                <td>
                  <span className={`tendance ${p.tendance}`}>
                    {p.tendance === 'hausse' ? '▲' : '▼'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GestionnaireLayout>
  );
}