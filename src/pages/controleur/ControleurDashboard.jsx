import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import ControleurLayout from '../../components/ControleurLayout';
import { mockControleurDashboard } from '../../services/mockDataControleur';
import './ControleurDashboard.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const MEDIA_COLORS = {
  lefaso: '#2563eb', sidwaya: '#16a34a', rtb: '#7c3aed', omega: '#f59e0b',
};

function KPICard({ label, value, delta, deltaSuffix = '', sub }) {
  const fmt = v => v >= 1000000 ? `${(v / 1000000).toFixed(1)}M` : v >= 1000 ? `${Math.round(v / 1000)}k` : v;
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{fmt(value)}</div>
      {delta !== undefined && (
        <div className="kpi-delta">▲ +{delta}{deltaSuffix}</div>
      )}
      {sub && <div className="kpi-sub">{sub}</div>}
    </div>
  );
}

export default function ControleurDashboard() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) setData(mockControleurDashboard);
    // else: api.get('/dashboard/controleur/').then(r => setData(r.data))
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
      <p className="page-subtitle">Performances consolidées · Mars 2025</p>

      {/* KPIs */}
      <div className="kpi-grid" style={{ marginTop: 24, gridTemplateColumns: 'repeat(4,1fr)' }}>
        <KPICard label="MÉDIAS SUIVIS"     value={data.medias_suivis}     sub="Tous actifs" />
        <KPICard label="VISITEURS TOTAL"   value={data.visiteurs_total}   delta={data.visiteurs_delta_pct} deltaSuffix="%" />
        <KPICard label="PAGES VUES TOTAL"  value={data.pages_vues_total}  delta={data.pages_vues_delta_pct} deltaSuffix="%" />
        <KPICard label="RAPPORTS GÉNÉRÉS"  value={data.rapports_generes}  sub="Ce mois" />
      </div>

      {/* Charts row */}
      <div className="charts-row" style={{ marginTop: 20 }}>
        {/* Stacked bar */}
        <div className="card chart-card">
          <div className="chart-title">Évolution trafic — tous médias</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data.trafic_7j} barCategoryGap="30%">
              <XAxis dataKey="jour" tick={{ fontSize: 12, fill: '#6b7280' }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                formatter={v => v.toLocaleString('fr-FR')}
              />
              <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 11, paddingTop: 8 }} />
              <Bar dataKey="lefaso" name="Lefaso.net"  stackId="a" fill={MEDIA_COLORS.lefaso}  radius={[0,0,0,0]} />
              <Bar dataKey="sidwaya" name="Sidwaya"    stackId="a" fill={MEDIA_COLORS.sidwaya} />
              <Bar dataKey="rtb"    name="RTB Online"  stackId="a" fill={MEDIA_COLORS.rtb}     />
              <Bar dataKey="omega"  name="Radio Omega" stackId="a" fill={MEDIA_COLORS.omega}   radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Mini perf cards */}
        <div className="card perf-mini-card">
          <div className="chart-title">Performances par média</div>
          <div className="perf-mini-grid">
            {data.performances.map(m => (
              <div key={m.id} className="perf-mini">
                <div className="perf-mini-name">{m.nom}</div>
                <div className="perf-mini-row">
                  <span className="perf-mini-label">Visiteurs</span>
                  <span className="perf-mini-val">{m.visiteurs.toLocaleString('fr-FR')}</span>
                </div>
                <div className="perf-mini-bar-track">
                  <div
                    className="perf-mini-bar-fill"
                    style={{ width: `${m.scroll_moy}%`, background: m.color }}
                  />
                </div>
                <div className="perf-mini-scroll">Scroll moy. {m.scroll_moy}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tableau comparatif */}
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
            {data.tableau.map(m => (
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
