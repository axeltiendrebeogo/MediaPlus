import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import ControleurLayout from '../../components/ControleurLayout';
import { mockControleurDashboard, mockRapports } from '../../services/mockDataControleur';
import './ControleurGenererRapport.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

const TYPE_RAPPORT = [
  { value: 'global', label: 'Rapport global (tous médias)' },
  { value: 'individuel', label: 'Rapport individuel (un média)' },
];

export default function ControleurGenererRapport() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [medias, setMedias] = useState([]);
  const [quota, setQuota] = useState(null);
  const [type, setType] = useState('global');
  const [selectedMedias, setSelectedMedias] = useState([]);
  const [dateDebut, setDateDebut] = useState('2025-03-01');
  const [dateFin, setDateFin] = useState('2025-03-31');
  const [sections, setSections] = useState({ statistiques: true, graphiques: true });
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (USE_MOCK) {
      const ms = mockControleurDashboard.performances.map(m => ({ id: m.id, nom: m.nom, color: m.color }));
      setMedias(ms);
      setQuota(mockRapports.quota);

      // Pré-sélection depuis query param ?media=
      const mediaParam = Number(searchParams.get('media'));
      if (mediaParam) {
        setType('individuel');
        setSelectedMedias([mediaParam]);
      } else {
        setSelectedMedias(ms.map(m => m.id));
      }
    }
  }, [searchParams]);

  const toggleMedia = id => {
    setSelectedMedias(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const toggleSection = key => {
    setSections(prev => ({ ...prev, [key]: !prev[key] }));
  };

  // Structure du rapport affiché à droite
  const structureItems = () => {
    const items = [{ label: 'En-tête (titre, période, date)', highlight: false }];
    const sel = type === 'global' ? medias : medias.filter(m => selectedMedias.includes(m.id));
    sel.forEach(m => items.push({ label: `Section ${m.nom} (KPI + graphiques)`, highlight: false }));
    if (type === 'global') items.push({ label: 'Comparaison croisée (G7 + G8)', highlight: true });
    return items;
  };

  const quotaAtteint = quota && quota.utilise >= quota.max;

  const handleGenerer = async () => {
    if (quotaAtteint) { setError('Quota atteint. Réessayez dans ' + quota.reset_dans + '.'); return; }
    if (selectedMedias.length === 0) { setError('Sélectionnez au moins un média.'); return; }
    setError('');
    setGenerating(true);
    try {
      if (!USE_MOCK) {
        await new Promise(r => setTimeout(r, 1200)); // fake delay
        // await api.post('/rapports/generer/', { type, medias: selectedMedias, date_debut: dateDebut, date_fin: dateFin, sections })
      } else {
        await new Promise(r => setTimeout(r, 1500));
      }
      setGenerated(true);
      setQuota(prev => ({ ...prev, utilise: prev.utilise + 1 }));
    } catch {
      setError('Une erreur est survenue lors de la génération.');
    } finally {
      setGenerating(false);
    }
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
            <button className="btn btn-blue" onClick={() => setGenerated(false)}>
              Générer un autre rapport
            </button>
          </div>
        </div>
      ) : (
        <div className="generer-layout" style={{ marginTop: 24 }}>
          {/* Paramètres */}
          <div className="card generer-params">
            <div className="generer-section-title">Paramètres du rapport</div>

            <div className="form-group" style={{ marginBottom: 16 }}>
              <label className="form-label">Type de rapport</label>
              <select
                className="form-select generer-type-select"
                value={type}
                onChange={e => {
                  setType(e.target.value);
                  setSelectedMedias(e.target.value === 'global' ? medias.map(m => m.id) : []);
                }}
              >
                {TYPE_RAPPORT.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
              </select>
            </div>

            <div className="form-group" style={{ marginBottom: 16 }}>
              <label className="form-label">Médias à inclure</label>
              <div className="comp-media-chips">
                {medias.map(m => (
                  <button
                    key={m.id}
                    type="button"
                    className={`media-chip${selectedMedias.includes(m.id) ? ' active' : ''}`}
                    style={selectedMedias.includes(m.id) ? { borderColor: m.color, background: m.color + '18', color: m.color } : {}}
                    onClick={() => toggleMedia(m.id)}
                  >
                    {m.nom}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 16 }}>
              <div className="form-group">
                <label className="form-label">Période — début</label>
                <input type="date" className="form-input" value={dateDebut} onChange={e => setDateDebut(e.target.value)} />
              </div>
              <div className="form-group">
                <label className="form-label">Période — fin</label>
                <input type="date" className="form-input" value={dateFin} onChange={e => setDateFin(e.target.value)} />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: 20 }}>
              <label className="form-label">Sections à inclure</label>
              <div className="sections-checks">
                {Object.entries({ statistiques: 'Statistiques', graphiques: 'Graphiques' }).map(([key, label]) => (
                  <label key={key} className="section-check">
                    <input
                      type="checkbox"
                      checked={sections[key]}
                      onChange={() => toggleSection(key)}
                    />
                    {label}
                  </label>
                ))}
              </div>
            </div>

            {error && <div className="login-error" style={{ marginBottom: 12 }}>{error}</div>}

            {quota && (
              <div className="quota-inline">
                <span>Quota : {quota.utilise}/{quota.max} rapports / 4h</span>
                {quota.utilise >= quota.max && (
                  <span className="quota-warn"> · Réinitialisation dans {quota.reset_dans}</span>
                )}
              </div>
            )}

            <button
              className="btn btn-primary btn-full"
              style={{ marginTop: 14 }}
              onClick={handleGenerer}
              disabled={generating || quotaAtteint}
            >
              {generating ? '⏳ Génération en cours…' : 'Générer le rapport'}
            </button>
          </div>

          {/* Structure prévisuelle */}
          <div className="generer-preview">
            <div className="card" style={{ padding: 20 }}>
              <div className="generer-section-title" style={{ marginBottom: 12 }}>Structure du rapport généré</div>
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
                Quota : {quota?.max || 3} rapports max / 4h. Les données de chaque média sont dans des sections séparées — jamais additionnées. La section "Comparaison croisée" est uniquement présente dans les rapports globaux.
              </p>
            </div>
          </div>
        </div>
      )}
    </ControleurLayout>
  );
}
