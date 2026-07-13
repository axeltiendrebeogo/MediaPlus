import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import api from '../../services/api';
import { mockPages } from '../../services/mockDataGestionnaire';
import './GestionnairePages.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const TRIS = [
  { value: '-vues',          label: 'Trier par vues'       },
  { value: '-duree_moyenne', label: 'Trier par durée'      },
  { value: '-visiteurs',     label: 'Trier par visiteurs'  },
  { value: 'date_publication', label: 'Trier par date'     },
];

function formatDuree(s) {
  const sec = Math.round(s || 0);
  return `${Math.floor(sec / 60)}m ${(sec % 60).toString().padStart(2, '0')}s`;
}

function formatDate(iso) {
  if (!iso) return '—';
  const [y, m, d] = iso.split('-');
  return `${d}/${m}/${y}`;
}

function normaliserPage(p) {
  return {
    id: p.id,
    titre: p.nom,
    date: formatDate(p.date_publication),
    vues: p.vues || 0,
    visiteurs: p.visiteurs_uniques || 0,
    duree: formatDuree(p.duree_moyenne),
    scroll: p.scroll_moyen || 0,
  };
}

// Adapte l'ancien format mock (champs différents) à la même forme normalisée
function normaliserMock(p) {
  return {
    id: p.id,
    titre: p.titre,
    date: p.date,
    vues: p.vues || 0,
    visiteurs: p.visiteurs || 0,
    duree: p.duree || '0m 00s',
    scroll: p.scroll || 0,
  };
}

export default function GestionnairePages() {
  const [pages, setPages] = useState([]);
  const [mediaNom, setMediaNom] = useState('');
  const [recherche, setRecherche] = useState('');
  const [tri, setTri] = useState('-vues');
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (USE_MOCK) {
      setPages(mockPages.map(normaliserMock));
      setLoading(false);
      return;
    }
    // Charge la liste des pages (auto-filtrée au média du gestionnaire côté back)
    api.get(`/pages/?ordering=${tri}`).then(r => {
      setPages((r.data.results || []).map(normaliserPage));
    }).finally(() => setLoading(false));
  }, [tri]);

  // Charge le nom du média depuis /auth/me/ pour l'affichage
  useEffect(() => {
    if (!USE_MOCK) {
      api.get('/auth/me/').then(r => setMediaNom(r.data.media_nom || ''));
    } else {
      setMediaNom('Mon Média');
    }
  }, []);

  const pagesFiltrees = pages.filter(p =>
    p.titre.toLowerCase().includes(recherche.toLowerCase())
  );

  return (
    <GestionnaireLayout pageTitle="Pages web">
      <div className="page-eyebrow">{mediaNom.toUpperCase()}</div>
      <h1 className="page-title">Pages web</h1>
      <p className="page-subtitle">Liste de toutes les pages indexées sur votre média</p>

      <div className="pages-filters" style={{ marginTop: 24 }}>
        <input
          className="form-input pages-search"
          placeholder="Rechercher une page…"
          value={recherche}
          onChange={e => setRecherche(e.target.value)}
        />
        <select className="form-select" value={tri} onChange={e => setTri(e.target.value)}>
          {TRIS.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
        </select>
      </div>

      <div className="card" style={{ marginTop: 16, padding: 0, overflow: 'hidden' }}>
        {loading ? (
          <div className="loading-state">Chargement…</div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>TITRE DE LA PAGE</th>
                <th>DATE</th>
                <th>VUES</th>
                <th>VISITEURS</th>
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
                  <td>{p.visiteurs.toLocaleString('fr-FR')}</td>
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
              {pagesFiltrees.length === 0 && (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: 32, color: '#9ca3af' }}>
                    Aucune page ne correspond à votre recherche.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </GestionnaireLayout>
  );
}