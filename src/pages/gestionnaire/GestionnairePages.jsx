import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import { mockPages, mockGestionnaireDashboard } from '../../services/mockDataGestionnaire';
import './GestionnairePages.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const TRIS = [
  { value: 'vues',  label: 'Trier par vues' },
  { value: 'duree', label: 'Trier par durée' },
  { value: 'scroll',label: 'Trier par scroll' },
  { value: 'date',  label: 'Trier par date' },
];

const DATES = [
  { value: '',      label: 'Toutes les dates' },
  { value: '7j',    label: '7 derniers jours' },
  { value: '30j',   label: '30 derniers jours' },
  { value: '3mois', label: '3 derniers mois' },
];

export default function GestionnairePages() {
  const [pages, setPages] = useState([]);
  const [recherche, setRecherche] = useState('');
  const [tri, setTri] = useState('vues');
  const [filtreDatee, setFiltreDate] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) setPages(mockPages);
    // sinon : api.get('/pages/').then(r => setPages(r.data.results))
  }, []);

  // Filtrage + tri côté client (en prod, ce serait côté serveur)
  const pagesFiltrees = pages
    .filter(p => p.titre.toLowerCase().includes(recherche.toLowerCase()))
    .sort((a, b) => {
      if (tri === 'vues')   return b.vues - a.vues;
      if (tri === 'scroll') return b.scroll - a.scroll;
      // durée : on compare les strings "Xm Ys" approximativement
      if (tri === 'duree') {
        const toSec = s => { const [m, sec] = s.split('m '); return Number(m) * 60 + Number(sec); };
        return toSec(b.duree) - toSec(a.duree);
      }
      return 0; // date : déjà triée
    });

  return (
    <GestionnaireLayout pageTitle="Pages web">
      <div className="page-eyebrow">{mockGestionnaireDashboard.media_nom.toUpperCase()}</div>
      <h1 className="page-title">Pages web</h1>
      <p className="page-subtitle">Liste de toutes les pages indexées sur votre média</p>

      {/* Filtres */}
      <div className="pages-filters" style={{ marginTop: 24 }}>
        <input
          className="form-input pages-search"
          placeholder="Rechercher une page…"
          value={recherche}
          onChange={e => setRecherche(e.target.value)}
        />
        <select className="form-select" value={filtreDatee} onChange={e => setFiltreDate(e.target.value)}>
          {DATES.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
        </select>
        <select className="form-select" value={tri} onChange={e => setTri(e.target.value)}>
          {TRIS.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
        </select>
      </div>

      {/* Tableau */}
      <div className="card" style={{ marginTop: 16, padding: 0, overflow: 'hidden' }}>
        <table className="table">
          <thead>
            <tr>
              <th>TITRE DE LA PAGE</th>
              <th>DATE</th>
              <th>VUES</th>
              <th>DURÉE</th>
              <th>SCROLL</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {pagesFiltrees.map(p => (
              <tr key={p.id}>
                <td className="font-medium">{p.titre}</td>
                <td className="text-muted">{p.date}</td>
                <td>{p.vues.toLocaleString('fr-FR')}</td>
                <td>{p.duree}</td>
                <td>
                  <div className="scroll-inline">
                    <div className="barre-track" style={{ width: 70 }}>
                      <div className="barre-fill" style={{ width: `${p.scroll}%`, background: '#2563eb' }} />
                    </div>
                    <span>{p.scroll}%</span>
                  </div>
                </td>
                <td>
                  <button
                    className="btn btn-secondary btn-sm"
                    onClick={() => navigate(`/gestionnaire/pages/${p.id}`)}
                  >
                    Analyser
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {pagesFiltrees.length === 0 && (
          <div className="empty-state">Aucune page ne correspond à votre recherche.</div>
        )}
      </div>
    </GestionnaireLayout>
  );
}
