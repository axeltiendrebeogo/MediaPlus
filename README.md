# MediaPulse — Back-end Django

Back-end de la plateforme MediaPulse (PFA — IGIT, École Polytechnique de
Ouagadougou), conforme au **Cahier des Charges v2.0** et au contrat API
fourni par l'équipe. Stack : Django 4.2 + Django REST Framework +
PostgreSQL + SimpleJWT + WeasyPrint.

---

## 1. Installation

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # puis éditer .env (voir §2)

python manage.py migrate
python manage.py seed_demo_data # données de démo — voir §4
python manage.py runserver
```

L'API est servie sur `http://localhost:8000/api/`.

## 2. Variables d'environnement (`.env`)

Voir `.env.example` pour la liste complète et des valeurs par défaut
raisonnables. Le point important : si `DATABASE_URL` n'est **pas** défini,
le projet retombe automatiquement sur **SQLite** (pratique pour développer
sans installer PostgreSQL localement). En production / pour le travail
d'équipe avec la base partagée, définir `DATABASE_URL` vers le PostgreSQL
réel (§1.2 et §2.1 du CdC : MediaPulse lit une base **partagée**, alimentée
par le système de collecte du Projet 1).

## 3. Structure du projet

Une app Django par domaine fonctionnel, comme demandé au §10.1 du CdC :

```
mediapulse_backend/   settings.py, urls.py racine
core/                  permissions par rôle, pagination, gestion d'erreurs
                       uniforme, commande seed_demo_data, dashboard admin
users/                 modèle User, auth JWT, CRUD comptes (Admin)
medias/                modèle Media, CRUD médias, affectation gestionnaire
pages/                 modèle Page_web, liste + stats détaillées par page
evenements/            modèles Visiteur/Evenement, endpoints /api/stats/*
rapports/              modèle Rapport, génération async, PDF, quota
templates/rapports/    template HTML → PDF (WeasyPrint)
```

Chaque app suit la convention `models.py` / `serializers.py` / `views.py`
/ `urls.py`, avec les calculs statistiques isolés dans des `services.py`
dédiés (§10.1 du CdC : *"tous les calculs statistiques dans un fichier
services.py dédié par app"*).

## 4. Données de démonstration

**MediaPulse ne collecte aucune donnée lui-même** (§1.2 du CdC) — en
production, `Visiteur`/`Evenement`/`Page_web` sont alimentés par le
système de collecte externe du **Projet 1** du PFA. Tant que celui-ci
n'est pas branché, une commande de seed simule des données réalistes :

```bash
python manage.py seed_demo_data            # ajoute des données
python manage.py seed_demo_data --reset    # vide tout et régénère
python manage.py seed_demo_data --jours 90 # historique plus long
```

Cela crée 4 médias, ~33 pages, 300 visiteurs et plusieurs milliers
d'événements répartis sur 60 jours, ainsi que les comptes de test :

| Email | Mot de passe | Rôle |
|---|---|---|
| admin@mediapulse.bf | adminPass123! | admin |
| controleur@mediapulse.bf | controleurPass123! | controleur |
| fatou@rtb.bf | gestPass123! | gestionnaire (RTB Online) |
| kofi@sidwaya.bf | gestPass123! | gestionnaire (Sidwaya Numérique) |
| aicha@omega.bf | gestPass123! | gestionnaire (Radio Omega) |
| ibrahim@lefaso.net | gestPass123! | gestionnaire (Lefaso.net) |

## 5. Décisions d'implémentation à connaître

### 5.1 — Conflits CdC ↔ contrat API, résolus en faveur du CdC

Le contrat API fourni et le CdC se contredisaient sur plusieurs points
concernant l'affectation des gestionnaires. **Le CdC fait foi** (directive
explicite) :

- `POST /api/users/` et `PATCH /api/users/:id/` : le champ `media_id` est
  **ignoré silencieusement**, même si le contrat API montre des exemples
  l'utilisant. Seul le Contrôleur affecte un gestionnaire, via
  `PATCH /api/medias/:id/` (§3.1/§8.3 du CdC).
- `POST /api/medias/` : idem, `gestionnaire_id` est ignoré à la création
  (le CdC §8.3 le dit explicitement : *"Crée un nouveau média (sans
  gestionnaire_id)"*).
- Un gestionnaire affecté à un nouveau média est **automatiquement retiré**
  de son média précédent (cohérent avec "responsable d'un seul média").

### 5.2 — Champs ajoutés au modèle de données (gaps du CdC)

Deux champs nécessaires aux calculs documentés étaient absents du modèle
de données §4 du CdC — ajoutés avec justification en commentaire dans le
code :

- `Visiteur.source_trafic` — sans lui, le graphique G2 (sources de trafic)
  est impossible à calculer. Le CdC lui-même le mentionne comme
  conditionnel (*"si disponible en base"*, §6.1).
- `Page_web.duree_contenu` — nécessaire au calcul du taux de complétion
  audio/vidéo (§5.5 : *"source : Evenement + Page_web"*), absent du modèle
  §4.3 documenté.

### 5.3 — Dashboard Admin sans données d'audience

Décision actée : le dashboard Admin n'affiche **aucune** statistique
d'audience (conforme à *"L'admin n'a aucun accès aux données analytiques"*,
§3.1/§9.2 du CdC). Un endpoint dédié, **hors contrat strict**, a été ajouté
pour les compteurs de gestion uniquement :

