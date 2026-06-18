import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell,
} from 'recharts';
import AdminLayout from '../../components/AdminLayout';
import { mockDashboardAdmin } from '../../services/mockData';
import './AdminDashboard.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const PIE_COLORS = ['#2563eb', '#3b82f6', '#8b5cf6', '#f59e0b'];

function KPICard({ label, value, delta, deltaSuffix = '' }) {
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{typeof value === 'number' && value >= 1000
        ? value >= 1000000 ? `${(value/1000000).toFixed(1)}M` : `${Math.round(value/1000)}k`
        : value}
      </div>
      {delta !== undefined && (
        <div className="kpi-delta">
          <span className="kpi-delta-arrow">▲</span>
          +{delta}{deltaSuffix} ce mois
        </div>
      )}
    </div>
  );
}

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setData(mockDashboardAdmin);
    } else {
      // TODO: api.get('/dashboard/admin/').then(r => setData(r.data))
    }
  }, []);

  if (!data) return (
    <AdminLayout pageTitle="Vue globale">
      <div className="loading-state">Chargement…</div>
    </AdminLayout>
  );

  const formatVisiteurs = v => v >= 1000 ? `${Math.round(v/1000)}k` : v;

  return (
    <AdminLayout pageTitle="Vue globale">
      {/* Page header */}
      <div className="page-eyebrow">ADMINISTRATION</div>
      <h1 className="page-title">Vue d'ensemble globale</h1>
      <p className="page-subtitle">Activité consolidée · Mars 2025</p>

      {/* KPIs */}
      <div className="kpi-grid" style={{ marginTop: 24 }}>
        <KPICard label="MÉDIAS ACTIFS" value={data.medias_actifs} delta={data.medias_actifs_delta} />
        <KPICard label="UTILISATEURS" value={data.utilisateurs} delta={data.utilisateurs_delta} />
        <KPICard label="VISITEURS TOTAL" value={data.visiteurs_total} delta={data.visiteurs_delta_pct} deltaSuffix="%" />
        <KPICard label="RAPPORTS" value={data.rapports} delta={data.rapports_delta} />
      </div>

      {/* Charts */}
      <div className="charts-row" style={{ marginTop: 20 }}>
        {/* Bar chart */}
        <div className="card chart-card">
          <div className="chart-title">Trafic global — 7 derniers jours</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data.trafic_7j} barGap={4} barCategoryGap="35%">
              <XAxis dataKey="jour" tick={{ fontSize: 12, fill: '#6b7280' }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                cursor={{ fill: '#f3f4f6' }}
              />
              <Legend
                iconType="circle" iconSize={8}
                wrapperStyle={{ fontSize: 12, paddingTop: 8 }}
              />
              <Bar dataKey="pages_vues" name="Pages vues" fill="#bfdbfe" radius={[3,3,0,0]} />
              <Bar dataKey="visiteurs" name="Visiteurs" fill="#dbeafe" radius={[3,3,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Donut chart */}
        <div className="card chart-card">
          <div className="chart-title">Sources de trafic</div>
          <div className="donut-layout">
            <ResponsiveContainer width={140} height={140}>
              <PieChart>
                <Pie
                  data={data.sources_trafic}
                  cx="50%" cy="50%"
                  innerRadius={40} outerRadius={62}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {data.sources_trafic.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
            <div className="donut-legend">
              {data.sources_trafic.map((s, i) => (
                <div key={s.name} className="donut-legend-row">
                  <span className="donut-dot" style={{ background: PIE_COLORS[i] }} />
                  <span className="donut-legend-name">{s.name}</span>
                  <span className="donut-legend-val">{s.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Performances table */}
      <div className="card" style={{ marginTop: 20 }}>
        <div className="perf-header">
          <div className="chart-title" style={{ margin: 0 }}>Performances par média</div>
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => navigate('/admin/medias')}
          >
            Gérer les médias →
          </button>
        </div>
        <table className="table" style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>MÉDIA</th>
              <th>TYPE</th>
              <th>GESTIONNAIRE</th>
              <th>VISITEURS/MOIS</th>
              <th>STATUT</th>
            </tr>
          </thead>
          <tbody>
            {data.performances_medias.map(m => (
              <tr key={m.id}>
                <td className="font-medium">{m.nom}</td>
                <td>
                  <span className={`badge badge-${m.type_media}`}>
                    {m.type_media.charAt(0).toUpperCase() + m.type_media.slice(1)}
                  </span>
                </td>
                <td className={m.gestionnaire_nom ? '' : 'text-muted'}>
                  {m.gestionnaire_nom || '—'}
                </td>
                <td>{formatVisiteurs(m.visiteurs_mois)}</td>
                <td>
                  <span className={`badge badge-${m.statut}`}>
                    • {m.statut.charAt(0).toUpperCase() + m.statut.slice(1)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </AdminLayout>
  );
}
