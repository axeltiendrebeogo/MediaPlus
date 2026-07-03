import React, { useState, useEffect, useCallback } from 'react';
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip,
  ResponsiveContainer, Legend,
} from 'recharts';
import ControleurLayout from '../../components/ControleurLayout';
import api from '../../services/api';
import { mockComparaison } from '../../services/mockDataControleur';
import './ControleurComparaison.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const PERIODES = [
  { label: '7 derniers jours',  value: '7j',    jours: 7   },
  { label: '30 derniers jours', value: '30j',   jours: 30  },
  { label: '3 mois',            value: '3mois', jours: 90  },
  { label: 'Cette année',       value: 'annee', jours: 365 },
];

const KPI_TABS = [
  { label: 'Visiteurs',   api: 'visiteurs'   },
  { label: 'Pages vues',  api: 'pages_vues'  },
  { label: 'Durée moy.',  api: 'duree_moyenne' },
  { label: 'Scroll moy.', api: 'scroll_moyen'  },
];

export default function ControleurComparaison() {
  const [allMedias, setAllMedias] = useState([]);
  const [selected, setSelected] = useState([]);
  const [periode, setPeriode] = useState('30j');
  const [kpiTab, setKpiTab] = useState(KPI_TABS[0]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Charger la liste des médias au démarrage
  useEffect(() => {
    if (USE_MOCK) {
      const ids = Object.keys(mockComparaison.medias).map(Number);
      const ms = ids.map(id => ({
        id,
        nom: mockComparaison.medias[id].nom,
        color: mockComparaison.medias[id].color,
      }));
      setAllMedias(ms);
      setSelected([ids[0], ids[1]]);
    } else {
      api.get('/medias/').then(r => {
        const PALETTE = ['#2563eb', '#16a34a', '#7c3aed', '#f59e0b', '#ef4444', '#06b6d4'];
        const ms = r.data.results.map((m, i) => ({
          id: m.id, nom: m.nom, color: PALETTE[i % PALETTE.length],
        }));
        setAllMedias(ms);
        if (ms.length >= 2) setSelected([ms[0].id, ms[1].id]);
      });
    }
  }, []);

  // Recharger les stats quand la sélection, la période ou le KPI changent
  const fetchComparaison = useCallback(() => {
    if (selected.length < 2) return;
    if (USE_MOCK) { setData(mockComparaison); return; }

    const jours = PERIODES.find(p => p.value === periode)?.jours || 30;
    setLoading(true);
    api.get(`/stats/comparaison/?medias=${selected.join(',')}&period=${jours}&kpi=${kpiTab.api}`)
      .then(r => setData(r.data))
      .finally(() => setLoading(false));
  }, [selected, periode, kpiTab]);

  useEffect(() => { fetchComparaison(); }, [fetchComparaison]);

  const toggleMedia = id => {
    setSelected(prev =>
      prev.includes(id)
        ? prev.length > 2 ? prev.filter(x => x !== id) : prev
        : prev.length < 6 ? [...prev, id] : prev
    );
  };

  const couleurs = data?.couleurs || {};
  const getColor = id => couleurs[String(id)] || allMedias.find(m => m.id === id)?.color || '#6b7280';

  // Graphique G8 — KPI comparatif (barres)
  const kpiChartData = (data?.comparaison_kpi || []).map(m => ({
    name: m.media_nom,
    value: m.valeur,
  }));

  // Graphique G7 — évolution journalière (lignes)
  const evolutionData = (data?.evolution || []).map(row => {
    const mapped = { date: row.date.slice(5) }; // "MM-DD"
    allMedias.filter(m => selected.includes(m.id)).forEach(m => {
      mapped[m.nom] = row[m.nom] || 0;
    });
    return mapped;
  });

  const selectedMedias = allMedias.filter(m => selected.includes(m.id));

  return (
    <ControleurLayout pageTitle="Comparaison">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Comparer les médias</h1>
      <p className="page-subtitle">Analyses croisées entre médias sélectionnés</p>

      <div className="card comparaison-filters" style={{ marginTop: 24 }}>
        <div className="comp-filter-label">Médias à comparer (2 minimum, 6 maximum)</div>
        <div className="comp-media-chips">
          {allMedias.map(m => (
            <button
              key={m.id}
              className={`media-chip${selected.includes(m.id) ? ' active' : ''}`}
              style={selected.includes(m.id) ? { borderColor: m.color, background: m.color + '18', color: m.color } : {}}
              onClick={() => toggleMedia(m.id)}
            >
              {m.nom}
            </button>
          ))}
        </div>
        <div className="comp-periode-row">
          <span className="comp-filter-label" style={{ marginTop: 0 }}>Période :</span>
          <select className="form-select comp-periode-select" value={periode} onChange={e => setPeriode(e.target.value)}>
            {PERIODES.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
          </select>
        </div>
      </div>

      {selected.length < 2 ? (
        <div className="comp-empty">Sélectionnez au moins 2 médias pour comparer.</div>
      ) : loading ? (
        <div className="loading-state" style={{ marginTop: 24 }}>Chargement…</div>
      ) : (
        <>
          <div className="charts-row" style={{ marginTop: 16 }}>
            {/* G8 — KPI comparatif */}
            <div className="card chart-card">
              <div className="chart-title-row">
                <div className="chart-title">Comparaison KPI</div>
                <div className="kpi-tabs">
                  {KPI_TABS.map(tab => (
                    <button
                      key={tab.api}
                      className={`kpi-tab${kpiTab.api === tab.api ? ' active' : ''}`}
                      onClick={() => setKpiTab(tab)}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>
              </div>
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={kpiChartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                  <XAxis type="number" hide />
                  <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fill: '#6b7280' }} axisLine={false} tickLine={false} width={110} />
                  <Tooltip
                    formatter={v => v.toLocaleString('fr-FR')}
                    contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]} fill="#2563eb" />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* G7 — Évolution multi-médias */}
            <div className="card chart-card">
              <div className="chart-title">Évolution — {PERIODES.find(p => p.value === periode)?.label}</div>
              <ResponsiveContainer width="100%" height={180}>
                <LineChart data={evolutionData}>
                  <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#6b7280' }} axisLine={false} tickLine={false} interval="preserveStartEnd" />
                  <YAxis hide />
                  <Tooltip
                    formatter={v => v.toLocaleString('fr-FR')}
                    contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                  />
                  <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
                  {selectedMedias.map(m => (
                    <Line key={m.id} type="monotone" dataKey={m.nom} stroke={getColor(m.id)} dot={false} strokeWidth={2} />
                  ))}
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Tableau récapitulatif */}
          <div className="card" style={{ marginTop: 16 }}>
            <div className="chart-title">Récapitulatif comparatif</div>
            <table className="table">
              <thead>
                <tr>
                  <th>MÉDIA</th>
                  <th>VISITEURS</th>
                  <th>PAGES VUES</th>
                  <th>DURÉE MOY.</th>
                  <th>SCROLL MOY.</th>
                </tr>
              </thead>
              <tbody>
                {selectedMedias.map(m => {
                  const kpi = (data?.comparaison_kpi || []).find(k => k.media_id === m.id) || {};
                  return (
                    <tr key={m.id}>
                      <td>
                        <div className="comp-table-media">
                          <span className="comp-legend-dot" style={{ background: getColor(m.id) }} />
                          <span className="font-medium">{m.nom}</span>
                        </div>
                      </td>
                      <td>{(kpi.valeur || 0).toLocaleString('fr-FR')}</td>
                      <td>—</td>
                      <td>—</td>
                      <td>—</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </ControleurLayout>
  );
}