import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import { mockAnalysePage } from '../../services/mockDataGestionnaire';
import './GestionnaireAnalysePage.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

function KPICard({ label, value, delta }) {
  const isNeg = delta?.startsWith('-');
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
      {delta && (
        <div className={`kpi-delta${isNeg ? ' kpi-delta-neg' : ''}`}>
          {isNeg ? '▼' : '▲'} {delta.replace(/^[+-]/, '')} vs sem. préc.
        </div>
      )}
    </div>
  );
}

export default function GestionnaireAnalysePage() {
  const { id } = useParams();      // récupère l'id depuis l'URL
  const navigate = useNavigate();
  const [data, setData] = useState(null);

  useEffect(() => {
    if (USE_MOCK) {
      // En mock, on retourne toujours la même page quel que soit l'id
      setData(mockAnalysePage);
    } else {
      // En prod : api.get(`/pages/${id}/analyse/`).then(r => setData(r.data))
    }
  }, [id]);

  if (!data) return (
    <GestionnaireLayout pageTitle="Analyse page">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  const { kpis } = data;

  return (
    <GestionnaireLayout pageTitle="Analyse page">
      {/* Lien retour */}
      <button
        className="btn-retour"
        onClick={() => navigate('/gestionnaire/pages')}
      >
        ← Retour aux pages
      </button>

      {/* En-tête */}
      <div className="page-eyebrow" style={{ marginTop: 16 }}>
        {data.media_nom.toUpperCase()} / PAGES WEB
      </div>
      <h1 className="page-title">{data.titre}</h1>
      <p className="page-subtitle">Publié le {data.date_publication} · Analyse détaillée</p>

      {/* KPIs */}
      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(4,1fr)', marginTop: 24 }}>
        <KPICard label="VUES TOTALES"   value={kpis.vues_totales.toLocaleString('fr-FR')} delta={kpis.vues_delta} />
        <KPICard label="DURÉE MOYENNE"  value={kpis.duree_moy}   delta={kpis.duree_delta} />
        <KPICard label="SCROLL MOYEN"   value={`${kpis.scroll_moy}%`}  delta={kpis.scroll_delta} />
        <KPICard label="TAUX DE REBOND" value={`${kpis.taux_rebond}%`} delta={kpis.rebond_delta} />
      </div>

      {/* Graphiques */}
      <div className="charts-row" style={{ marginTop: 20 }}>

        {/* Visiteurs par heure */}
        <div className="card chart-card">
          <div className="chart-title">Visiteurs par heure de la journée</div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={data.par_heure} margin={{ left: -20, right: 10 }}>
              <defs>
                <linearGradient id="gradVisiteurs" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#2563eb" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="h"
                tick={{ fontSize: 11, fill: '#9ca3af' }}
                axisLine={false} tickLine={false}
              />
              <YAxis hide />
              <Tooltip
                contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                formatter={v => [`${v} visiteurs`]}
              />
              <Area
                type="monotone"
                dataKey="v"
                stroke="#2563eb"
                strokeWidth={2}
                fill="url(#gradVisiteurs)"
                dot={false}
              />
            </AreaChart>
          </ResponsiveContainer>
          <div className="pic-audience">{data.pic_audience}</div>
        </div>

        {/* Profondeur de scroll */}
        <div className="card chart-card">
          <div className="chart-title">Profondeur de scroll par section</div>
          <div className="scroll-sections">
            {data.scroll_sections.map(s => (
              <div key={s.label} className="scroll-section-row">
                <span className="scroll-section-label">{s.label}</span>
                <div className="barre-track" style={{ flex: 1 }}>
                  <div
                    className="barre-fill"
                    style={{ width: `${s.pct}%`, background: s.color }}
                  />
                </div>
                <span className="scroll-section-pct">{s.pct}%</span>
              </div>
            ))}
          </div>
          <p className="scroll-sections-note">
            % de visiteurs ayant atteint chaque section
          </p>
        </div>
      </div>
    </GestionnaireLayout>
  );
}
