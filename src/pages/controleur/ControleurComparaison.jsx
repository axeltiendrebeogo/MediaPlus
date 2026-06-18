import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts';
import ControleurLayout from '../../components/ControleurLayout';
import { mockComparaison } from '../../services/mockDataControleur';
import './ControleurComparaison.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const PERIODES = [
  { label: '7 derniers jours', value: '7j' },
  { label: '30 derniers jours', value: '30j' },
  { label: 'Ce mois', value: 'mois' },
  { label: 'Mois précédent', value: 'mois_prec' },
];

const KPI_TABS = ['Visiteurs', 'Pages vues', 'Scroll'];
const KPI_KEY = { Visiteurs: 'visiteurs', 'Pages vues': 'pages_vues', Scroll: 'scroll_moy' };
const KPI_SEMAINE = { Visiteurs: 'visiteurs', 'Pages vues': 'pages_vues', Scroll: 'scroll' };

export default function ControleurComparaison() {
  const [allMedias, setAllMedias] = useState([]);
  const [selected, setSelected] = useState([]);
  const [periode, setPeriode] = useState('30j');
  const [kpiTab, setKpiTab] = useState('Visiteurs');
  const [data, setData] = useState(null);

  useEffect(() => {
    if (USE_MOCK) {
      const ids = Object.keys(mockComparaison.medias).map(Number);
      setAllMedias(ids.map(id => ({ id, nom: mockComparaison.medias[id].nom, color: mockComparaison.medias[id].color })));
      setSelected([ids[0], ids[1]]); // default: 2 premiers
      setData(mockComparaison);
    }
  }, []);

  const toggleMedia = id => {
    setSelected(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const selectedData = selected.map(id => data?.medias[id]).filter(Boolean);

  // Graphique KPI comparatif (barres côte à côte)
  const kpiChartData = selectedData.map(m => ({
    name: m.nom,
    value: m[KPI_KEY[kpiTab]] || 0,
    color: m.color,
  }));

  // Graphique évolution croisée par semaine
  const semainesData = (data?.semaines || []).map((sem, i) => {
    const row = { sem };
    selectedData.forEach(m => {
      const key = KPI_SEMAINE[kpiTab];
      row[m.nom] = m.par_semaine[key]?.[i] ?? 0;
    });
    return row;
  });

  // Formatage valeurs
  const fmtVal = (v) => {
    if (kpiTab === 'Scroll') return `${v}%`;
    return v >= 1000 ? `${Math.round(v / 1000)}k` : v;
  };

  return (
    <ControleurLayout pageTitle="Comparaison">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Comparer les médias</h1>
      <p className="page-subtitle">Analyses croisées entre médias sélectionnés</p>

      {/* Sélecteur médias + période */}
      <div className="card comparaison-filters" style={{ marginTop: 24 }}>
        <div className="comp-filter-label">Sélectionner les médias à comparer</div>
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
          <select
            className="form-select comp-periode-select"
            value={periode}
            onChange={e => setPeriode(e.target.value)}
          >
            {PERIODES.map(p => <option key={p.value} value={p.value}>{p.label}</option>)}
          </select>
        </div>
      </div>

      {selected.length < 2 ? (
        <div className="comp-empty">Sélectionnez au moins 2 médias pour comparer.</div>
      ) : (
        <>
          {/* Graphiques */}
          <div className="charts-row" style={{ marginTop: 16 }}>
            {/* KPI comparatif */}
            <div className="card chart-card">
              <div className="chart-title-row">
                <div className="chart-title">Comparaison KPI</div>
                <div className="kpi-tabs">
                  {KPI_TABS.map(tab => (
                    <button
                      key={tab}
                      className={`kpi-tab${kpiTab === tab ? ' active' : ''}`}
                      onClick={() => setKpiTab(tab)}
                    >
                      {tab}
                    </button>
                  ))}
                </div>
              </div>
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={kpiChartData} layout="vertical" margin={{ left: 10, right: 20 }}>
                  <XAxis type="number" hide />
                  <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fill: '#6b7280' }} axisLine={false} tickLine={false} width={90} />
                  <Tooltip
                    formatter={v => fmtVal(v)}
                    contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                  />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {kpiChartData.map((entry, i) => (
                      <rect key={i} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
              <div className="comp-legend">
                {selectedData.map(m => (
                  <div key={m.nom} className="comp-legend-item">
                    <span className="comp-legend-dot" style={{ background: m.color }} />
                    <span>{m.nom} — {fmtVal(m[KPI_KEY[kpiTab]])}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Évolution croisée */}
            <div className="card chart-card">
              <div className="chart-title">Évolution croisée — {PERIODES.find(p => p.value === periode)?.label}</div>
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={semainesData} barCategoryGap="30%" barGap={3}>
                  <XAxis dataKey="sem" tick={{ fontSize: 12, fill: '#6b7280' }} axisLine={false} tickLine={false} />
                  <YAxis hide />
                  <Tooltip
                    formatter={v => fmtVal(v)}
                    contentStyle={{ border: '1px solid #e5e7eb', borderRadius: 8, fontSize: 12 }}
                  />
                  {selectedData.map(m => (
                    <Bar key={m.nom} dataKey={m.nom} fill={m.color} radius={[3, 3, 0, 0]} />
                  ))}
                </BarChart>
              </ResponsiveContainer>
              <div className="comp-legend">
                {selectedData.map(m => (
                  <div key={m.nom} className="comp-legend-item">
                    <span className="comp-legend-dot" style={{ background: m.color }} />
                    <span>{m.nom}</span>
                  </div>
                ))}
              </div>
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
                  <th>TAUX DE REBOND</th>
                </tr>
              </thead>
              <tbody>
                {selectedData.map(m => (
                  <tr key={m.nom}>
                    <td>
                      <div className="comp-table-media">
                        <span className="comp-legend-dot" style={{ background: m.color }} />
                        <span className="font-medium">{m.nom}</span>
                      </div>
                    </td>
                    <td>{m.visiteurs.toLocaleString('fr-FR')}</td>
                    <td>{m.pages_vues.toLocaleString('fr-FR')}</td>
                    <td>{m.duree_moy}</td>
                    <td>{m.scroll_moy}%</td>
                    <td>{m.taux_rebond}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </ControleurLayout>
  );
}
