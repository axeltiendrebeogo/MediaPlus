# 📰 FasoHorizon - Plateforme Simulée pour Tests Métriques d'Audience

**FasoHorizon** est un site web d'actualités burkinabè entièrement statique et responsive. Il a été spécialement conçu pour servir de cible stable et d'environnement de test pour instrumenter un système externe de collecte de métriques d'audience (tracker JS et collecteur PHP externe).

---

## 🚀 Lancement Rapide en Local

Le site est conçu pour fonctionner sur n'importe quel serveur HTTP statique simple. 

Pour le lancer avec le serveur intégré de Python :
1. Ouvrez un terminal dans le dossier du projet.
2. Exécutez la commande suivante :
   ```bash
   python -m http.server 8000
   ```
3. Ouvrez votre navigateur et accédez à l'adresse : **[http://localhost:8000](http://localhost:8000)**

---

## 💉 Injection du Script de Tracking (Où et comment l'insérer)

Pour instrumenter FasoHorizon avec votre script de tracking, vous devez insérer votre balise `<script>` dans les fichiers HTML.

### 1. Structure d'Injection Directe
Chaque page générée possède une balise `<!-- EXTRA_TRACKING_SCRIPTS_PLACEHOLDER -->` située dans l'en-tête `<head>` juste avant la balise de fermeture `</head>`.

Exemple d'intégration dans chaque fichier HTML :
```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Titre de l'article - FasoHorizon</title>
    <link rel="stylesheet" href="assets/css/styles.css">
    
    <!-- Insérez votre balise ici, juste sous le placeholder -->
    <script src="http://mon-serveur/tracker.js"></script>
</head>
```

### 2. Emplacement dans les fichiers
*   **Fichiers racines** (ex: `index.html`, `politique.html`, `videos.html`, `contact.html`) :
    *   Le placeholder se situe généralement à la **ligne 9** ou **10**, juste avant le tag `</head>`.
*   **Fichiers articles** (dans le dossier `/articles/`, ex: `articles/video-siao-ouaga.html`) :
    *   Le placeholder se situe généralement à la **ligne 9** ou **10**, juste avant le tag `</head>`.

### 3. Injection Automatique (Script Python)
Pour éviter de modifier manuellement les 32 fichiers HTML générés, vous pouvez exécuter ce court script Python depuis la racine du projet pour injecter votre tracker automatiquement :

```python
import os

# Remplacez cette URL par celle de votre serveur
TRACKER_TAG = '<script src="http://mon-serveur/tracker.js"></script>'

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Injection au niveau du placeholder
            if '<!-- EXTRA_TRACKING_SCRIPTS_PLACEHOLDER -->' in content:
                updated = content.replace(
                    '<!-- EXTRA_TRACKING_SCRIPTS_PLACEHOLDER -->',
                    f'<!-- EXTRA_TRACKING_SCRIPTS_PLACEHOLDER -->\n    {TRACKER_TAG}'
                )
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated)
                print(f"[Injecté] {filepath}")
```

---

## 🎯 Cibles Clés pour Scrapers & Trackers (DOM Stable)

Tous les éléments interactifs possèdent des IDs et des classes stables et uniques :

*   **Newsletter Form** : `<form id="newsletter-form">`
    *   Email Input : `id="newsletter-email"`
    *   Submit Button : `id="newsletter-submit"`
*   **Contact Form** : `<form id="contact-form">`
    *   Champs : `id="contact-name"`, `id="contact-email"`, `id="contact-subject"`, `id="contact-message"`
    *   Submit : `id="contact-submit"`
*   **Formulaire de Commentaires d'Articles** : `<form id="comment-form-{slug}">` (situé au bas de chaque page d'article).
    *   Auteur : `id="comment-author"`
    *   Corps : `id="comment-text"`
    *   Bouton d'envoi : `id="comment-submit"`
*   **Lecteurs Vidéo Natifs HTML5** : `<video class="faso-video-player" id="video-player-{slug}">`
    *   Des attributs métadonnées stables sont insérés pour faciliter le tracking d'événement :
        *   `data-video-title` (Titre du reportage)
        *   `data-video-duration` (Durée fictive estimée pour les calculs de complétion)
*   **Boutons de partage social** (situés en haut et bas d'article) :
    *   Facebook : `id="share-fb-{slug}"`
    *   X / Twitter : `id="share-tw-{slug}"`
    *   WhatsApp : `id="share-wa-{slug}"`

---

## 🔍 Validation du Site

Pour lancer un diagnostic et s'assurer que tous les fichiers, liens internes, balises vidéo, et formulaires sont intègres :
```bash
python verify_site.py
```
Ce script validera l'absence de liens morts et confirmera la stabilité structurelle du DOM.
