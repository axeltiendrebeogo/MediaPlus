import React, { useState, useEffect, useRef } from 'react';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import api from '../../services/api';
import { mockRapportsGest } from '../../services/mockDataGestionnaire';
import './GestionnaireRapports.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const today = () => new Date().toISOString().slice(0, 10);
const monthAgo = () => {
  const d = new Date();
  d.setMonth(d.getMonth() - 1);
  return d.toISOString().slice(0, 10);
};

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('fr-FR', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export default function GestionnaireRapports() {
  const [mediaNom, setMediaNom] = useState('');
  const [rapports, setRapports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [dateDebut, setDateDebut] = useState(monthAgo());
  const [dateFin, setDateFin] = useState(today());
  const [inclureStats, setInclureStats] = useState(true);
  const [inclureGraphiques, setInclureGraphiques] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [progression, setProgression] = useState(0);
  const [error, setError] = useState('');
  const [downloading, setDownloading] = useState(null);
  const pollRef = useRef(null);

  // Charge les infos du gestionnaire + la liste des rapports
  useEffect(() => {
    if (USE_MOCK) {
      setMediaNom(mockRapportsGest.media_nom || 'Mon Média');
      setRapports(mockRapportsGest.rapports || []);
      setLoading(false);
      return;
    }
    Promise.all([
      api.get('/auth/me/'),
      api.get('/rapports/?ordering=-date_generation'),
    ]).then(([meRes, rapportsRes]) => {
      setMediaNom(meRes.data.media_nom || '');
      setRapports(rapportsRes.data.results || []);
    }).finally(() => setLoading(false));

    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, []);

  const pollStatut = (id) => {
    const start = Date.now();
    pollRef.current = setInterval(async () => {
      if (Date.now() - start > 130000) {
        clearInterval(pollRef.current);
        setError('Délai de génération dépassé. Vérifiez la liste des rapports.');
        setGenerating(false);
        return;
      }
      try {
        const r = await api.get(`/rapports/${id}/statut/`);
        setProgression(r.data.progression || 0);
        if (r.data.statut === 'pret') {
          clearInterval(pollRef.current);
          setGenerating(false);
          // Recharge la liste pour voir le nouveau rapport
          api.get('/rapports/?ordering=-date_generation').then(res => {
            setRapports(res.data.results || []);
          });
        } else if (r.data.statut === 'erreur') {
          clearInterval(pollRef.current);
          setError(r.data.message || 'Erreur lors de la génération.');
          setGenerating(false);
        }
      } catch { /* continue polling */ }
    }, 5000);
  };

  const handleGenerer = async () => {
    if (generating) return;
    setError('');
    setGenerating(true);
    setProgression(0);

    if (USE_MOCK) {
      let p = 0;
      const t = setInterval(() => {
        p += 20; setProgression(p);
        if (p >= 100) {
          clearInterval(t);
          setGenerating(false);
          const nouveau = {
            id: Date.now(),
            titre: `Rapport ${dateDebut.slice(0, 7)} — ${mediaNom}`,
            media_nom: mediaNom,
            periode_debut: dateDebut,
            periode_fin: dateFin,
            statut: 'pret',
            date_generation: new Date().toISOString(),
            genere_par_nom: 'Moi',
          };
          setRapports(prev => [nouveau, ...prev]);
        }
      }, 600);
      return;
    }

    try {
      const r = await api.post('/rapports/generer/', {
        type_rapport: 'media',
        periode_debut: dateDebut,
        periode_fin: dateFin,
        inclure_stats: inclureStats,
        inclure_graphiques: inclureGraphiques,
      });
      pollStatut(r.data.id);
    } catch (e) {
      const detail = e.response?.data?.detail || 'Erreur lors de la génération.';
      const retryAfter = e.response?.data?.retry_after;
      setError(retryAfter
        ? `${detail} Réessayez dans ${Math.ceil(retryAfter / 60)} minutes.`
        : detail
      );
      setGenerating(false);
    }
  };

  const handleDownload = async (rapport) => {
    if (USE_MOCK) { alert('Téléchargement PDF non disponible en mode démo.'); return; }
    setDownloading(rapport.id);
    try {
      const r = await api.get(`/rapports/${rapport.id}/export/`, { responseType: 'blob' });
      const url = URL.createObjectURL(new Blob([r.data], { type: 'application/pdf' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = `${rapport.titre || `rapport-${rapport.id}`}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert('Erreur lors du téléchargement.');
    } finally {
      setDownloading(null);
    }
  };

  if (loading) return (
    <GestionnaireLayout pageTitle="Mes rapports">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  return (
    <GestionnaireLayout pageTitle="Mes rapports">
      <div className="page-eyebrow">{mediaNom.toUpperCase()}</div>
      <h1 className="page-title">Mes rapports</h1>
      <p className="page-subtitle">Générez et consultez vos rapports d'analyse</p>

      {/* Formulaire de génération */}
      <div className="card rapport-form" style={{ marginTop: 24 }}>
        <div className="rapport-form-title">Générer un nouveau rapport</div>

        <div className="rapport-form-dates">
          <div className="form-group">
            <label className="form-label">Période — début</label>
            <input type="date" className="form-input" value={dateDebut}
              max={dateFin} onChange={e => setDateDebut(e.target.value)} disabled={generating} />
          </div>
          <div className="form-group">
            <label className="form-label">Période — fin</label>
            <input type="date" className="form-input" value={dateFin}
              max={today()} onChange={e => setDateFin(e.target.value)} disabled={generating} />
          </div>
        </div>

        <div className="form-group" style={{ marginTop: 14 }}>
          <label className="form-label">Inclure dans le rapport</label>
          <div className="rapport-toggles">
            <label className="toggle-label">
              <div className={`toggle-switch${inclureStats ? ' on' : ''}`}
                onClick={() => !generating && setInclureStats(p => !p)}>
                <div className="toggle-thumb" />
              </div>
              <span>Statistiques détaillées</span>
            </label>
            <label className="toggle-label">
              <div className={`toggle-switch${inclureGraphiques ? ' on' : ''}`}
                onClick={() => !generating && setInclureGraphiques(p => !p)}>
                <div className="toggle-thumb" />
              </div>
              <span>Graphiques</span>
            </label>
          </div>
        </div>

        {error && <div className="login-error" style={{ margin: '10px 0' }}>{error}</div>}

        {generating && (
          <div style={{ marginBottom: 10 }}>
            <div style={{ fontSize: 13, color: '#6b7280', marginBottom: 6 }}>
              Génération en cours… {progression}%
            </div>
            <div style={{ background: '#e5e7eb', borderRadius: 4, height: 6 }}>
              <div style={{ background: '#2563eb', width: `${progression}%`, height: 6, borderRadius: 4, transition: 'width 0.4s' }} />
            </div>
          </div>
        )}

        <button className="btn btn-primary btn-full" style={{ marginTop: 16 }}
          onClick={handleGenerer} disabled={generating}>
          {generating ? `⏳ Génération en cours… ${progression}%` : 'Générer le rapport'}
        </button>
      </div>

      {/* Liste des rapports */}
      <div className="rapports-list" style={{ marginTop: 20 }}>
        {rapports.length === 0 && (
          <div className="empty-state">Aucun rapport généré pour le moment.</div>
        )}
        {rapports.map(r => (
          <div key={r.id} className={`rapport-item card rapport-${r.statut}`}>
            <div className="rapport-item-header">
              <div>
                <div className="rapport-item-titre">{r.titre}</div>
                <div className="rapport-item-meta">
                  {r.periode_debut} → {r.periode_fin} · Généré par {r.genere_par_nom}
                </div>
                <div className="rapport-item-meta text-muted">
                  {formatDate(r.date_generation)}
                </div>
              </div>
              <span className={`badge ${r.statut === 'pret' ? 'badge-actif' : r.statut === 'erreur' ? 'badge-inactif' : 'badge-inactif'}`}>
                {r.statut === 'pret' ? '• Prêt' : r.statut === 'erreur' ? '✗ Erreur' : '⏳ En cours'}
              </span>
            </div>

            {r.statut === 'pret' && (
              <div className="rapport-item-footer" style={{ marginTop: 12 }}>
                <button className="btn btn-secondary btn-sm"
                  onClick={() => handleDownload(r)}
                  disabled={downloading === r.id}>
                  {downloading === r.id ? '…' : '↓ Exporter PDF'}
                </button>
              </div>
            )}

            {r.statut === 'erreur' && (
              <p className="rapport-erreur-msg">Erreur lors de la génération. Réessayez.</p>
            )}
          </div>
        ))}
      </div>
    </GestionnaireLayout>
  );
}