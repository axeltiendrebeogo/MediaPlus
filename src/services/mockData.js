// Mock data — activated when REACT_APP_USE_MOCK=true

export const mockUser = {
  id: 1,
  nom: 'Sami Traoré',
  email: 'admin@mediapulse.bf',
  role: 'admin',
  media_id: null,
  media_nom: null,
  date_creation: '2025-01-01T00:00:00Z',
  is_active: true,
};

export const mockUsers = {
  count: 5,
  results: [
    { id: 2, nom: 'Fatou Diallo', email: 'fatou@rtb.bf', role: 'gestionnaire', media_id: 1, media_nom: 'RTB Online', date_creation: '2025-01-12T10:30:00Z', is_active: true },
    { id: 3, nom: 'Ibrahim Sawadogo', email: 'ibrahim@lefaso.bf', role: 'gestionnaire', media_id: 3, media_nom: 'Lefaso.net', date_creation: '2025-02-05T09:00:00Z', is_active: true },
    { id: 4, nom: 'Awa Coulibaly', email: 'awa@omega.bf', role: 'gestionnaire', media_id: 4, media_nom: 'Radio Omega', date_creation: '2025-03-10T14:00:00Z', is_active: true },
    { id: 5, nom: 'Moussa Kaboré', email: 'moussa@mediapulse.bf', role: 'controleur', media_id: null, media_nom: null, date_creation: '2025-01-08T08:00:00Z', is_active: true },
    { id: 6, nom: 'Aïcha Diallo', email: 'aicha@sidwaya.bf', role: 'gestionnaire', media_id: null, media_nom: null, date_creation: '2025-04-01T11:00:00Z', is_active: false },
  ],
};

export const mockMedias = {
  count: 4,
  results: [
    {
      id: 1, nom: 'RTB Online', url: 'rtb.bf', type_media: 'television', statut: 'actif',
      gestionnaire_id: 2, gestionnaire_nom: 'Fatou Diallo',
      visiteurs_mois: 12431, pages_indexees: 24,
      date_creation: '2025-01-10T00:00:00Z',
    },
    {
      id: 2, nom: 'Sidwaya Numérique', url: 'sidwaya.bf', type_media: 'presse', statut: 'actif',
      gestionnaire_id: null, gestionnaire_nom: null,
      visiteurs_mois: 31200, pages_indexees: 142,
      date_creation: '2025-01-15T00:00:00Z',
    },
    {
      id: 3, nom: 'Lefaso.net', url: 'lefaso.net', type_media: 'presse', statut: 'actif',
      gestionnaire_id: 3, gestionnaire_nom: 'Ibrahim Sawadogo',
      visiteurs_mois: 95700, pages_indexees: 890,
      date_creation: '2025-01-20T00:00:00Z',
    },
    {
      id: 4, nom: 'Radio Omega', url: 'omega.bf', type_media: 'radio', statut: 'inactif',
      gestionnaire_id: 4, gestionnaire_nom: 'Awa Coulibaly',
      visiteurs_mois: 8900, pages_indexees: 18,
      date_creation: '2025-02-01T00:00:00Z',
    },
  ],
};

export const mockDashboardAdmin = {
  medias_actifs: 4,
  medias_actifs_delta: 1,
  utilisateurs: 12,
  utilisateurs_delta: 3,
  visiteurs_total: 148000,
  visiteurs_delta_pct: 12,
  rapports: 7,
  rapports_delta: 2,
  trafic_7j: [
    { jour: 'Lun', pages_vues: 4200, visiteurs: 1800 },
    { jour: 'Mar', pages_vues: 5100, visiteurs: 2200 },
    { jour: 'Mer', pages_vues: 6800, visiteurs: 2900 },
    { jour: 'Jeu', pages_vues: 4900, visiteurs: 2100 },
    { jour: 'Ven', pages_vues: 7200, visiteurs: 3100 },
    { jour: 'Sam', pages_vues: 3800, visiteurs: 1600 },
    { jour: 'Dim', pages_vues: 3100, visiteurs: 1400 },
  ],
  sources_trafic: [
    { name: 'Recherche', value: 45 },
    { name: 'Direct', value: 28 },
    { name: 'Réseaux', value: 18 },
    { name: 'Autres', value: 9 },
  ],
  performances_medias: [
    { id: 1, nom: 'Lefaso.net', type_media: 'presse', gestionnaire_nom: 'Ibrahim Sawadogo', visiteurs_mois: 95700, statut: 'actif' },
    { id: 2, nom: 'Sidwaya Numérique', type_media: 'presse', gestionnaire_nom: null, visiteurs_mois: 31200, statut: 'actif' },
    { id: 3, nom: 'RTB Online', type_media: 'television', gestionnaire_nom: 'Fatou Diallo', visiteurs_mois: 12431, statut: 'actif' },
    { id: 4, nom: 'Radio Omega', type_media: 'radio', gestionnaire_nom: 'Awa Coulibaly', visiteurs_mois: 8900, statut: 'inactif' },
  ],
};
