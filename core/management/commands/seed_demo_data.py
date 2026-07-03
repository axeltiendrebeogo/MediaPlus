"""
Commande de DÉVELOPPEMENT UNIQUEMENT — hors périmètre strict du CdC.

MediaPulse ne collecte pas de données lui-même (§1.2 du CdC) : en
production, Visiteur/Evenement/Page_web sont alimentés par le système de
collecte externe (Projet 1 du PFA). Tant que ce système n'existe pas /
n'est pas branché, cette commande simule des données réalistes pour
pouvoir développer et démontrer le back-end MediaPulse de façon autonome.

Usage :
    python manage.py seed_demo_data            # ajoute des données
    python manage.py seed_demo_data --reset     # vide tout et régénère
"""

import datetime as dt
import random

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from evenements.models import Evenement, Visiteur
from medias.models import Media
from pages.models import PageWeb
from rapports.models import Rapport
from users.models import User

OS_PAR_APPAREIL = {
    "mobile": ["Android", "iOS"],
    "desktop": ["Windows", "macOS", "Linux"],
    "tablette": ["iPadOS", "Android"],
}
NAVIGATEURS = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]

# Quelques points géographiques approximatifs au Burkina Faso (villes principales)
GEO_BF = [
    (12.3714, -1.5197),   # Ouagadougou
    (11.1781, -4.2979),   # Bobo-Dioulasso
    (12.7, -0.0333),      # Kaya
    (10.6, -4.7667),      # Banfora
    (13.0833, -1.0667),   # Ouahigouya
]

TITRES_ARTICLES = [
    "Élections régionales 2026 : résultats complets",
    "Économie : la croissance du secteur agricole en hausse",
    "Sécurité : nouvelles mesures annoncées par le gouvernement",
    "Culture : le FESPACO ouvre ses portes",
    "Sport : victoire des Étalons en match amical",
    "Santé : campagne de vaccination dans les régions",
    "Éducation : rentrée scolaire 2026 - ce qu'il faut savoir",
    "Infrastructure : ouverture de la nouvelle route Ouaga-Bobo",
    "Société : portrait d'un entrepreneur burkinabè",
    "International : sommet régional sur le climat",
    "Tech : le numérique au service de l'agriculture",
    "Justice : réforme du code pénal en discussion",
]
TITRES_VIDEOS = [
    "JT 20h — édition du jour",
    "Débat : enjeux économiques de la région",
    "Reportage : vie quotidienne à Ouagadougou",
    "Interview exclusive du ministre",
    "Match en replay : Étalons vs Lions",
]
TITRES_AUDIOS = [
    "Podcast : actualités de la semaine",
    "Émission matinale — invité spécial",
    "Chronique culturelle",
    "Débat radio : société et développement",
]
AUTEURS = ["Jean Kaboré", "Aïcha Sawadogo", "Moussa Traoré", "Fatimata Ouédraogo", "Issa Compaoré"]


