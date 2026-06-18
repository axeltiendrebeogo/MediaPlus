import React, { useState, useEffect, useRef } from 'react';
import GestionnaireLayout from '../../components/GestionnaireLayout';
import { mockRapportsGest } from '../../services/mockDataGestionnaire';
import './GestionnaireRapports.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

export default function GestionnaireRapports() {
  const [data, setData] = useState(null);

  // Formulaire
  const [dateDebut, setDateDebut] = useState('2025-03-01');
  const [dateFin,   setDateFin]   = useState('2025-03-31');
  const [sections,  setSections]  = useState({ statistiques: true, graphiques: false });

  // État génération
  const [generating, setGenerating] = useState(false);
  const [pollSecs,   setPollSecs]   = useState(0);   // secondes écoulées
  const pollRef = useRef(null);

  useEffect(() => {
    if (USE_MOCK) setData(mockRapportsGest);
    // sinon : api.get('/rapports/').then(r => setData(r.data))
  }, []);

  // Nettoyage du polling au démontage
  useEffect(() => () => clearInterval(pollRef.current), []);

  const toggleSection = key => setSections(prev => ({ ...prev, [key]: !prev[key] }));

  const handleGenerer = async () => {
    if (generating) return;
    setGenerating(true);
    setPollSecs(0);

    // Polling toutes les 5s, jusqu'à 120s max (comme la maquette)
    let elapsed = 0;
    pollRef.current = setInterval(async () => {
      elapsed += 5;
      setPollSecs(elapsed);

      if (USE_MOCK) {
        // En mock : on simule une fin à 10s
        if (elapsed >= 10) {
          clearInterval(pollRef.current);
          setGenerating(false);
          const nouveau = {
            id: Date.now(),
            titre: `Rapport ${dateDebut.slice(0, 7)} — ${data.media_nom}`,
            auteur: 'Moi',
            date: new Date().toLocaleDateString('fr-FR'),
            statut: 'pret',
            resume: 'Rapport généré avec succès en mode simulation.',
            recommandations: ['Continuez votre excellent travail !'],
          };
          setData(prev => ({
            ...prev,
            rapports: [nouveau, ...prev.rapports],
            quota: { ...prev.quota, utilise: prev.quota.utilise + 1 },
          }));
        }
        return;
      }

      // En prod : on interroge le statut
      try {
        // const res = await api.get('/rapports/statut-dernier/');
        // if (res.data.statut === 'pret' || res.data.statut === 'erreur') { ... }
      } catch {}

      if (elapsed >= 120) {
        clearInterval(pollRef.current);
        setGenerating(false);
      }
    }, 5000);
  };

  if (!data) return (
    <GestionnaireLayout pageTitle="Mes rapports">
      <div className="loading-state">Chargement…</div>
    </GestionnaireLayout>
  );

  const quotaAtteint = data.quota.utilise >= data.quota.max;

  return (
    <GestionnaireLayout pageTitle="Mes rapports">
      <div className="page-eyebrow">{data.media_nom.toUpperCase()}</div>
      <h1 className="page-title">Mes rapports</h1>
      <p className="page-subtitle">Générez et consultez vos rapports d'analyse</p>

      {/* ── Formulaire de génération ── */}
      <div className="card rapport-form" style={{ marginTop: 24 }}>
        <div className="rapport-form-title">Générer un nouveau rapport</div>

        <div className="rapport-form-dates">
          <div className="form-group">
            <label className="form-label">Période — début</label>
            <input
              type="date" className="form-input"
              value={dateDebut} onChange={e => setDateDebut(e.target.value)}
              disabled={generating}
            />
          </div>
          <div className="form-group">
            <label className="form-label">Période — fin</label>
            <input
              type="date" className="form-input"
              value={dateFin} onChange={e => setDateFin(e.target.value)}
              disabled={generating}
            />
          </div>
        </div>

        <div className="form-group" style={{ marginTop: 14 }}>
          <label className="form-label">Inclure dans le rapport</label>
          <div className="rapport-toggles">
            {Object.entries({ statistiques: 'Statistiques', graphiques: 'Graphiques' }).map(([key, label]) => (
              <label key={key} className="toggle-label">
                <div
                  className={`toggle-switch${sections[key] ? ' on' : ''}`}
                  onClick={() => !generating && toggleSection(key)}
                >
                  <div className="toggle-thumb" />
                </div>
                <span>{label}</span>
              </label>
            ))}
          </div>
        </div>

        <button
          className="btn btn-primary btn-full"
          style={{ marginTop: 16 }}
          onClick={handleGenerer}
          disabled={generating || quotaAtteint}
        >
          {generating ? 'Génération en cours…' : quotaAtteint ? `Quota atteint — réinit. dans ${data.quota.reset_dans}` : 'Générer le rapport'}
        </button>
      </div>

      {/* ── Barre de progression polling ── */}
      {generating && (
        <div className="card poll-banner" style={{ marginTop: 12 }}>
          <div className="poll-spinner" />
          <span>
            Génération en cours… vérification toutes les 5 secondes.
            ({pollSecs} / 120s)
          </span>
        </div>
      )}

      {/* ── Liste des rapports ── */}
      <div className="rapports-list" style={{ marginTop: 20 }}>
        {data.rapports.map(r => (
          <div key={r.id} className={`rapport-item card rapport-${r.statut}`}>
            <div className="rapport-item-header">
              <div>
                <div className="rapport-item-titre">{r.titre}</div>
                <div className="rapport-item-meta">
                  Généré par {r.auteur} · {r.date}
                </div>
              </div>
              <span className={`badge ${r.statut === 'pret' ? 'badge-actif' : 'badge-erreur'}`}>
                {r.statut === 'pret' ? '• Prêt' : 'Erreur'}
              </span>
            </div>

            {r.statut === 'pret' && (
              <>
                <p className="rapport-resume">{r.resume}</p>

                {r.recommandations?.length > 0 && (
                  <div className="rapport-recommandations">
                    <div className="recommandations-label">RECOMMANDATIONS</div>
                    <ol className="recommandations-list">
                      {r.recommandations.map((rec, i) => (
                        <li key={i}>{rec}</li>
                      ))}
                    </ol>
                  </div>
                )}

                <div className="rapport-item-footer">
                  <button className="btn btn-secondary">↓ Exporter PDF</button>
                </div>
              </>
            )}

            {r.statut === 'erreur' && (
              <p className="rapport-erreur-msg">{r.erreur}</p>
            )}
          </div>
        ))}
      </div>
    </GestionnaireLayout>
  );
}
