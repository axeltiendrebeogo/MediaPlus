// ── Données mock Contrôleur ──

export const mockControleurDashboard = {
  medias_suivis: 4,
  visiteurs_total: 148000,
  visiteurs_delta_pct: 11,
  pages_vues_total: 412000,
  pages_vues_delta_pct: 9,
  rapports_generes: 7,

  // Graphique empilé — trafic 7 jours par média
  trafic_7j: [
    { jour: 'Lun', lefaso: 12000, sidwaya: 8000, rtb: 3500, omega: 2200 },
    { jour: 'Mar', lefaso: 15000, sidwaya: 9500, rtb: 4100, omega: 2800 },
    { jour: 'Mer', lefaso: 19000, sidwaya: 11000, rtb: 5200, omega: 3100 },
    { jour: 'Jeu', lefaso: 13500, sidwaya: 8800, rtb: 3800, omega: 2500 },
    { jour: 'Ven', lefaso: 21000, sidwaya: 12500, rtb: 5800, omega: 3400 },
    { jour: 'Sam', lefaso: 10000, sidwaya: 6500, rtb: 2900, omega: 1900 },
    { jour: 'Dim', lefaso: 8500, sidwaya: 5200, rtb: 2400, omega: 1600 },
  ],

  // Mini-cartes par média
  performances: [
    { id: 1, nom: 'Lefaso.net',       type_media: 'presse',     visiteurs: 95700, scroll_moy: 61, color: '#2563eb' },
    { id: 2, nom: 'Sidwaya',          type_media: 'presse',     visiteurs: 31200, scroll_moy: 58, color: '#16a34a' },
    { id: 3, nom: 'RTB Online',       type_media: 'television', visiteurs: 12431, scroll_moy: 64, color: '#7c3aed' },
    { id: 4, nom: 'Radio Omega',      type_media: 'radio',      visiteurs: 8900,  scroll_moy: 55, color: '#f59e0b' },
  ],

  // Tableau comparatif
  tableau: [
    { id: 1, nom: 'Lefaso.net',       type_media: 'presse',     visiteurs: 95700,  pages_vues: 287000, duree_moy: '3m 12s', scroll_moy: 61 },
    { id: 2, nom: 'Sidwaya Numérique',type_media: 'presse',     visiteurs: 31200,  pages_vues: 98000,  duree_moy: '2m 58s', scroll_moy: 58 },
    { id: 3, nom: 'RTB Online',       type_media: 'television', visiteurs: 12431,  pages_vues: 38200,  duree_moy: '3m 48s', scroll_moy: 64 },
    { id: 4, nom: 'Radio Omega',      type_media: 'radio',      visiteurs: 8900,   pages_vues: 18500,  duree_moy: '5m 22s', scroll_moy: 55 },
  ],
};

export const mockComparaison = {
  // Données par média et par semaine pour le graphique croisé
  semaines: ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7'],
  medias: {
    1: {
      nom: 'Lefaso.net', color: '#2563eb',
      visiteurs: 95700, pages_vues: 287000, duree_moy: '3m 12s', scroll_moy: 61, taux_rebond: 42,
      par_semaine: { visiteurs: [12000, 16000, 18000, 14000, 19000, 10000, 6700], pages_vues: [38000, 48000, 54000, 42000, 57000, 30000, 18000], scroll: [60, 62, 63, 59, 64, 58, 61] },
    },
    2: {
      nom: 'Sidwaya Numérique', color: '#16a34a',
      visiteurs: 31200, pages_vues: 98000, duree_moy: '2m 58s', scroll_moy: 58, taux_rebond: 38,
      par_semaine: { visiteurs: [4000, 5200, 5800, 4500, 6000, 3200, 2500], pages_vues: [12500, 16000, 18000, 14000, 19000, 10000, 8500], scroll: [56, 59, 60, 57, 61, 55, 58] },
    },
    3: {
      nom: 'RTB Online', color: '#7c3aed',
      visiteurs: 12431, pages_vues: 38200, duree_moy: '3m 48s', scroll_moy: 64, taux_rebond: 35,
      par_semaine: { visiteurs: [1600, 2100, 2300, 1800, 2400, 1300, 931], pages_vues: [4900, 6500, 7100, 5600, 7400, 4000, 2700], scroll: [62, 65, 66, 63, 67, 61, 64] },
    },
    4: {
      nom: 'Radio Omega', color: '#f59e0b',
      visiteurs: 8900, pages_vues: 18500, duree_moy: '5m 22s', scroll_moy: 55, taux_rebond: 44,
      par_semaine: { visiteurs: [1100, 1500, 1600, 1300, 1700, 900, 800], pages_vues: [2300, 3100, 3300, 2700, 3500, 1900, 1700], scroll: [53, 56, 57, 54, 58, 52, 55] },
    },
  },
};

export const mockAffectations = {
  stats: { avec_gestionnaire: 3, sans_gestionnaire: 1, total: 4 },
  medias: [
    { id: 1, nom: 'RTB Online',        type_media: 'television', url: 'rtb.bf',      gestionnaire_id: 2, gestionnaire_nom: 'Fatou Diallo',    initiales: 'FD' },
    { id: 2, nom: 'Sidwaya Numérique', type_media: 'presse',     url: 'sidwaya.bf',  gestionnaire_id: null, gestionnaire_nom: null,            initiales: null },
    { id: 3, nom: 'Lefaso.net',        type_media: 'presse',     url: 'lefaso.net',  gestionnaire_id: 3, gestionnaire_nom: 'Ibrahim Sawadogo', initiales: 'IS' },
    { id: 4, nom: 'Radio Omega',       type_media: 'radio',      url: 'omega.bf',    gestionnaire_id: 4, gestionnaire_nom: 'Awa Coulibaly',    initiales: 'AC' },
  ],
  gestionnaires_disponibles: [
    { id: 2, nom: 'Fatou Diallo' },
    { id: 3, nom: 'Ibrahim Sawadogo' },
    { id: 4, nom: 'Awa Coulibaly' },
    { id: 6, nom: 'Kofi Mensah' },
  ],
};

export const mockRapports = {
  quota: { utilise: 1, max: 3, reset_dans: '3h 42m' },
  rapports: [
    { id: 1, titre: 'Rapport global — Mars 2025',    type: 'global',    medias: ['Lefaso.net', 'Sidwaya', 'RTB Online', 'Radio Omega'], periode: '01/03 – 31/03/2025', cree_le: '2025-04-02T09:15:00Z', statut: 'pret' },
    { id: 2, titre: 'Rapport Lefaso.net — Fév 2025', type: 'individuel', medias: ['Lefaso.net'],  periode: '01/02 – 28/02/2025', cree_le: '2025-03-05T14:20:00Z', statut: 'pret' },
    { id: 3, titre: 'Rapport RTB Online — Jan 2025', type: 'individuel', medias: ['RTB Online'],  periode: '01/01 – 31/01/2025', cree_le: '2025-02-03T11:00:00Z', statut: 'pret' },
  ],
};
