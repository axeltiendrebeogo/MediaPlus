// ── Données mock Gestionnaire ──
// Le gestionnaire ne voit que SON média (ici RTB Online, id=1)

export const mockGestionnaireDashboard = {
  media_nom: 'RTB Online',
  media_type: 'television',

  // Périodes disponibles
  periodes: ['7j', '30j', '3mois', 'annee'],

  // KPIs (valeurs pour la période 30j par défaut)
  kpis: {
    '7j':     { visiteurs: 3200,  pages_vues: 9800,  duree_moy: '3m 22s', scroll_moy: 61, visiteurs_delta: '+8.2%',  pages_delta: '+5.1%',  duree_delta: '+12s', scroll_delta: '-1%' },
    '30j':    { visiteurs: 12431, pages_vues: 38204, duree_moy: '3m 48s', scroll_moy: 64, visiteurs_delta: '+18.4%', pages_delta: '+12.1%', duree_delta: '+24s', scroll_delta: '-3%' },
    '3mois':  { visiteurs: 36200, pages_vues: 112000,duree_moy: '3m 35s', scroll_moy: 63, visiteurs_delta: '+22.1%', pages_delta: '+14.8%', duree_delta: '+18s', scroll_delta: '+1%' },
    'annee':  { visiteurs: 142000,pages_vues: 438000,duree_moy: '3m 41s', scroll_moy: 62, visiteurs_delta: '+31.2%', pages_delta: '+28.4%', duree_delta: '+32s', scroll_delta: '+2%' },
  },

  // Graphique visiteurs & pages vues
  trafic: {
    '7j': [
      { label: 'Lun', pages_vues: 1200, visiteurs: 420 },
      { label: 'Mar', pages_vues: 1580, visiteurs: 540 },
      { label: 'Mer', pages_vues: 2100, visiteurs: 710 },
      { label: 'Jeu', pages_vues: 1350, visiteurs: 460 },
      { label: 'Ven', pages_vues: 1900, visiteurs: 650 },
      { label: 'Sam', pages_vues: 870,  visiteurs: 290 },
      { label: 'Dim', pages_vues: 800,  visiteurs: 270 },
    ],
    '30j': [
      { label: 'S1', pages_vues: 8200, visiteurs: 2800 },
      { label: 'S2', pages_vues: 9500, visiteurs: 3200 },
      { label: 'S3', pages_vues: 11800,visiteurs: 3900 },
      { label: 'S4', pages_vues: 8700, visiteurs: 2900 },
    ],
    '3mois': [
      { label: 'Jan', pages_vues: 34000, visiteurs: 11200 },
      { label: 'Fév', pages_vues: 36500, visiteurs: 12000 },
      { label: 'Mar', pages_vues: 38200, visiteurs: 12431 },
    ],
    'annee': [
      { label: 'Avr', pages_vues: 28000, visiteurs: 9200 },
      { label: 'Mai', pages_vues: 31000, visiteurs: 10100 },
      { label: 'Jun', pages_vues: 29500, visiteurs: 9600 },
      { label: 'Jul', pages_vues: 27000, visiteurs: 8800 },
      { label: 'Aoû', pages_vues: 26000, visiteurs: 8400 },
      { label: 'Sep', pages_vues: 32000, visiteurs: 10500 },
      { label: 'Oct', pages_vues: 35000, visiteurs: 11400 },
      { label: 'Nov', pages_vues: 37000, visiteurs: 12100 },
      { label: 'Déc', pages_vues: 36000, visiteurs: 11800 },
      { label: 'Jan', pages_vues: 34000, visiteurs: 11200 },
      { label: 'Fév', pages_vues: 36500, visiteurs: 12000 },
      { label: 'Mar', pages_vues: 38200, visiteurs: 12431 },
    ],
  },

  // Répartition appareils
  appareils: [
    { label: 'Mobile',   pct: 62, color: '#2563eb' },
    { label: 'Desktop',  pct: 28, color: '#3b82f6' },
    { label: 'Tablette', pct: 10, color: '#bfdbfe' },
  ],

  // Sources de trafic
  sources: [
    { label: 'Recherche',       pct: 45 },
    { label: 'Direct',          pct: 28 },
    { label: 'Réseaux sociaux', pct: 18 },
  ],

  // Top pages
  top_pages: [
    { id: 1, titre: 'Élections régionales 2025 : résultats',  vues: 4821, duree: '4m 12s', scroll: 72, tendance: 'hausse' },
    { id: 2, titre: 'Économie : croissance de 6.2%',           vues: 3204, duree: '3m 45s', scroll: 61, tendance: 'hausse' },
    { id: 3, titre: 'FESPACO primé à Cannes',                  vues: 2891, duree: '5m 01s', scroll: 85, tendance: 'baisse' },
  ],
};

