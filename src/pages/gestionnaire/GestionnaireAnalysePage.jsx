import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import api from '../../services/api';
import { mockAnalysePage } from '../../services/mockDataGestionnaire';
import './GestionnaireAnalysePage.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

function formatDuree(s) {
  const sec = Math.round(s || 0);
  return `${Math.floor(sec / 60)}m ${(sec % 60).toString().padStart(2, '0')}s`;
}

function KPICard({ label, value }) {
  return (
    <div className="kpi-card card">
      <div className="kpi-label">{label}</div>
      <div className="kpi-value">{value}</div>
    </div>
  );
}

// Transforme la réponse de GET /api/pages/:id/stats/ vers la forme attendue par l'UI
function normaliser(raw, pageNom) {
  // G4 — visiteurs par heure (heure: "HH:00", visiteurs: N)
  const par_heure = (raw.par_heure || []).map(h => ({
    h: h.heure.slice(0, 2) + 'h',
    v: h.visiteurs,
  }));

  const picHeure = par_heure.reduce((max, h) => h.v > (max?.v || 0) ? h : max, null);

  // G5 — scroll sections
  const COULEURS_SCROLL = ['#2563eb', '#7c3aed', '#059669', '#f59e0b'];
  const scroll_sections = (raw.scroll_sections || []).map((s, i) => ({
    label: s.section,
    pct: s.pct_visiteurs,
    color: COULEURS_SCROLL[i % COULEURS_SCROLL.length],
  }));

  // Sources (G2 à l'échelle de la page)
  const sources = (raw.sources || []).map(s => ({ label: s.source, pct: s.pct }));

  // Appareils (G3 à l'échelle de la page)
  const appareils = (raw.appareils || []).map(a => ({ label: a.type, pct: a.pct }));

  return {
    titre: raw.nom || pageNom || 'Page',
    media_nom: '',
    date_publication: raw.periode?.debut || '',
    par_heure,
    scroll_sections,
    sources,
    appareils,
    pic_audience: picHeure
      ? `📊 Pic d'audience à ${picHeure.h} avec ${picHeure.v} visiteurs`
      : '',
    kpis: {
      vues_totales: raw.vues || 0,
      visiteurs: raw.visiteurs_uniques || 0,
      duree_moy: formatDuree(raw.duree_moyenne),
      scroll_moy: raw.scroll_moyen || 0,
      taux_rebond: raw.taux_rebond || 0,
    },
  };
}

// Adapte l'ancien format mock à la même forme
function normaliserMock(mock) {
  return {
    titre: mock.titre,
    media_nom: mock.media_nom || '',
    date_publication: mock.date_publication || '',
    par_heure: mock.par_heure || [],
    scroll_sections: mock.scroll_sections || [],
    sources: mock.sources || [],
    appareils: mock.appareils || [],
    pic_audience: mock.pic_audience || '',
    kpis: {
      vues_totales: mock.kpis?.vues_totales || 0,
      visiteurs: mock.kpis?.visiteurs || 0,
      duree_moy: mock.kpis?.duree_moy || '0m 00s',
      scroll_moy: mock.kpis?.scroll_moy || 0,
      taux_rebond: mock.kpis?.taux_rebond || 0,
    },
  };
}

export default function GestionnaireAnalysePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);

  useEffect(() => {
    if (USE_MOCK) {
      setData(normaliserMock(mockAnalysePage));
      return;
    }
    // Charge les stats détaillées de la page (G2, G3, G4, G5)
    api.get(`/pages/${id}/stats/`).then(r => {
      setData(normaliser(r.data, ''));
    });
  }, [id]);

  if (!data) return (
    <GestionnaireLayout pageTitle="Analyse page">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  const { kpis } = data;

  return (
    <GestionnaireLayout pageTitle="Analyse page">
      <button className="btn-retour" onClick={() => navigate('/gestionnaire/pages')}>
        ← Retour aux pages
      </button>

      <div className="page-eyebrow" style={{ marginTop: 16 }}>
        {data.media_nom ? data.media_nom.toUpperCase() + ' / ' : ''}PAGES WEB
      </div>
      <h1 className="page-title">{data.titre}</h1>
      <p className="page-subtitle">Analyse détaillée</p>

      <div className="kpi-grid" style={{ gridTemplateColumns: 'repeat(5,1fr)', marginTop: 24 }}>
        <KPICard label="VUES TOTALES"    value={kpis.vues_totales.toLocaleString('fr-FR')} />
        <KPICard label="VISITEURS"       value={kpis.visiteurs.toLocaleString('fr-FR')} />
        <KPICard label="DURÉE MOYENNE"   value={kpis.duree_moy} />
        <KPICard label="SCROLL MOYEN"    value={`${kpis.scroll_moy}%`} />
        <KPICard label="TAUX DE REBOND"  value={`${kpis.taux_rebond}%`} />
      </div>

      <div className="charts-row" style={{ marginTop: 20 }}>
        {/* G4 — Visiteurs par heure */}
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
              <XAxis dataKey="h" tick={{ fontSize: 11, fill: '#9ca3af' }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip
                contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                formatter={v => [`${v} visiteurs`]}
              />
              <Area type="monotone" dataKey="v" stroke="#2563eb" strokeWidth={2}
                fill="url(#gradVisiteurs)" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
          {data.pic_audience && <div className="pic-audience">{data.pic_audience}</div>}
        </div>

        {/* G5 — Profondeur de scroll */}
        <div className="card chart-card">
          <div className="chart-title">Profondeur de scroll par section</div>
          <div className="scroll-sections">
            {data.scroll_sections.map(s => (
              <div key={s.label} className="scroll-section-row">
                <span className="scroll-section-label">{s.label}</span>
                <div className="barre-track" style={{ flex: 1 }}>
                  <div className="barre-fill" style={{ width: `${s.pct}%`, background: s.color }} />
                </div>
                <span className="scroll-section-pct">{s.pct}%</span>
              </div>
            ))}
          </div>
          <p className="scroll-sections-note">% de visiteurs ayant atteint chaque section</p>

          {/* Sources de trafic (G2) à l'échelle de la page */}
          {data.sources.length > 0 && (
            <>
              <div className="chart-title" style={{ marginTop: 16, fontSize: 13 }}>Sources de trafic</div>
              {data.sources.map(s => (
                <div key={s.label} className="scroll-section-row" style={{ marginTop: 6 }}>
                  <span className="scroll-section-label">{s.label}</span>
                  <div className="barre-track" style={{ flex: 1 }}>
                    <div className="barre-fill" style={{ width: `${s.pct}%`, background: '#7c3aed' }} />
                  </div>
                  <span className="scroll-section-pct">{s.pct}%</span>
                </div>
              ))}
            </>
          )}
        </div>
      </div>

      {/* Appareils (G3 à l'échelle de la page) */}
      {data.appareils.length > 0 && (
        <div className="card" style={{ marginTop: 16, padding: 20 }}>
          <div className="chart-title">Répartition par appareil (cette page)</div>
          <div className="barres-list" style={{ marginTop: 12 }}>
            {data.appareils.map(a => (
              <div key={a.label} className="barre-row">
                <span className="barre-label">{a.label.charAt(0).toUpperCase() + a.label.slice(1)}</span>
                <div className="barre-track">
                  <div className="barre-fill" style={{ width: `${a.pct}%`, background: '#2563eb' }} />
                </div>
                <span className="barre-pct">{a.pct}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </GestionnaireLayout>
  );
}