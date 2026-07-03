import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import ControleurLayout from '../../components/ControleurLayout';
import api from '../../services/api';
import { mockControleurDashboard, mockRapports } from '../../services/mockDataControleur';
import './ControleurGenererRapport.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const today = () => new Date().toISOString().slice(0, 10);
const monthAgo = () => {
  const d = new Date();
  d.setMonth(d.getMonth() - 1);
  return d.toISOString().slice(0, 10);
};

export default function ControleurGenererRapport() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const pollRef = useRef(null);

  const [medias, setMedias] = useState([]);
  const [type, setType] = useState('global');
  const [selectedMedias, setSelectedMedias] = useState([]);
  const [dateDebut, setDateDebut] = useState(monthAgo());
  const [dateFin, setDateFin] = useState(today());
  const [inclureStats, setInclureStats] = useState(true);
  const [inclureGraphiques, setInclureGraphiques] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [progression, setProgression] = useState(0);
  const [generated, setGenerated] = useState(false);
  const [rapportId, setRapportId] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (USE_MOCK) {
      const ms = mockControleurDashboard.performances?.map(m => ({ id: m.id, nom: m.nom }))
        || mockControleurDashboard.tableau?.map(m => ({ id: m.id, nom: m.nom }))
        || [];
      setMedias(ms);
      const mediaParam = Number(searchParams.get('media'));
      if (mediaParam) { setType('individuel'); setSelectedMedias([mediaParam]); }
      else setSelectedMedias(ms.map(m => m.id));
    } else {
      api.get('/medias/').then(r => {
        const ms = r.data.results.map(m => ({ id: m.id, nom: m.nom }));
        setMedias(ms);
        const mediaParam = Number(searchParams.get('media'));
        if (mediaParam) { setType('media'); setSelectedMedias([mediaParam]); }
        else { setType('global'); setSelectedMedias(ms.map(m => m.id)); }
      });
    }
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [searchParams]);

  const toggleMedia = id =>
    setSelectedMedias(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);

  const pollStatut = (id) => {
    const start = Date.now();
    pollRef.current = setInterval(async () => {
      if (Date.now() - start > 130000) {
        clearInterval(pollRef.current);
        setError('Délai dépassé. Vérifiez la liste des rapports.');
        setGenerating(false);
        return;
      }
      try {
        const r = await api.get(`/rapports/${id}/statut/`);
        setProgression(r.data.progression || 0);
        if (r.data.statut === 'pret') {
          clearInterval(pollRef.current);
          setGenerated(true);
          setGenerating(false);
          setRapportId(id);
        } else if (r.data.statut === 'erreur') {
          clearInterval(pollRef.current);
          setError(r.data.message || 'Erreur lors de la génération.');
          setGenerating(false);
        }
      } catch { /* continue polling */ }
    }, 5000);
  };

  const handleGenerer = async () => {
    setError('');
    if (!USE_MOCK && selectedMedias.length === 0) { setError('Sélectionnez au moins un média.'); return; }
    setGenerating(true);
    setProgression(0);

    if (USE_MOCK) {
      let p = 0;
      const t = setInterval(() => {
        p += 20;
        setProgression(p);
        if (p >= 100) { clearInterval(t); setGenerated(true); setGenerating(false); }
      }, 600);
      return;
    }

    try {
      const body = type === 'global'
        ? { type_rapport: 'global', medias_ids: selectedMedias, periode_debut: dateDebut, periode_fin: dateFin, inclure_stats: inclureStats, inclure_graphiques: inclureGraphiques }
        : { type_rapport: 'media', media_id: selectedMedias[0], periode_debut: dateDebut, periode_fin: dateFin, inclure_stats: inclureStats, inclure_graphiques: inclureGraphiques };

      const r = await api.post('/rapports/generer/', body);
      setRapportId(r.data.id);
      pollStatut(r.data.id);
    } catch (e) {
      const detail = e.response?.data?.detail || 'Erreur lors de la génération.';
      const retryAfter = e.response?.data?.retry_after;
      setError(retryAfter ? `${detail} Réessayez dans ${Math.ceil(retryAfter / 60)} minutes.` : detail);
      setGenerating(false);
    }
  };

  const structureItems = () => {
    const items = [{ label: 'En-tête (titre, période, date)' }];
    const sel = type === 'global'
      ? medias
      : medias.filter(m => selectedMedias.includes(m.id));
    sel.forEach(m => items.push({ label: `Section ${m.nom} (KPI + graphiques)`, highlight: false }));
    if (type === 'global') items.push({ label: 'Comparaison croisée (G7 + G8)', highlight: true });
    return items;
  };

  return (
    <ControleurLayout pageTitle="Générer rapport">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Générer un rapport</h1>
      <p className="page-subtitle">Rapport par média ou rapport global multi-médias</p>

      {generated ? (
        <div className="card rapport-success" style={{ marginTop: 24 }}>
          <div className="rapport-success-icon">✅</div>
          <h2>Rapport généré avec succès !</h2>
          <p>Votre rapport est disponible dans la liste des rapports.</p>
          <div style={{ display: 'flex', gap: 10, justifyContent: 'center', marginTop: 16 }}>
            <button className="btn btn-secondary" onClick={() => navigate('/controleur/rapports')}>
              Voir mes rapports
            </button>
            <button className="btn btn-blue" onClick={() => { setGenerated(false); setProgression(0); }}>
              Générer un autre rapport
            </button>
          </div>
        </div>
      ) : (
        <div className="generer-layout" style={{ marginTop: 24 }}>
          <div className="card generer-params">
            <div className="generer-section-title">Paramètres du rapport</div>

            <div className="form-group" style={{ marginBottom: 16 }}>
              <label className="form-label">Type de rapport</label>
              <select className="form-select" value={type}
                onChange={e => {
                  setType(e.target.value);
                  setSelectedMedias(e.target.value === 'global' ? medias.map(m => m.id) : []);
                }}>
                <option value="global">Rapport global (tous médias)</option>
                <option value="media">Rapport individuel (un média)</option>
              </select>
            </div>

            <div className="form-group" style={{ marginBottom: 16 }}>
              <label className="form-label">Médias à inclure</label>
              <div className="comp-media-chips">
                {medias.map(m => (
                  <button key={m.id} type="button"
                    className={`media-chip${selectedMedias.includes(m.id) ? ' active' : ''}`}
                    onClick={() => type === 'media' ? setSelectedMedias([m.id]) : toggleMedia(m.id)}>
                    {m.nom}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
              <div className="form-group">
                <label className="form-label">Période — début</label>
                <input type="date" className="form-input" value={dateDebut} max={dateFin}
                  onChange={e => setDateDebut(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Période — fin</label>
                <input type="date" className="form-input" value={dateFin} max={today()}
                  onChange={e => setDateFin(e.target.value)} />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: 20 }}>
              <label className="form-label">Sections à inclure</label>
              <div className="sections-checks">
                <label className="section-check">
                  <input type="checkbox" checked={inclureStats} onChange={e => setInclureStats(e.target.checked)} />
                  Statistiques détaillées
                </label>
                <label className="section-check">
                  <input type="checkbox" checked={inclureGraphiques} onChange={e => setInclureGraphiques(e.target.checked)} />
                  Graphiques
                </label>
              </div>
            </div>

            {error && <div className="login-error" style={{ marginBottom: 12 }}>{error}</div>}

            {generating && (
              <div style={{ marginBottom: 12 }}>
                <div style={{ fontSize: 13, color: '#6b7280', marginBottom: 6 }}>
                  Génération en cours… {progression}%
                </div>
                <div style={{ background: '#e5e7eb', borderRadius: 4, height: 6 }}>
                  <div style={{ background: '#2563eb', width: `${progression}%`, height: 6, borderRadius: 4, transition: 'width 0.4s' }} />
                </div>
              </div>
            )}

            <button className="btn btn-primary btn-full" style={{ marginTop: 8 }}
              onClick={handleGenerer} disabled={generating}>
              {generating ? '⏳ Génération en cours…' : 'Générer le rapport'}
            </button>
          </div>

          <div className="generer-preview">
            <div className="card" style={{ padding: 20 }}>
              <div className="generer-section-title" style={{ marginBottom: 12 }}>Structure du rapport</div>
              <div className="preview-items">
                {structureItems().map((item, i) => (
                  <div key={i} className={`preview-item${item.highlight ? ' highlight' : ''}`}>
                    {item.label}
                  </div>
                ))}
              </div>
            </div>
            <div className="card quota-info-card" style={{ padding: 16, marginTop: 12 }}>
              <p className="quota-info-text">
                Quota : 3 rapports max toutes les 4 heures. Les données de chaque média sont présentées dans des sections séparées — jamais additionnées.
              </p>
            </div>
          </div>
        </div>
      )}
    </ControleurLayout>
  );
}