class Command(BaseCommand):
    help = "Génère des données de démo (médias, pages, visiteurs, événements) pour le développement local."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true",
            help="Supprime les données de démo existantes avant de régénérer.",
        )
        parser.add_argument(
            "--jours", type=int, default=60,
            help="Nombre de jours d'historique d'événements à générer (défaut: 60).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write("Suppression des données existantes...")
            Evenement.objects.all().delete()
            Visiteur.objects.all().delete()
            Rapport.objects.all().delete()
            PageWeb.objects.all().delete()
            Media.objects.all().delete()
            User.objects.filter(role__in=["gestionnaire", "controleur"]).delete()

        users = self._creer_users()
        medias = self._creer_medias(users)
        pages = self._creer_pages(medias)
        visiteurs = self._creer_visiteurs(n=300)
        self._creer_evenements(pages, visiteurs, jours=options["jours"])

        self.stdout.write(self.style.SUCCESS(
            f"Terminé : {len(users)} utilisateurs, {len(medias)} médias, "
            f"{len(pages)} pages, {len(visiteurs)} visiteurs, "
            f"{Evenement.objects.count()} événements."
        ))
        self.stdout.write(self.style.WARNING(
            "Identifiants de test (mot de passe identique à l'email avant le @ + 'Pass123!') :"
        ))
        for u in users:
            self.stdout.write(f"  - {u.email}  [{u.role}]")

    def _creer_users(self):
        users = []
        if not User.objects.filter(role="admin").exists():
            users.append(User.objects.create_user(
                email="admin@mediapulse.bf", password="adminPass123!",
                nom="Administrateur", role="admin", is_staff=True, is_superuser=True,
            ))
        if not User.objects.filter(role="controleur").exists():
            users.append(User.objects.create_user(
                email="controleur@mediapulse.bf", password="controleurPass123!",
                nom="Issa Ouédraogo", role="controleur",
            ))

        noms_gestionnaires = [
            ("fatou@rtb.bf", "Fatou Diallo"),
            ("kofi@sidwaya.bf", "Kofi Mensah"),
            ("aicha@omega.bf", "Aïcha Kaboré"),
            ("ibrahim@lefaso.net", "Ibrahim Sawadogo"),
        ]
        for email, nom in noms_gestionnaires:
            if not User.objects.filter(email=email).exists():
                users.append(User.objects.create_user(
                    email=email, password="gestPass123!", nom=nom, role="gestionnaire",
                ))
        return users or list(User.objects.all())

    def _creer_medias(self, users):
        # Association explicite par email (et non par position de liste : la
        # Meta.ordering=["nom"] de User aurait décalé l'association attendue).
        EMAIL_PAR_MEDIA = {
            "rtb.bf": "fatou@rtb.bf",
            "sidwaya.bf": "kofi@sidwaya.bf",
            "omega.bf": "aicha@omega.bf",
            "lefaso.net": "ibrahim@lefaso.net",
        }
        specs = [
            ("RTB Online", "rtb.bf", Media.TypeMedia.TELEVISION),
            ("Sidwaya Numérique", "sidwaya.bf", Media.TypeMedia.PRESSE),
            ("Radio Omega", "omega.bf", Media.TypeMedia.RADIO),
            ("Lefaso.net", "lefaso.net", Media.TypeMedia.WEB),
        ]
        medias = []
        for nom, url, type_media in specs:
            media, _ = Media.objects.get_or_create(
                url=url, defaults={"nom": nom, "type_media": type_media}
            )
            if not media.gestionnaire_id:
                email = EMAIL_PAR_MEDIA.get(url)
                gestionnaire = User.objects.filter(email=email, role="gestionnaire").first()
                if gestionnaire:
                    media.gestionnaire = gestionnaire
                    media.save()
            medias.append(media)
        return medias

    def _creer_pages(self, medias):
        pages = []
        for media in medias:
            if media.type_media == Media.TypeMedia.TELEVISION:
                titres, duree_min, duree_max = TITRES_VIDEOS, 600, 2400
            elif media.type_media == Media.TypeMedia.RADIO:
                titres, duree_min, duree_max = TITRES_AUDIOS, 300, 3600
            else:
                titres, duree_min, duree_max = TITRES_ARTICLES, None, None

            for titre in titres:
                jours_passes = random.randint(0, 90)
                date_pub = timezone.now().date() - dt.timedelta(days=jours_passes)
                duree_contenu = random.randint(duree_min, duree_max) if duree_min else None
                page = PageWeb.objects.create(
                    nom=titre,
                    url=f"https://{media.url}/{titre.lower().replace(' ', '-').replace(':', '')[:40]}",
                    date_publication=date_pub,
                    auteur=random.choice(AUTEURS),
                    media=media,
                    duree_contenu=duree_contenu,
                )
                pages.append(page)
        return pages

    def _creer_visiteurs(self, n=300):
        visiteurs = []
        for _ in range(n):
            appareil = random.choices(
                ["mobile", "desktop", "tablette"], weights=[60, 30, 10]
            )[0]
            lat, lon = random.choice(GEO_BF)
            visiteurs.append(Visiteur(
                adresse_ip=f"{random.randint(10,200)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}",
                type_appareil=appareil,
                os=random.choice(OS_PAR_APPAREIL[appareil]),
                navigateur=random.choice(NAVIGATEURS),
                latitude=lat + random.uniform(-0.3, 0.3),
                longitude=lon + random.uniform(-0.3, 0.3),
                source_trafic=random.choices(
                    [c for c, _ in Visiteur.SourceTrafic.choices], weights=[45, 28, 18, 9]
                )[0],
            ))
        return Visiteur.objects.bulk_create(visiteurs)

    def _creer_evenements(self, pages, visiteurs, jours=60):
        maintenant = timezone.now()
        evenements = []

        # Poids horaires réalistes (creux la nuit, pics 8h, 12h, 19h-21h)
        poids_heures = [1, 1, 1, 1, 1, 2, 4, 8, 10, 7, 6, 8, 10, 7, 6, 6, 7, 8, 10, 12, 11, 8, 5, 2]

        for page in pages:
            est_av = page.duree_contenu is not None
            nb_visiteurs_page = random.randint(20, 150)
            visiteurs_page = random.sample(visiteurs, min(nb_visiteurs_page, len(visiteurs)))

            for visiteur in visiteurs_page:
                jour_offset = random.randint(0, jours - 1)
                heure = random.choices(range(24), weights=poids_heures)[0]
                date_heure = maintenant - dt.timedelta(
                    days=jour_offset,
                    hours=-(heure - maintenant.hour),
                    minutes=random.randint(0, 59),
                )
                date_heure = date_heure.replace(hour=heure, minute=random.randint(0, 59), second=random.randint(0, 59))

                # Vue de page (clic ou scroll)
                evenements.append(Evenement(
                    type_even=random.choice(["clic", "scroll"]),
                    date_heure=date_heure,
                    profondeur_scroll=random.randint(10, 100),
                    visiteur=visiteur,
                    page=page,
                ))

                # Pour les contenus audio/vidéo : événement de lecture/visionnage
                if est_av and random.random() < 0.7:
                    type_even = "visionnage" if page.media.type_media == Media.TypeMedia.TELEVISION else "lecture"
                    completion = random.betavariate(2, 1.5)  # biaisé vers une bonne complétion
                    duree_ecoute = int(page.duree_contenu * min(completion, 1.0))
                    evenements.append(Evenement(
                        type_even=type_even,
                        date_heure=date_heure + dt.timedelta(seconds=5),
                        duree_ecoute=duree_ecoute,
                        visiteur=visiteur,
                        page=page,
                    ))
                elif not est_av:
                    evenements.append(Evenement(
                        type_even=random.choice(["clic", "scroll"]),
                        date_heure=date_heure + dt.timedelta(seconds=random.randint(10, 240)),
                        duree_ecoute=random.randint(30, 400),
                        profondeur_scroll=random.randint(10, 100),
                        visiteur=visiteur,
                        page=page,
                    ))

        Evenement.objects.bulk_create(evenements, batch_size=1000)
