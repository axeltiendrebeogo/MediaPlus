import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import { mockGestionnaireDashboard } from '../../services/mockDataGestionnaire';
import './GestionnaireDashboard.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

// Labels affichés sur les boutons de période
const PERIODES = [
  { value: '7j',    label: '7 jours' },
  { value: '30j',   label: '30 jours' },
  { value: '3mois', label: '3 mois' },
  { value: 'annee', label: 'Cette année' },
];

// Composant KPI card réutilisable
function KPICard({ label, value, delta }) {
  const isNeg = delta?.startsWith('▼') || delta?.startsWith('-');
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {delta && (
        <div className={`kpi-delta ${isNeg ? 'kpi-delta-neg' : ''}`}>
          {isNeg ? '▼' : '▲'} {delta.replace(/^[▲▼]/, '')} vs M-1
        </div>
      )}
    </div>
  );
}

export default function GestionnaireDashboard() {
  const [data, setData] = useState(null);
  const [periode, setPeriode] = useState('30j');
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) setData(mockGestionnaireDashboard);
    // sinon : api.get('/dashboard/gestionnaire/').then(r => setData(r.data))
  }, []);

  if (!data) return (
    <GestionnaireLayout pageTitle="Dashboard">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  const kpis = data.kpis[periode];
  const trafic = data.trafic[periode];

  return (
    <GestionnaireLayout pageTitle="Dashboard">
      {/* En-tête de page */}
      <div className="page-eyebrow">{data.media_nom.toUpperCase()}</div>
      <h1 className="page-title">Tableau de bord</h1>
      <p className="page-subtitle">Performances de votre média · Mars 2025</p>

      {/* Sélecteur de période */}
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

      {/* KPIs */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4,1fr)', marginTop: 20 }}>
        <KPICard label="VISITEURS UNIQUES" value={kpis.visiteurs.toLocaleString('fr-FR')} delta={kpis.visiteurs_delta} />
        <KPICard label="PAGES VUES"        value={kpis.pages_vues.toLocaleString('fr-FR')} delta={kpis.pages_delta} />
        <KPICard label="DURÉE MOYENNE"     value={kpis.duree_moy}   delta={kpis.duree_delta} />
        <KPICard label="SCROLL MOYEN"      value={`${kpis.scroll_moy}%`} delta={kpis.scroll_delta} />
      </div>

      {/* Graphiques */}
      <div className="charts-row" style={{ marginTop: 20 }}>

        {/* Graphique trafic */}
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

        {/* Appareils + Sources */}
        <div className="card chart-card">
          {/* Appareils */}
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

          {/* Sources */}
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

      {/* Top pages */}
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