export const mockPages = [
  { id: 1,  titre: 'Élections régionales 2025 : résultats complets', date: '15 mars', vues: 4821, duree: '4m 12s', scroll: 72, tendance: 'hausse' },
  { id: 2,  titre: 'Économie : croissance de 6.2%',                   date: '14 mars', vues: 3204, duree: '3m 45s', scroll: 61, tendance: 'hausse' },
  { id: 3,  titre: 'Culture : FESPACO primé à Cannes',                date: '13 mars', vues: 2891, duree: '5m 01s', scroll: 85, tendance: 'baisse' },
  { id: 4,  titre: 'Sport : CAN 2025 — les qualifiés',                date: '12 mars', vues: 2540, duree: '2m 38s', scroll: 55, tendance: 'hausse' },
  { id: 5,  titre: 'Santé : campagne de vaccination nationale',        date: '11 mars', vues: 2103, duree: '3m 12s', scroll: 68, tendance: 'stable' },
  { id: 6,  titre: 'Politique : discours du chef de l\'État',         date: '10 mars', vues: 1987, duree: '4m 50s', scroll: 79, tendance: 'hausse' },
  { id: 7,  titre: 'Météo : prévisions de la saison des pluies',      date: '9 mars',  vues: 1654, duree: '1m 42s', scroll: 42, tendance: 'baisse' },
  { id: 8,  titre: 'Education : résultats du BAC 2025',               date: '8 mars',  vues: 1520, duree: '2m 28s', scroll: 58, tendance: 'stable' },
];

export const mockAnalysePage = {
  id: 1,
  media_nom: 'RTB Online',
  titre: 'Élections régionales 2025 : résultats complets',
  date_publication: '15 mars 2025',

  kpis: {
    vues_totales: 4821,
    duree_moy: '4m 12s',
    scroll_moy: 72,
    taux_rebond: 38,
    vues_delta: '+34%',
    duree_delta: '+28s',
    scroll_delta: '+8%',
    rebond_delta: '-4%',
  },

  // Visiteurs par heure (courbe)
  par_heure: [
    { h: '6h',  v: 12 }, { h: '8h',  v: 45 }, { h: '10h', v: 98 },
    { h: '12h', v: 210 },{ h: '14h', v: 185 },{ h: '16h', v: 160 },
    { h: '18h', v: 190 },{ h: '19h', v: 310 },{ h: '20h', v: 420 },
    { h: '21h', v: 380 },{ h: '22h', v: 210 },{ h: '0h',  v: 80 },
  ],
  pic_audience: 'Pic d\'audience entre 19h – 21h',

  // Profondeur de scroll
  scroll_sections: [
    { label: '0 – 25%',   pct: 92, color: '#2563eb' },
    { label: '25 – 50%',  pct: 74, color: '#3b82f6' },
    { label: '50 – 75%',  pct: 72, color: '#60a5fa' },
    { label: '75 – 100%', pct: 31, color: '#bfdbfe' },
  ],
};

export const mockRapportsGest = {
  media_nom: 'RTB Online',
  quota: { utilise: 1, max: 3, reset_dans: '3h 12m' },
  rapports: [
    {
      id: 1,
      titre: 'Rapport Mars 2025 — RTB Online',
      auteur: 'Fatou Diallo',
      date: '31 mars 2025',
      statut: 'pret',
      resume: 'RTB Online affiche une croissance soutenue avec +18% de visiteurs uniques ce mois. Le pic d\'audience se situe entre 19h et 21h, correspondant aux journaux télévisés…',
      recommandations: [
        'Publier les résumés du JT en format article pour capter l\'audience mobile.',
        'Renforcer la couverture des actualités locales (3× plus d\'engagement).',
      ],
    },
    {
      id: 2,
      titre: 'Rapport Fév. 2025 — RTB Online',
      auteur: 'Fatou Diallo',
      date: '28 fév. 2025',
      statut: 'erreur',
      erreur: 'La génération a dépassé le délai maximum de 120 secondes.',
    },
  ],
};
