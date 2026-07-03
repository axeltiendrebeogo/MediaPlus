import React, { useState, useEffect } from 'react';
import ControleurLayout from '../../components/ControleurLayout';
import ModalConfirmReaffectation from './modals/ModalConfirmReaffectation';
import api from '../../services/api';
import { mockAffectations } from '../../services/mockDataControleur';
import './ControleurAffectations.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

export default function ControleurAffectations() {
  const [data, setData] = useState(null);
  // selection locale: { mediaId -> { gestionnaire_id, gestionnaire_nom } }
  const [selections, setSelections] = useState({});
  const [pending, setPending] = useState({}); // mediaId -> bool (en cours de validation)
  const [success, setSuccess] = useState({}); // mediaId -> bool
  const [confirmModal, setConfirmModal] = useState(null); // { media, ancienGest, nouveauGestNom, nouveauGestId }

  useEffect(() => {
    if (USE_MOCK) {
      setData(mockAffectations);
      const init = {};
      mockAffectations.medias.forEach(m => {
        init[m.id] = { gestionnaire_id: m.gestionnaire_id, gestionnaire_nom: m.gestionnaire_nom };
      });
      setSelections(init);
    } else {
      Promise.all([
        api.get('/medias/'),
        api.get('/users/?role=gestionnaire&is_active=true'),
      ]).then(([mediasRes, gestRes]) => {
        const medias = mediasRes.data.results.map(m => ({
          ...m,
          initiales: m.gestionnaire_nom
            ? m.gestionnaire_nom.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
            : null,
        }));
        const gestionnaires_disponibles = gestRes.data.results.map(g => ({ id: g.id, nom: g.nom }));
        const stats = {
          avec_gestionnaire: medias.filter(m => m.gestionnaire_id).length,
          sans_gestionnaire: medias.filter(m => !m.gestionnaire_id).length,
          total: medias.length,
        };

        setData({ stats, medias, gestionnaires_disponibles });

        const init = {};
        medias.forEach(m => {
          init[m.id] = { gestionnaire_id: m.gestionnaire_id, gestionnaire_nom: m.gestionnaire_nom };
        });
        setSelections(init);
      });
    }
  }, []);

  const handleSelectChange = (mediaId, gestId, gestNom) => {
    setSelections(prev => ({ ...prev, [mediaId]: { gestionnaire_id: gestId || null, gestionnaire_nom: gestNom || null } }));
    setSuccess(prev => ({ ...prev, [mediaId]: false }));
  };

  const handleValider = (media) => {
    const sel = selections[media.id];
    const actuel = data.medias.find(m => m.id === media.id);
    const isReaffectation = actuel.gestionnaire_id && sel.gestionnaire_id && actuel.gestionnaire_id !== sel.gestionnaire_id;

    if (isReaffectation) {
      setConfirmModal({
        media,
        ancienGestionnaire: actuel.gestionnaire_nom,
        nouveauGestionnaire: sel.gestionnaire_nom,
        nouveauGestId: sel.gestionnaire_id,
      });
    } else {
      doAffectation(media.id, sel.gestionnaire_id, sel.gestionnaire_nom);
    }
  };

  const doAffectation = async (mediaId, gestId, gestNom) => {
    setPending(prev => ({ ...prev, [mediaId]: true }));
    try {
      if (!USE_MOCK) {
        await api.patch(`/medias/${mediaId}/`, { gestionnaire_id: gestId });
      }
      // Mise à jour locale
      setData(prev => ({
        ...prev,
        medias: prev.medias.map(m =>
          m.id === mediaId
            ? { ...m, gestionnaire_id: gestId, gestionnaire_nom: gestNom, initiales: gestNom ? gestNom.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase() : null }
            : m
        ),
        stats: {
          ...prev.stats,
          avec_gestionnaire: prev.medias.filter(m => m.id === mediaId ? !!gestId : !!m.gestionnaire_id).length,
          sans_gestionnaire: prev.medias.filter(m => m.id === mediaId ? !gestId : !m.gestionnaire_id).length,
        }
      }));
      setSuccess(prev => ({ ...prev, [mediaId]: true }));
      setTimeout(() => setSuccess(prev => ({ ...prev, [mediaId]: false })), 2500);
    } finally {
      setPending(prev => ({ ...prev, [mediaId]: false }));
      setConfirmModal(null);
    }
  };

  if (!data) return (
    <ControleurLayout pageTitle="Affectations">
      <div className="loading-state">Chargement…</div>
    </ControleurLayout>
  );

  const { stats, medias, gestionnaires_disponibles } = data;

  return (
    <ControleurLayout pageTitle="Affectations">
      <div className="page-eyebrow">ESPACE CONTRÔLEUR</div>
      <h1 className="page-title">Affectation des gestionnaires</h1>
      <p className="page-subtitle">Affecter, réaffecter ou retirer un gestionnaire pour chaque média</p>

      {/* Stats */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 14, marginTop: 24 }}>
        <div className="kpi-card card">
          <div className="kpi-label">MÉDIAS AVEC GESTIONNAIRE</div>
          <div className="kpi-value">{stats.avec_gestionnaire}</div>
          <div className="kpi-delta" style={{ color: 'var(--color-success)' }}>• Affectés</div>
        </div>
        <div className="kpi-card card">
          <div className="kpi-label">SANS GESTIONNAIRE</div>
          <div className="kpi-value">{stats.sans_gestionnaire}</div>
          <div className="kpi-delta" style={{ color: 'var(--color-danger)' }}>⚠ À affecter</div>
        </div>
        <div className="kpi-card card">
          <div className="kpi-label">TOTAL MÉDIAS</div>
          <div className="kpi-value">{stats.total}</div>
          <div className="kpi-sub">Sur la plateforme</div>
        </div>
      </div>

      {/* Tableau affectations */}
      <div className="card" style={{ marginTop: 20, padding: 0, overflow: 'hidden' }}>
        <table className="table affectation-table">
          <thead>
            <tr>
              <th>MÉDIA</th>
              <th>GESTIONNAIRE ACTUEL</th>
              <th>MODIFIER L'AFFECTATION</th>
              <th>ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            {medias.map(media => {
              const sel = selections[media.id] || {};
              const hasChanged = sel.gestionnaire_id !== media.gestionnaire_id;
              const hasGest = !!media.gestionnaire_id;

              return (
                <tr key={media.id} className={!hasGest ? 'row-warning' : ''}>
                  {/* Média */}
                  <td>
                    <div className="affectation-media-name">{media.nom}</div>
                    <div className="affectation-media-sub">
                      {media.type_media.charAt(0).toUpperCase() + media.type_media.slice(1)} · {media.url}
                    </div>
                  </td>

                  {/* Gestionnaire actuel */}
                  <td>
                    {hasGest ? (
                      <div className="gestionnaire-cell">
                        <div className="gestionnaire-avatar">
                          {media.initiales}
                        </div>
                        <span>{media.gestionnaire_nom}</span>
                      </div>
                    ) : (
                      <span className="sans-gestionnaire">⚠ Sans gestionnaire</span>
                    )}
                  </td>

                  {/* Sélecteur */}
                  <td>
                    <select
                      className={`form-select affectation-select${!sel.gestionnaire_id ? ' select-warning' : ''}`}
                      value={sel.gestionnaire_id || ''}
                      onChange={e => {
                        const id = Number(e.target.value) || null;
                        const nom = gestionnaires_disponibles.find(g => g.id === id)?.nom || null;
                        handleSelectChange(media.id, id, nom);
                      }}
                    >
                      <option value="">— Retirer —</option>
                      {gestionnaires_disponibles.map(g => (
                        <option key={g.id} value={g.id}>{g.nom}</option>
                      ))}
                    </select>
                  </td>

                  {/* Action */}
                  <td>
                    {success[media.id] ? (
                      <span className="affectation-success">✓ Enregistré</span>
                    ) : (
                      <button
                        className={`btn btn-sm ${hasChanged ? 'btn-blue' : 'btn-secondary'}`}
                        disabled={pending[media.id] || !hasChanged}
                        onClick={() => handleValider(media)}
                      >
                        {pending[media.id] ? '…' : hasGest && hasChanged ? 'Valider' : !hasGest && sel.gestionnaire_id ? 'Affecter' : 'Valider'}
                      </button>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {confirmModal && (
        <ModalConfirmReaffectation
          media={confirmModal.media}
          ancienGestionnaire={confirmModal.ancienGestionnaire}
          nouveauGestionnaire={confirmModal.nouveauGestionnaire}
          onConfirm={() => doAffectation(confirmModal.media.id, confirmModal.nouveauGestId, confirmModal.nouveauGestionnaire)}
          onClose={() => setConfirmModal(null)}
        />
      )}
    </ControleurLayout>
  );
}