```
GET /api/admin/dashboard/   (Admin uniquement)
→ { medias_actifs, medias_total, utilisateurs_total,
    gestionnaires_total, medias_sans_gestionnaire, rapports_generes_total }
```

### 5.4 — Statistiques calculées en direct (pas de cache horaire)

Le CdC prévoit un recalcul horaire via Celery/cron (§2.2/§5.1). Ici, les
statistiques sont calculées **à la demande**, à chaque requête — toujours
exactes, et sans la complexité d'infrastructure de Celery/Redis pour un
projet de cette taille. `derniere_maj` reflète donc l'heure de la requête.
Si la volumétrie réelle l'exigeait un jour, les fonctions de
`evenements/services.py` sont le point d'entrée naturel à brancher
derrière une tâche planifiée + cache, sans changer les vues.

### 5.5 — Génération de rapports : thread Python, pas Celery

Pas de broker Celery/Redis disponible. La génération tourne dans un
thread Python en arrière-plan (`rapports/services.py`), ce qui donne un
vrai flux asynchrone (POST renvoie immédiatement, le front fait du
polling) sans infrastructure supplémentaire. `generate_rapport()` est
volontairement isolée de la vue HTTP : pour passer à Celery en
production, il suffit de la décorer avec `@shared_task` et de l'appeler
via `.delay()` au lieu de `Thread(...).start()`.

⚠️ **Limite connue** : avec SQLite (mode dev sans `DATABASE_URL`), des
générations de rapports concurrentes peuvent ralentir fortement
(verrouillage SQLite mono-écrivain). Avec PostgreSQL (cible de
production), ce n'est pas un problème. Le mécanisme de timeout (120s,
§7.5 du CdC) protège dans tous les cas contre un blocage permanent.

### 5.6 — Formules statistiques

Toutes les formules de calcul (visiteurs uniques, taux de rebond, scroll
moyen, etc.) suivent **à la lettre** les définitions du §5 du CdC, y
compris quand certaines semblent surprenantes (ex. "Pages vues" ne compte
que les événements `clic`/`scroll`, pas `lecture`/`visionnage` — c'est la
formule donnée par le CdC, appliquée telle quelle plutôt que réinterprétée).

## 6. Endpoints implémentés

Tous les endpoints du contrat API sont implémentés (auth, users, medias,
pages, stats, rapports) — voir le contrat API fourni pour le détail
complet des paramètres et formes de réponse. Un récapitulatif rapide :

```
POST   /api/token/                      Connexion
POST   /api/token/refresh/              Rafraîchir le token
POST   /api/auth/logout/                Déconnexion
GET    /api/auth/me/                    Profil connecté

GET    /api/users/                      Liste (Admin)
POST   /api/users/                      Créer un compte (Admin)
GET    /api/users/:id/                  Détail (Admin)
PATCH  /api/users/:id/                  Modifier (Admin)
DELETE /api/users/:id/                  Supprimer (Admin)

GET    /api/medias/                     Liste (Admin/Contrôleur)
POST   /api/medias/                     Créer (Admin)
GET    /api/medias/:id/                 Détail (Admin/Contrôleur)
PATCH  /api/medias/:id/                 Modifier — double comportement
                                         selon rôle (Admin: métier /
                                         Contrôleur: gestionnaire_id)
DELETE /api/medias/:id/?mode=hard|soft  Supprimer (Admin)

GET    /api/pages/                      Liste (Gest./Contr.)
GET    /api/pages/:id/                  Détail (Gest./Contr.)
GET    /api/pages/:id/stats/            Stats détaillées — G2,G3,G4,G5

GET    /api/stats/dashboard/            KPI + G1,G2,G3 (Gest./Contr.)
GET    /api/stats/global/               Stats tous médias (Contrôleur)
GET    /api/stats/audio-video/          Stats audio/vidéo — G6
GET    /api/stats/comparaison/          Comparaison multi-médias — G7,G8

GET    /api/rapports/                   Liste (Gest./Contr.)
POST   /api/rapports/generer/           Déclenche la génération (async)
GET    /api/rapports/:id/statut/        Polling (toutes les 5s)
GET    /api/rapports/:id/               Détail complet
GET    /api/rapports/:id/export/        Télécharger le PDF

GET    /api/admin/dashboard/            Compteurs de gestion (Admin) — voir §5.3
```

## 7. Tests rapides

Pas de suite de tests automatisés formelle pour l'instant (à ajouter —
bon prochain chantier : `pytest-django` avec un test par endpoint
critique). En attendant, chaque flux a été vérifié manuellement via le
client de test Django (`Client` de `django.test`) pendant le
développement : login/refresh/logout, permissions croisées par rôle,
CRUD médias avec double comportement du PATCH, calculs statistiques sur
données de démo, génération de rapport de bout en bout (média et
global), export PDF, quota 429.

## 8. ⚠️ À synchroniser avec le front-end

Le front-end (déjà poussé par ton binôme) contient des appels vers des
endpoints **TODO** dont les noms et formats ne correspondent pas
toujours à ce contrat (ex. `/dashboard/gestionnaire/` au lieu de
`/stats/dashboard/`, `gestionnaire_id` envoyé par l'Admin, durées
pré-formatées `"3m 48s"` au lieu de secondes brutes). Le back-end suit le
CdC à la lettre (décision actée en conversation) — c'est donc le
front-end qui doit être ajusté pour appeler les bons endpoints avec les
bonnes formes de données documentées ci-dessus et dans le contrat API.
