import React, { useState, useEffect } from 'react';
import AdminLayout from '../../components/AdminLayout';
import api from '../../services/api';
import { mockMedias } from '../../services/mockData';
import ModalAjouterMedia from './modals/ModalAjouterMedia';
import ModalSupprimerMedia from './modals/ModalSupprimerMedia';
import './AdminMedias.css';

const USE_MOCK = process.env.REACT_APP_USE_MOCK === 'true';

function MediaCard({ media, onDelete }) {
  const hasGestionnaire = !!media.gestionnaire_nom;

  return (
    <div className="media-card card">
      <div className="media-card-header">
        <div>
          <div className="media-card-name">{media.nom}</div>
          <div className="media-card-url">{media.url}</div>
          <span className={`badge badge-${media.type_media}`}>
            {media.type_media.charAt(0).toUpperCase() + media.type_media.slice(1)}
          </span>
        </div>
        <span className={`badge badge-${media.statut}`}>
          • {media.statut.charAt(0).toUpperCase() + media.statut.slice(1)}
        </span>
      </div>

      <div className="media-card-stats">
        <div className="media-stat">
          <div className="media-stat-label">Visiteurs/mois</div>
          <div className="media-stat-val">{media.visiteurs_mois?.toLocaleString('fr-FR')}</div>
        </div>
        <div className="media-stat">
          <div className="media-stat-label">Pages indexées</div>
          <div className="media-stat-val">{media.pages_indexees}</div>
        </div>
      </div>

      <div className="media-card-footer">
        <div className={`media-gestionnaire${!hasGestionnaire ? ' missing' : ''}`}>
          {hasGestionnaire ? (
            <>
              <span>Gestionnaire : </span>
              <strong>{media.gestionnaire_nom}</strong>
            </>
          ) : (
            <>
              <span className="warning-icon">⚠</span>
              <span className="text-danger">Sans gestionnaire</span>
            </>
          )}
        </div>
        <button
          className="btn-icon-delete"
          title="Supprimer"
          onClick={() => onDelete(media)}
        >
          🗑
        </button>
      </div>

      {!hasGestionnaire && (
        <div className="media-no-gestionnaire-alert">
          Demandez au Contrôleur d'affecter un gestionnaire
        </div>
      )}

    </div>
  );
}

export default function AdminMedias() {
  const [medias, setMedias] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAjouter, setShowAjouter] = useState(false);
  const [mediaToDelete, setMediaToDelete] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      if (USE_MOCK) {
        setMedias(mockMedias.results);
      } else {
        const res = await api.get('/medias/');
        setMedias(res.data.results);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const handleDeleted = (id) => {
    setMedias(prev => prev.filter(m => m.id !== id));
    setMediaToDelete(null);
  };

  const handleCreated = (media) => {
    setMedias(prev => [media, ...prev]);
    setShowAjouter(false);
  };

  return (
    <AdminLayout pageTitle="Médias">
      <div className="page-header-row">
        <div>
          <div className="page-eyebrow">ADMINISTRATION</div>
          <h1 className="page-title">Médias</h1>
        </div>
        <button className="btn btn-secondary" onClick={() => setShowAjouter(true)}>
          Ajouter un média
        </button>
      </div>

      {loading ? (
        <div className="loading-state">Chargement…</div>
      ) : (
        <div className="medias-grid">
          {medias.map(m => (
            <MediaCard key={m.id} media={m} onDelete={setMediaToDelete} />
          ))}
        </div>
      )}

      {showAjouter && (
        <ModalAjouterMedia
          onClose={() => setShowAjouter(false)}
          onCreated={handleCreated}
        />
      )}

      {mediaToDelete && (
        <ModalSupprimerMedia
          media={mediaToDelete}
          onClose={() => setMediaToDelete(null)}
          onDeleted={handleDeleted}
        />
      )}
    </AdminLayout>
  );
}
