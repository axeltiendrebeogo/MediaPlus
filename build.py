#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FasoHorizon - Static Site Generator
Generates a complete, beautiful Burkinabè news website for tracker testing.
Creates:
- Homepage (index.html)
- 6 Category pages (politique.html, economie.html, etc.)
- Multimedia/Video hub (videos.html)
- About & Contact pages (a-propos.html, contact.html)
- Legal notices (mentions-legales.html)
- 15 Standard articles inside articles/ directory
- 6 Video articles inside articles/ directory
"""

import os
import random
import urllib.request

# Ensure directories exist
os.makedirs('articles', exist_ok=True)
os.makedirs('assets/css', exist_ok=True)
os.makedirs('assets/js', exist_ok=True)
os.makedirs('assets/videos', exist_ok=True)

# Download sample open WebM videos for local hosting so Chromium/Playwright plays them without H.264 license problems
def download_sample_videos():
    video_map = {
        'flower.webm': 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.webm',
        'sample-5s.webm': 'https://samplelib.com/webm/sample-5s-360p.webm',
        'sample-10s.webm': 'https://samplelib.com/webm/sample-10s-360p.webm',
        'sample-15s.webm': 'https://samplelib.com/webm/sample-15s-360p.webm',
        'sample-20s.webm': 'https://samplelib.com/webm/sample-20s-360p.webm',
        'sample-30s.webm': 'https://samplelib.com/webm/sample-30s-360p.webm'
    }
    for filename, url in video_map.items():
        filepath = os.path.join('assets/videos', filename)
        if not os.path.exists(filepath):
            print(f"Téléchargement de {filename} depuis {url}...")
            try:
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
                )
                with urllib.request.urlopen(req) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
                print(f"Téléchargement réussi : {filename} ({os.path.getsize(filepath)} octets)")
            except Exception as e:
                print(f"Erreur de téléchargement pour {filename} : {e}")
                flower_path = os.path.join('assets/videos', 'flower.webm')
                if os.path.exists(flower_path) and filename != 'flower.webm':
                    print(f"Copie de flower.webm vers {filename} en guise de secours...")
                    import shutil
                    shutil.copy(flower_path, filepath)

download_sample_videos()

# Shared Navigation Menu Items
CATEGORIES = [
    {"slug": "politique", "label": "Politique", "badge": "badge-politique"},
    {"slug": "economie", "label": "Économie", "badge": "badge-economie"},
    {"slug": "societe", "label": "Société", "badge": "badge-societe"},
    {"slug": "sport", "label": "Sport", "badge": "badge-sport"},
    {"slug": "culture", "label": "Culture", "badge": "badge-culture"},
    {"slug": "international", "label": "International", "badge": "badge-international"},
    {"slug": "videos", "label": "Vidéos", "badge": "badge-videos"}
]

# Database of standard text articles
TEXT_ARTICLES = [
    {
        "slug": "transition-administration-reformes",
        "category": "politique",
        "title": "Réforme de l'Administration Publique : Quel bilan à mi-parcours pour la dématérialisation ?",
        "author": "Adama Ouédraogo",
        "date": "14 Juillet 2026",
        "img_id": "10", # Picsum photo ID
        "summary": "Lancée il y a dix-huit mois, la numérisation des démarches administratives visait à réduire la corruption et à fluidifier les dossiers des usagers. Entre avancées réelles et fractures numériques.",
        "content_blocks": [
            "L'administration publique burkinabè traverse une transformation sans précédent sous l'impulsion du plan stratégique national pour la dématérialisation. Initiée pour moderniser la fonction publique et simplifier la vie des citoyens, cette initiative suscite autant d'espoirs que de questionnements. En arpentant les couloirs du ministère de la Transition Digitale à Ouagadougou, l'enthousiasme des chefs de projet est palpable. Pourtant, sur le terrain, l'application concrète de ces réformes se heurte aux réalités d'une infrastructure réseau encore fragile.",
            "Selon le secrétariat permanent chargé des réformes administratives, plus de trente procédures clés ont été entièrement digitalisées. Il s'agit notamment de la demande de casier judiciaire, du dépôt de candidature aux concours de la fonction publique, et du paiement de certaines taxes municipales. Les autorités se félicitent d'un gain de temps considérable : là où il fallait parfois deux semaines et de multiples déplacements physiques pour obtenir un document officiel, quelques clics suffisent désormais.",
            "Pour le citoyen lambda, le changement est indéniable mais parfois difficile à appréhender. Rencontré devant le guichet unique de l'arrondissement de Bogodogo, Moussa Kaboré témoigne : 'C'est plus rapide si on maîtrise l'outil informatique et qu'on a une bonne connexion internet. Mais pour mes parents installés à Koudougou, sans assistance, cela devient un véritable parcours du combattant.' Cette fracture numérique est au cœur des débats parmi les syndicats de la fonction publique.",
            "<h2>Les défis de l'accès universel et de la connectivité</h2>",
            "La question des infrastructures énergétiques et de télécommunication reste le talon d'Achille de ce projet ambitieux. Si Ouagadougou et Bobo-Dioulasso bénéficient d'une couverture internet convenable, de nombreuses provinces demeurent des zones blanches numériques. Sans électricité stable ni réseau haut débit, la dématérialisation risque de creuser le fossé entre les centres urbains et le Burkina rural.",
            "Des experts en cybersécurité tirent également la sonnette d'alarme sur la protection des données personnelles collectées sur ces plateformes. Bien que l'Agence Nationale de Sécurité des Systèmes d'Information (ANSSI) assure avoir mis en place des pare-feux robustes, les incidents mineurs de fuite d'informations survenus en début d'année incitent à la prudence. La formation continue des agents publics à la sécurité informatique s'avère donc impérative.",
            "<h2>Une réorganisation humaine profonde</h2>",
            "La transition vers le numérique ne se limite pas à l'installation d'ordinateurs et de logiciels. Elle implique une profonde réorganisation du travail humain. Certains agents craignent une dépersonnalisation du service public et une réduction d'effectifs à terme. La direction générale de la fonction publique se veut rassurante, affirmant que les postes ne seront pas supprimés mais réorientés vers des missions d'accompagnement direct et de conseil de proximité.",
            "blockquote: 'La dématérialisation n'est pas une fin en soi, c'est un outil pour rapprocher l'État de ses citoyens, en particulier les plus vulnérables. Nous devons veiller à ce que personne ne soit laissé au bord de la route numérique.' - Allocution de la Ministre lors du dernier conseil sectoriel.",
            "En conclusion, le bilan à mi-parcours de la dématérialisation administrative au Burkina Faso présente un caractère contrasté. Les gains d'efficacité pour les usagers urbains et les finances publiques sont indéniables. Néanmoins, la réussite globale du projet dépendra de la capacité du gouvernement à déployer des réseaux résilients sur l'ensemble du territoire et à accompagner les populations les moins technophiles dans cette nouvelle ère numérique."
        ]
    },
    {
        "slug": "mines-or-enjeux-ecologiques",
        "category": "economie",
        "title": "Mines d'or au Burkina Faso : La double réalité économique et environnementale",
        "author": "Mariam Sawadogo",
        "date": "13 Juillet 2026",
        "img_id": "11",
        "summary": "Premier produit d'exportation du pays, l'or contribue massivement au budget national. Toutefois, les dégâts écologiques sur les sols et les nappes phréatiques inquiètent de plus en plus les populations riveraines.",
        "content_blocks": [
            "Le sous-sol burkinabè regorge d'or, et l'industrie minière s'est imposée en moins de deux décennies comme le moteur central de l'économie nationale. Représentant plus de 70% des recettes d'exportation et contribuant de manière significative au Produit Intérieur Brut (PIB), le métal précieux fait vivre des milliers de ménages. De Houndé à Essakane, les complexes miniers à ciel ouvert ont redessiné le paysage et stimulé le commerce local. Mais derrière les chiffres flatteurs se cache une urgence écologique grandissante.",
            "L'extraction de l'or à grande échelle consomme d'importantes quantités d'eau et utilise des substances chimiques hautement toxiques comme le cyanure et le mercure pour séparer le métal précieux de la roche. Bien que les compagnies minières industrielles affirment respecter les normes environnementales les plus strictes en confinant ces résidus dans des bassins étanches, les craintes de contamination des nappes phréatiques sont quotidiennes pour les communautés vivant en aval.",
            "<h2>L'impact direct sur l'agriculture et les sols</h2>",
            "Dans les zones minières, la pression foncière est immense. Des terres agricoles fertiles sont régulièrement réquisitionnées pour l'extension des concessions, privant les paysans de leurs moyens de subsistance traditionnels. Bien que des compensations financières soient versées, beaucoup estiment qu'elles ne compensent pas la perte d'un patrimoine productif transmissible aux générations futures. De plus, la déforestation accrue et le tassement des sols perturbent le cycle de l'eau.",
            "L'orpaillage artisanal, souvent informel ou clandestin, pose des problèmes environnementaux encore plus graves. Utilisant le mercure sans aucune protection, des milliers d'orpailleurs s'exposent eux-mêmes à de graves maladies neurologiques tout en polluant durablement les cours d'eau locaux. Les tentatives de régulation par l'Agence Nationale de l'Encadrement des Exploitations Minières Artisanales et Semi-Mécanisées (ANEEMAS) tardent à porter leurs fruits faute de moyens de contrôle suffisants.",
            "blockquote: 'L'or doit briller pour tous les Burkinabè, y compris pour nos enfants qui hériteront de cette terre. Si nous extrayons toute la richesse sous nos pieds en empoisonnant l'eau et en détruisant les forêts, nous fabriquons une fausse prospérité.' - Dr. Souleymane Diallo, chercheur en sciences de l'environnement.",
            "<h2>Des retombées fiscales locales contestées</h2>",
            "La loi minière de 2015 a instauré le Fonds Minier de Développement Local (FMDL), destiné à financer des projets d'infrastructures sociales (écoles, dispensaires, forages) dans les communes abritant les sites d'extraction. Si ce fonds a permis de réaliser d'importants investissements, sa gouvernance suscite de vifs débats. Des comités locaux dénoncent parfois des lenteurs bureaucratiques dans le déblocage des fonds ou un manque de transparence dans le choix des projets prioritaires.",
            "Pour inverser la tendance, des organisations de la société civile plaident pour un renforcement des études d'impact environnemental indépendantes et une transition progressive vers des technologies d'extraction sans mercure ni cyanure. Ils estiment que la souveraineté économique du Burkina Faso ne doit pas se faire au détriment de sa sécurité environnementale à long terme."
        ]
    },
    {
        "slug": "education-filles-zones-periurbaines",
        "category": "societe",
        "title": "Éducation au Burkina : La scolarisation des filles gagne du terrain dans le périurbain de Ouaga",
        "author": "Fidèle Kaboré",
        "date": "12 Juillet 2026",
        "img_id": "12",
        "summary": "Grâce aux campagnes de sensibilisation et à la gratuité scolaire progressive, le taux d'inscription des filles dans les collèges de la périphérie de la capitale affiche une hausse encourageante.",
        "content_blocks": [
            "Dans les quartiers périphériques de Ouagadougou, tels que Rimkiéta ou Saaba, l'éducation des filles connaît une révolution discrète mais profonde. Longtemps pénalisées par les tâches ménagères, les mariages précoces ou le manque de moyens financiers des familles, les jeunes filles accèdent désormais plus massivement aux cycles post-primaires et secondaires. Ce progrès est le fruit d'une synergie d'actions combinant politiques publiques volontaristes et initiatives communautaires locales.",
            "Dans le collège d'enseignement général de Rimkiéta, le taux de réussite des filles au Brevet d'Études du Premier Cycle (BEPC) a dépassé pour la première fois celui des garçons lors de la dernière session. La directrice de l'établissement attribue cette réussite à un changement profond de mentalité au sein des foyers : 'Avant, lorsqu'une famille traversait une crise financière, c'était la scolarité de la fille qui était immédiatement sacrifiée. Aujourd'hui, les parents comprennent que l'éducation d'une fille est un levier d'ascension sociale pour toute la famille.'",
            "<h2>L'appui crucial des bourses d'études et des kits scolaires</h2>",
            "La gratuité des frais de scolarité pour les filles jusqu'à l'âge de 16 ans, couplée à la distribution gratuite de manuels scolaires par le ministère de l'Éducation Nationale, a levé des obstacles économiques majeurs. Par ailleurs, des associations locales soutenues par des partenaires internationaux fournissent des bourses d'excellence aux élèves les plus méritantes issues de familles démunies. Ces bourses couvrent non seulement les fournitures scolaires, mais garantissent aussi un repas chaud quotidien au réfectoire.",
            "L'hygiène menstruelle en milieu scolaire, sujet longtemps tabou, a fait l'objet de projets de rénovation d'infrastructures. La construction de latrines séparées et équipées de points d'eau fonctionnels a permis de réduire drastiquement l'absentéisme mensuel des adolescentes. Une mesure technique simple, mais dont l'impact sur le parcours académique des élèves est majeur selon les rapports pédagogiques.",
            "blockquote: 'Étudier me permet de rêver d'un avenir meilleur. Je veux devenir médecin pour soigner les habitants de mon quartier. Mes parents m'encouragent chaque soir et me libèrent des corvées pour que je puisse réviser mes leçons.' - Balkissa Zongo, élève de 3ème à Saaba.",
            "<h2>Des obstacles subsistent en zone rurale reculée</h2>",
            "Malgré ces victoires encourageantes en zone périurbaine, la situation reste préoccupante dans les régions plus éloignées et touchées par l'insécurité. La fermeture d'écoles dans certaines provinces de l'Est et du Sahel perturbe gravement les trajectoires éducatives de milliers d'enfants. Les filles y sont particulièrement exposées, risquant l'abandon définitif de la scolarité au profit de mariages arrangés ou du travail informel.",
            "Le défi actuel consiste donc à répliquer les succès observés aux abords de la capitale dans les provinces les plus reculées, tout en sécurisant les espaces scolaires et en maintenant un accompagnement financier et social fort pour les familles vulnérables."
        ]
    },
    {
        "slug": "etalons-preparatifs-can-tactique",
        "category": "sport",
        "title": "Étalons du Burkina : Les grands chantiers tactiques en vue de la CAN 2027",
        "author": "Moussa Barro",
        "date": "11 Juillet 2026",
        "img_id": "13",
        "summary": "Après une série de matchs amicaux convaincants, le sélectionneur national peaufine son système de jeu. Objectif : stabiliser la défense et dynamiser l'animation offensive pour le grand rendez-vous continental.",
        "content_blocks": [
            "Le football burkinabè retient son souffle à l'approche des éliminatoires décisifs pour la Coupe d'Afrique des Nations (CAN) 2027. Les Étalons du Burkina Faso, portés par une génération de joueurs évoluant dans les plus grands championnats européens et africains, affichent des ambitions claires : ramener le trophée continental à Ouagadougou. Pour y parvenir, le staff technique mené par le sélectionneur national s'est lancé dans un vaste chantier de restructuration tactique.",
            "Les récentes confrontations amicales ont mis en lumière la nécessité d'une refonte du secteur défensif. Si la charnière centrale fait preuve de puissance physique, le positionnement sur les phases de transition rapide adverse a parfois fait défaut. Le sélectionneur insiste sur l'importance du bloc compact : 'Nous devons apprendre à souffrir ensemble et à boucher les intervalles plus rapidement. Le football moderne exige une rigueur de chaque instant.'",
            "<h2>L'animation offensive : Trouver la clé du verrou</h2>",
            "En phase offensive, le Burkina Faso dispose d'ailiers rapides capables d'éliminer en un contre un. Cependant, l'efficacité devant le but reste un problème récurrent. Le travail actuel se concentre sur les combinaisons dans les petits espaces et l'apport offensif des milieux de terrain relayeurs. L'intégration de jeunes talents issus du championnat local (Ligue 1 burkinabè) apporte une saine concurrence au sein de l'effectif.",
            "La préparation physique et mentale constitue un autre volet crucial. Les tournois continentaux se jouent sous des climats exigeants et imposent un enchaînement rapide des rencontres. Un staff médical renforcé a été recruté pour assurer la récupération optimale des joueurs, incluant des nutritionnistes et des préparateurs mentaux chargés de gérer la pression médiatique et populaire.",
            "blockquote: 'Porter le maillot des Étalons est un honneur immense mais aussi une grande responsabilité envers tout un peuple. Nous donnerons tout sur le terrain pour hisser haut les couleurs du Burkina Faso.' - Bertrand Traoré, capitaine de l'équipe nationale.",
            "<h2>Le soutien populaire, douzième homme indispensable</h2>",
            "Les supporters des Étalons, regroupés au sein de l'Union Nationale des Supporters des Étalons (UNSE), préparent activement leurs déplacements. L'engouement populaire autour de l'équipe nationale transcende les clivages politiques et sociaux, faisant du football un vecteur d'unité nationale exceptionnel. Les autorités sportives étudient actuellement des mesures de soutien pour faciliter l'accès aux billets et aux transports pour les fans désireux d'encourager l'équipe lors des matchs décisifs à l'extérieur.",
            "Le rendez-vous de 2027 s'annonce ainsi comme un test grandeur nature pour le football burkinabè. Les bases tactiques posées ces derniers mois devront rapidement être converties en résultats solides pour valider le ticket pour la phase finale et espérer décrocher la première étoile continentale de l'histoire du pays."
        ]
    },
    {
        "slug": "siao-artisanat-savoir-faire",
        "category": "culture",
        "title": "SIAO 2026 : Le savoir-faire des artisans burkinabè sous les projecteurs mondiaux",
        "author": "Amina Sanou",
        "date": "10 Juillet 2026",
        "img_id": "14",
        "summary": "Le Salon International de l'Artisanat de Ouagadougou bat son plein. Cette édition met en avant l'innovation dans le domaine du textile traditionnel Faso Dan Fani et de la sculpture sur bronze.",
        "content_blocks": [
            "Le Salon International de l'Artisanat de Ouagadougou (SIAO) s'est imposé au fil des décennies comme la vitrine majeure de la créativité et de l'ingéniosité africaines. Pour cette édition 2026, des milliers d'exposants venus de tout le continent et des acheteurs internationaux se pressent dans les pavillons d'exposition. Au centre de toutes les attentions, l'artisanat d'art burkinabè fait la démonstration de sa vitalité et de sa capacité à allier traditions ancestrales et tendances contemporaines.",
            "Le Faso Dan Fani, le célèbre pagne tissé en coton local, est sans conteste la star du salon. Longtemps cantonné aux tenues de cérémonie, il est aujourd'hui réinventé par de jeunes designers burkinabè et internationaux qui le déclinent en vestes modernes, accessoires de mode et objets de décoration intérieure. Le tissage manuel, exécuté majoritairement par des coopératives de femmes, bénéficie de nouvelles techniques de teinture naturelle à base de plantes locales.",
            "<h2>La sculpture sur bronze : L'art du feu et du métal</h2>",
            "Un autre secteur phare est la fonderie de bronze à la cire perdue, une tradition séculaire particulièrement vivante à Ouagadougou. Les bronziers burkinabè créent des œuvres d'une finesse remarquable, représentant des scènes de la vie quotidienne, des figures animales stylisées ou des sculptures abstraites monumentales. Chaque pièce est unique, façonnée dans la terre d'argile avant que le métal en fusion ne vienne prendre la place de la cire.",
            "Le salon met également en avant l'éco-artisanat. Face à la prolifération des déchets plastiques, plusieurs groupements d'artisans ont développé des techniques innovantes de recyclage. Les sachets plastiques usagés sont collectés, lavés, découpés puis tissés avec des fibres de coton ou de sisal pour créer des sacs et des paniers robustes et colorés. Une initiative saluée par le jury du salon pour son impact environnemental et social positif.",
            "blockquote: 'Le SIAO n'est pas seulement un lieu de commerce, c'est le conservatoire vivant de notre identité culturelle. Chaque objet acheté soutient directement une famille d'artisans et maintient un savoir-faire précieux en vie.' - Mamadou Zongo, bronzier d'art à Ouagadougou.",
            "<h2>Le défi de la commercialisation internationale</h2>",
            "Si la qualité artistique des œuvres est unanimement saluée, l'accès durable aux marchés internationaux demeure un défi de taille pour de nombreux petits producteurs. Les frais de transport élevés, les barrières douanières complexes et le manque de maîtrise des plateformes de commerce électronique limitent leur potentiel de vente. Des ateliers de formation sont organisés tout au long du salon pour aider les exposants à structurer leur offre commerciale et à utiliser les outils numériques.",
            "Le succès populaire et commercial du SIAO 2026 confirme le rôle stratégique de la culture et de l'artisanat comme moteurs de croissance économique et de rayonnement international pour le Burkina Faso. Une fierté nationale partagée qui résonne bien au-delà des frontières du pays."
        ]
    },
    {
        "slug": "uemoa-integration-douaniere-defis",
        "category": "international",
        "title": "Intégration Douanière dans l'UEMOA : Les transporteurs face aux réalités des corridors routiers",
        "author": "Ibrahim Barry",
        "date": "09 Juillet 2026",
        "img_id": "15",
        "summary": "Malgré les accords de libre-échange de l'Union Économique et Monétaire Ouest-Africaine, les tracasseries administratives et les taxes illégales ralentissent le trafic de marchandises entre Ouagadougou et les ports de la sous-région.",
        "content_blocks": [
            "L'Union Économique et Monétaire Ouest-Africaine (UEMOA) s'est donné pour objectif de créer un marché commun dynamique basé sur la libre circulation des personnes, des biens et des services. Pour un pays enclavé comme le Burkina Faso, le bon fonctionnement des corridors routiers reliant le territoire national aux ports de mer voisins (Abidjan, Lomé, Cotonou) est une question de sécurité économique vitale. Pourtant, les transporteurs routiers décrivent une réalité quotidienne éloignée des textes officiels de l'Union.",
            "Le transport de marchandises le long de ces corridors fait face à des obstacles persistants, communément appelés 'tracasseries routières'. Il s'agit des contrôles douaniers et policiers excessifs et non coordonnés, qui multiplient les arrêts obligatoires pour les chauffeurs routiers. Ces arrêts répétés s'accompagnent fréquemment de demandes de paiements informels, augmentant artificiellement le coût du transport et, par ricochet, les prix des produits de grande consommation sur les marchés d'Ouagadougou.",
            "<h2>Le coût économique des retards logistiques</h2>",
            "Selon l'Observatoire des Pratiques Anormales (OPA) de l'UEMOA, le temps perdu aux postes de contrôle routier représente un manque à gagner de plusieurs millions de francs CFA pour les entreprises de logistique chaque année. Un camion de fret reliant le port de Lomé à la capitale burkinabè met parfois plus d'une semaine pour accomplir un trajet de moins de mille kilomètres. Ces délais excessifs nuisent également à la compétitivité des produits d'exportation burkinabè comme la mangue fraîche ou le bétail sur pied.",
            "La mise en place de Postes de Contrôle Juxtaposés (PCJ) aux frontières communes visait à simplifier les formalités en regroupant les services de douane et de police des deux pays concernés dans un espace unique. Si certaines infrastructures sont fonctionnelles, d'autres tardent à être inaugurées ou souffrent d'un manque de coordination opérationnelle entre les administrations douanières concernées.",
            "blockquote: 'Nous demandons simplement l'application stricte des textes de l'UEMOA. La libre circulation ne doit pas rester un slogan politique, elle doit se traduire concrètement sur la route pour les transporteurs qui prennent des risques.' - Seydou Traoré, porte-parole du syndicat des conducteurs de poids lourds.",
            "<h2>Vers une numérisation des formalités douanières</h2>",
            "Face à ces défis, les États membres de l'UEMOA travaillent au déploiement de solutions numériques d'interconnexion des systèmes douaniers (comme le projet Sydonia World). L'objectif est de permettre un suivi électronique en temps réel des cargaisons sous douane depuis le port de départ jusqu'à la destination finale, éliminant ainsi le besoin de contrôles physiques répétés tout au long du trajet.",
            "L'accélération de ces réformes technologiques, doublée d'une volonté politique forte de lutter contre les pratiques anormales sur les axes routiers, est indispensable pour faire de l'espace UEMOA une zone économique véritablement intégrée et compétitive sur la scène continentale."
        ]
    },
    {
        "slug": "decentralisation-communes-rurales-budget",
        "category": "politique",
        "title": "Gouvernance Locale : Le budget participatif s'implante avec succès dans les communes rurales",
        "author": "Adama Ouédraogo",
        "date": "08 Juillet 2026",
        "img_id": "16",
        "summary": "Dans la province du Boulkiemdé, plusieurs municipalités testent une approche innovante impliquant directement les citoyens dans le choix des investissements publics prioritaires.",
        "content_blocks": [
            "La décentralisation au Burkina Faso franchit un nouveau palier grâce à l'expérimentation du budget participatif dans plusieurs communes de la région du Centre-Ouest. Cette démarche démocratique directe consiste à associer les citoyens à la prise de décision budgétaire en leur confiant le pouvoir d'orienter une partie des dépenses de investissement de leur municipalité. À Koudougou et dans les villages rattachés, le processus a permis d'apaiser les relations entre élus locaux et administrés.",
            "Le principe est simple : des assemblées villageoises sont organisées pour recueillir les besoins prioritaires des populations (construction d'une classe d'école, aménagement d'une piste agricole, forage d'un puits deau potable). Ensuite, des représentants élus au sein de ces comités villageois participent à des séances d'arbitrage budgétaire avec les services techniques de la mairie pour valider la faisabilité technique et financière des projets proposés.",
            "<h2>Une transparence accrue pour les impôts locaux</h2>",
            "L'un des impacts les plus notables de cette démarche est l'amélioration de la collecte des taxes municipales. Constatant que les fonds publics sont alloués à des projets qu'ils ont eux-mêmes décidés et dont ils suivent le chantier, les contribuables locaux se montrent plus enclins à s'acquitter de leurs taxes de marché ou de leurs redevances d'eau potable. Le civisme fiscal s'en trouve grandement renforcé.",
            "<h2>Les limites du modèle participatif</h2>",
            "Cependant, le budget participatif requiert du temps et des ressources d'animation importants pour s'assurer que toutes les franges de la population, notamment les femmes et les jeunes, participent activement aux débats. Par ailleurs, les ressources financières globales des communes rurales restant modestes, la frustration peut naître si trop peu de projets prioritaires sont financés au final.",
            "blockquote: 'Le budget participatif a changé notre regard sur la mairie. Nous ne sommes plus de simples spectateurs, nous sommes acteurs du développement de notre communauté.' - Alizéta Sawadogo, membre d'un comité villageois.",
            "L'exemple du Boulkiemdé suscite l'intérêt d'autres provinces burkinabè et de partenaires au développement, qui y voient un outil efficace pour renforcer la cohésion sociale et la légitimité démocratique des institutions locales dans un contexte de transition."
        ]
    },
    {
        "slug": "filiere-mangue-exportation-bio",
        "category": "economie",
        "title": "Agro-industrie : Le Burkina Faso renforce ses exportations de mangues séchées bio vers l'Europe",
        "author": "Mariam Sawadogo",
        "date": "07 Juillet 2026",
        "img_id": "17",
        "summary": "Grâce à la modernisation des unités de séchage et à l'obtention de certifications internationales équitables, les producteurs burkinabè valorisent l'or vert du verger national.",
        "content_blocks": [
            "La mangue burkinabè est réputée pour sa saveur unique et sa chair généreuse. Si l'exportation de mangues fraîches reste soumise aux aléas logistiques aériens et maritimes, la transformation locale sous forme de mangue séchée biologique connaît un essor spectaculaire. Cette activité à forte valeur ajoutée crée des milliers d'emplois, principalement féminins, dans les zones de production de Bobo-Dioulasso, Banfora et Orodara.",
            "Les unités de séchage se sont modernisées ces dernières années pour répondre aux exigences sanitaires rigoureuses des marchés extérieurs (notamment les normes bio européennes et américaines). L'abandon progressif des séchoirs artisanaux au profit de séchoirs à gaz ou solaires performants garantit une qualité homogène du produit fini, exempt d'impuretés et préservant les qualités nutritionnelles du fruit.",
            "<h2>L'impact social sur l'emploi féminin</h2>",
            "Le séchage de la mangue emploie une main-d'œuvre majoritairement féminine. Du pelage au parage en passant par le tri et l'emballage, des centaines de femmes trouvent dans ces unités industrielles saisonnières un revenu stable qui leur permet d'assurer les dépenses de santé et de scolarité de leurs enfants. Des coopératives se sont structurées pour reverser une part équitable du prix de vente directement aux productrices.",
            "Cependant, la filière reste confrontée au défi du coût élevé des emballages certifiés et des coûts énergétiques liés au séchage continu. De plus, les attaques récurrentes de la mouche des fruits sur les vergers continuent de menacer les volumes de récolte chaque année, appelant à des interventions phytosanitaires écologiques plus efficaces.",
            "blockquote: 'La mangue séchée est notre or à nous. Elle permet de valoriser les surplus de récolte qui pourrissaient auparavant sous les arbres et d'apporter de la richesse dans nos foyers.' - Assetou Coulibaly, présidente de coopérative à Banfora.",
            "Le renforcement de la marque de qualité 'Mangue du Burkina Faso' sur les marchés internationaux s'annonce comme une priorité pour pérenniser ces gains économiques et inciter les investisseurs à soutenir l'implantation de nouvelles usines de transformation dans le pays."
        ]
    },
    {
        "slug": "forages-solaires-acces-eau",
        "category": "societe",
        "title": "Accès à l'Eau Potable : Les forages solaires transforment le quotidien du Plateau Central",
        "author": "Fidèle Kaboré",
        "date": "06 Juillet 2026",
        "img_id": "18",
        "summary": "L'installation de pompes à motricité solaire remplace avantageusement les pompes manuelles fatiguées, offrant un accès continu à l'eau potable pour les populations rurales et le cheptel.",
        "content_blocks": [
            "Dans la région aride du Plateau Central du Burkina Faso, l'accès régulier à l'eau potable reste un défi quotidien. Traditionnellement, les villageois dépendent de forages équipés de pompes manuelles dont l'entretien est coûteux et le débit limité. L'arrivée des forages solaires de grande capacité constitue une avancée majeure, allégeant la pénibilité des corvées deau et sécurisant l'approvisionnement des foyers.",
            "Les nouveaux systèmes installés reposent sur des panneaux solaires photovoltaïques qui alimentent une pompe immergée. L'eau est pompée automatiquement pendant les heures d'ensoleillement et stockée dans un château d'eau surélevé. De là, elle est distribuée par gravité vers plusieurs bornes-fontaines réparties dans le village et vers des abreuvoirs aménagés pour le bétail, évitant les conflits d'usage.",
            "<h2>Une gestion communautaire de l'infrastructure</h2>",
            "La pérennité de ces infrastructures repose sur un modèle de gestion communautaire rigoureux. Un comité des usagers de l'eau est élu dans chaque village. Une participation financière symbolique est demandée aux familles lors de chaque prélèvement d'eau. Ce fonds d'entretien permet de rémunérer la fontainière, d'assurer la sécurité du site et de financer les futures réparations techniques ou le remplacement des filtres.",
            "<h2>Les bénéfices collatéraux pour le maraîchage</h2>",
            "Au-delà des besoins domestiques directs, la disponibilité de l'eau permet le développement de micro-projets de maraîchage. Autour des forages solaires, des groupements de femmes aménagent de petits périmètres irrigués où elles cultivent des tomates, des oignons et des choux, améliorant la sécurité nutritionnelle locale et générant des revenus complémentaires non négligeables.",
            "blockquote: 'Avec la pompe solaire, nous n'avons plus besoin de pomper pendant des heures sous le soleil brûlant. L'eau coule directement du robinet. Nos filles ont plus de temps pour aller à l'école.' - Fatimata Ouédraogo, fontainière à Ziniaré.",
            "Le déploiement à grande échelle de ces technologies propres s'avère être une réponse concrète et durable aux effets du dérèglement climatique au Sahel, garantissant le droit fondamental d'accès à l'eau pour tous."
        ]
    },
    {
        "slug": "patrimoine-tiebele-unesco-art-kassena",
        "category": "culture",
        "title": "Patrimoine Mondial : Tiébélé célèbre son inscription à l'UNESCO et prépare son avenir touristique",
        "author": "Amina Sanou",
        "date": "05 Juillet 2026",
        "img_id": "19",
        "summary": "La cour royale de Tiébélé, célèbre pour son architecture de terre et ses fresques murales traditionnelles peintes à la main par les femmes Kasséna, bénéficie d'une reconnaissance internationale historique.",
        "content_blocks": [
            "C'est une reconnaissance attendue depuis des années par le monde culturel burkinabè. La cour royale de Tiébélé, joyau de l'architecture traditionnelle Kasséna situé dans la province du Nahouri, fait désormais officiellement partie du Patrimoine Mondial de l'UNESCO. Cette inscription consacre la valeur universelle exceptionnelle de ces habitations de terre fortifiées, appelées soukhala, ornées de motifs géométriques peints par les femmes de la communauté.",
            "L'art mural de Tiébélé est un savoir-faire complexe transmis de mère en fille. Il utilise uniquement des matériaux naturels locaux : de l'argile rouge, du kaolin blanc et du charbon de bois noir, fixés à l'aide d'une décoction de cosses de néré qui imperméabilise les enduits. Les motifs peints ne sont pas de simples décorations ; ils représentent des symboles culturels profonds liés à la fertilité, à la protection et à la mythologie Kasséna.",
            "<h2>Un enjeu de préservation physique face au climat</h2>",
            "L'un des défis majeurs pour Tiébélé est la conservation physique de ces structures en terre face aux agressions climatiques. Les pluies torrentielles de la saison humide érodent les murs d'argile, nécessitant une réfection annuelle des peintures. L'inscription à l'UNESCO devrait permettre d'accéder à des financements internationaux pour former les jeunes aux techniques de restauration et de stabilisation des sols.",
            "<h2>Développer un tourisme respectueux et inclusif</h2>",
            "La communauté locale espère que cette vitrine internationale stimulera un écotourisme porteur d'emplois pour la jeunesse de la région. Des projets de guides locaux formés, d'hébergements chez l'habitant et d'ateliers d'initiation à la peinture traditionnelle sont à l'étude. Le respect des rituels et de la vie privée de la cour royale reste toutefois une priorité absolue de la gestion du site.",
            "blockquote: 'Cette inscription est une immense fierté pour notre peuple. C'est la preuve que notre culture de terre et nos traditions peintes ont une valeur pour l'humanité tout entière. Nous devons maintenant les protéger activement.' - Le porte-parole du chef de la cour royale Kasséna.",
            "L'inscription de Tiébélé démontre la richesse du patrimoine immatériel burkinabè et offre une opportunité unique de développement territorial durable par la valorisation de la culture et du tourisme local."
        ]
    },
    {
        "slug": "cyclisme-tour-du-faso-preparation-trace",
        "category": "sport",
        "title": "Tour du Faso 2026 : Un parcours renouvelé sous le signe de la cohésion nationale",
        "author": "Moussa Barro",
        "date": "04 Juillet 2026",
        "img_id": "20",
        "summary": "Les organisateurs de la plus grande course cycliste d'Afrique de l'Ouest dévoilent un tracé innovant qui traversera plusieurs provinces du pays pour célébrer le sport et la fraternité.",
        "content_blocks": [
            "Le Tour du Faso est bien plus qu'une simple compétition sportive ; c'est un monument de la culture populaire burkinabè. Chaque année, des millions de spectateurs massés le long des routes encouragent les coureurs sous une chaleur écrasante. Pour l'édition 2026, le comité d'organisation a préparé un tracé inédit qui ambitionne d'apporter l'effervescence de la caravane du Tour au plus près des populations des régions libérées.",
            "Le parcours comprendra dix étapes reliant plusieurs capitales régionales. Le grand départ sera donné à Bobo-Dioulasso, la ville de Sya, pour remonter ensuite vers Koudougou avant de redescendre vers les provinces du Sud et de s'achever traditionnellement sur l'avenue de l'Indépendance à Ouagadougou. Des délégations internationales venues d'Europe et de plusieurs pays frères d'Afrique sont attendues pour défier les coureurs locaux.",
            "<h2>Les chances de l'équipe nationale burkinabè</h2>",
            "Les cyclistes burkinabè, menés par des leaders expérimentés, se préparent intensivement dans les collines de l'Ouest. L'accent est mis sur l'endurance et la stratégie collective en course pour rivaliser avec les équipes professionnelles invitées. Le directeur technique national exprime sa confiance : 'Nos gars connaissent chaque caillou de la route et savent courir ensemble. Le public sera notre force.'",
            "<h2>La logistique et la sécurité sur la route</h2>",
            "La sécurité de la caravane publicitaire et des coureurs fait l'objet d'un plan de coordination renforcé entre les forces de défense et de sécurité et les services de santé. L'état des routes sur certains tronçons suscite des inquiétudes, et des travaux de réfection d'urgence ont été lancés par le ministère des Infrastructures pour garantir un déroulement fluide de l'épreuve.",
            "blockquote: 'Le Tour du Faso fait briller notre pays. C'est l'image d'un Burkina debout, uni, festif, capable d'organiser de grands événements sportifs internationaux dans la fraternité.' - Le président de la Fédération Burkinabè de Cyclisme.",
            "L'événement promet d'offrir des moments sportifs intenses tout en stimulant l'économie des villes étapes à travers l'hébergement et le commerce local. Le rendez-vous est pris pour le coup d'envoi officiel de cette caravane de l'unité."
        ]
    },
    {
        "slug": "sahel-adaptation-agricole-climat",
        "category": "international",
        "title": "Changement Climatique : Les techniques sahéliennes d'adaptation agricole font école à l'international",
        "author": "Ibrahim Barry",
        "date": "03 Juillet 2026",
        "img_id": "21",
        "summary": "Le Zaï, les demi-lunes et la régénération naturelle assistée développés par les paysans du Nord du Burkina suscitent un vif intérêt auprès des experts mondiaux de la lutte contre la désertification.",
        "content_blocks": [
            "Le Sahel burkinabè est l'une des régions les plus vulnérables aux dérèglements climatiques de la planète. Confrontés à des saisons de pluies de plus en plus erratiques et à une désertification progressive des terres arables, les paysans du Nord du Burkina Faso ont développé et perfectionné des techniques d'adaptation agricole remarquables. Ces savoir-faire endogènes, autrefois négligés, sont aujourd'hui étudiés par des scientifiques du monde entier comme des réponses efficaces au réchauffement global.",
            "La technique du Zaï est l'une des plus emblématiques. Elle consiste à creuser des trous de taille moyenne durant la saison sèche, à y déposer de la matière organique (fumier, compost) pour attirer les termites qui vont creuser des galeries souterraines, puis à y semer des céréales (mil, sorgho) dès les premières pluies. Cette méthode permet de retenir l'eau au niveau des racines et de cultiver sur des sols auparavant encroûtés et stériles.",
            "<h2>La régénération naturelle assistée (RNA)</h2>",
            "Une autre technique clé est la RNA, qui consiste pour le paysan à protéger activement les repousses naturelles d'arbres utiles dans son champ lors des travaux de défrichage. Les arbres fournissent de l'ombre, limitent l'érosion des sols par le vent et enrichissent la terre en matière organique grâce à la chute des feuilles. Certaines espèces arborées locales, comme le Faidherbia albida, ont la particularité de perdre leurs feuilles en saison humide, évitant ainsi de faire de l'ombre aux cultures.",
            "<h2>La transmission transfrontalière des savoirs</h2>",
            "Des délégations de paysans venues du Mali, du Niger, mais aussi de pays d'Afrique de l'Est et du Moyen-Orient, visitent régulièrement les parcelles expérimentales du Yatenga pour se former à ces techniques. Des agronomes burkinabè sont également invités dans des conférences internationales pour exposer ces solutions basées sur la nature, peu coûteuses et adaptées aux moyens des petits producteurs.",
            "blockquote: 'La terre n'est pas morte, elle dort simplement. Avec le Zaï et les arbres, nous lui redonnons vie sans produits chimiques. C'est un combat de patience que nous partageons aujourd'hui avec le monde.' - Yacouba Sawadogo, le paysan récipiendaire de prix internationaux.",
            "Le soutien à la diffusion massive de ces techniques paysannes résilientes s'impose comme un pilier de la politique nationale d'autosuffisance alimentaire et de protection de la biodiversité sahélienne."
        ]
    },
    {
        "slug": "numerisation-etat-civil-ouaga",
        "category": "politique",
        "title": "Services Publics : Ouagadougou accélère la numérisation de l'état civil dans ses mairies d'arrondissement",
        "author": "Adama Ouédraogo",
        "date": "02 Juillet 2026",
        "img_id": "22",
        "summary": "Un projet pilote d'archivage numérique des actes de naissance et de mariage promet de réduire considérablement les délais de délivrance et de fiabiliser les registres de la capitale.",
        "content_blocks": [
            "Obtenir un extrait d'acte de naissance ou faire enregistrer un mariage à Ouagadougou a longtemps rimé avec tracasseries, longues files d'attente et registres papier poussiéreux menacés par l'humidité et les termites. Pour remédier à ces dysfonctionnements, la municipalité a engagé un projet d'archivage et de délivrance électronique des actes de l'état civil. Cette initiative marque un tournant qualitatif important dans le rapport quotidien des Ouagalais à leur administration.",
            "Le projet consiste à numériser l'ensemble des registres historiques des arrondissements de la ville et à équiper les agents de guichets de terminaux informatiques connectés à une base de données sécurisée centralisée. Dès qu'un citoyen fait une demande d'acte, l'agent peut retrouver l'enregistrement en quelques secondes à l'aide d'un numéro d'identifiant unique ou d'une recherche multicritère, évitant la fouille manuelle dans les cartons d'archives.",
            "<h2>Une sécurité accrue face à la fraude et aux pertes</h2>",
            "La centralisation des données de l'état civil permet également de lutter efficacement contre la falsification de documents administratifs et la double identité. De plus, les données étant sauvegardées sur des serveurs distants sécurisés, la ville s'assure de ne pas perdre ses archives en cas de sinistre physique majeur (incendie, inondation). Une avancée majeure saluée par les services de justice.",
            "<h2>Former les personnels pour une appropriation réussie</h2>",
            "La transition numérique exige un accompagnement conséquent des agents municipaux, dont beaucoup n'étaient pas familiers des outils informatiques. Des sessions de formation continue au traitement numérique des données et à l'accueil du public ont été mises en œuvre. Les syndicats de la mairie restent attentifs aux conditions de travail et réclament des investissements réguliers dans la maintenance du parc informatique.",
            "blockquote: 'Avant, je devais perdre toute une journée de travail pour obtenir une copie conforme de mon acte. Aujourd'hui, je suis reparti de la mairie en moins de quinze minutes avec un document impeccable.' - Jean-Baptiste Ouedraogo, habitant du secteur 30.",
            "La généralisation de cette numérisation de l'état civil à l'ensemble du territoire national est la prochaine étape cruciale pour asseoir les bases d'un État moderne et proche des besoins de ses citoyens."
        ]
    },
    {
        "slug": "jeunes-incubateurs-startups-bobo",
        "category": "economie",
        "title": "Innovation Numérique : Bobo-Dioulasso voit émerger une scène dynamique de startups technologiques",
        "author": "Mariam Sawadogo",
        "date": "01 Juillet 2026",
        "img_id": "23",
        "summary": "La capitale économique du Burkina Faso n'est plus seulement industrielle et agricole ; de nouveaux espaces de coworking et incubateurs y propulsent des innovations locales.",
        "content_blocks": [
            "Bobo-Dioulasso, réputée pour ses usines textiles, ses huileries et son ambiance culturelle chaleureuse, se découvre un nouveau destin technologique. Porté par une jeunesse entreprenante et l'implantation de structures d'accompagnement spécialisées, l'écosystème numérique local se structure rapidement autour de thématiques d'avenir telles que l'agritech, la fintech et la edtech.",
            "Les incubateurs offrent aux porteurs de projets un cadre de travail moderne incluant des connexions haut débit stables (souvent absentes à domicile), des programmes de formation intensifs en codage et en entrepreneuriat, et des opportunités d'accès à des financements d'amorçage. Les startups développent des applications adaptées aux réalités locales, comme des outils d'alerte météo par SMS pour les agriculteurs de la région.",
            "<h2>La synergie avec l'université et l'industrie locale</h2>",
            "L'un des atouts majeurs de l'écosystème de Bobo-Dioulasso est la collaboration étroite avec les instituts d'enseignement supérieur techniques et les entreprises industrielles de la zone. Les étudiants en fin de cycle peuvent ainsi confronter leurs projets théoriques aux besoins réels des usines ou proposer des solutions d'optimisation de chaînes logistiques, facilitant leur insertion professionnelle.",
            "<h2>Le défi crucial de la levée de fonds</h2>",
            "Bien que l'enthousiasme soit fort, les entrepreneurs de Bobo font face à des difficultés pour passer à l'échelle supérieure. L'accès au crédit bancaire classique restant difficile pour les structures innovantes sans garanties physiques, beaucoup dépendent de concours internationaux ou d'aides publiques modestes. La structuration d'un réseau local d'investisseurs providentiels ('Business Angels') s'avère nécessaire.",
            "blockquote: 'Il y a un vivier d'idées incroyable ici à Bobo. Nous n'avons rien à envier aux capitales de la sous-région. Si on nous donne les moyens et l'accompagnement, nous pouvons concevoir des solutions technologiques majeures pour l'Afrique.' - Salimata Coulibaly, fondatrice d'une startup agritech.",
            "Le dynamisme de la scène technologique bobolaise est un signal fort du renouvellement économique de la ville, qui entend bien s'imposer comme un pôle d'innovation incontournable en Afrique de l'Ouest."
        ]
    },
    {
        "slug": "securite-alimentaire-stocks-cereales",
        "category": "societe",
        "title": "Sécurité Alimentaire : L'État renforce la régulation des prix des céréales pour la période de soudure",
        "author": "Fidèle Kaboré",
        "date": "30 Juin 2026",
        "img_id": "24",
        "summary": "Pour protéger le pouvoir d'achat des ménages les plus exposés, la SONAGESS déploie ses stocks stratégiques de maïs et de mil dans les boutiques témoins du pays.",
        "content_blocks": [
            "La période de soudure, cet intervalle critique entre l'épuisement des réserves de la récolte précédente et les nouvelles récoltes, est un moment de tension pour la sécurité alimentaire au Burkina Faso. Face au risque de spéculation et de hausse irrégulière des prix des denrées de base, les autorités publiques ont réagi en lançant une vaste opération de mise à disposition de céréales à prix social sur l'ensemble du territoire.",
            "La Société Nationale de Gestion des Stocks de Sécurité (SONAGESS) a ouvert plusieurs centaines de 'boutiques témoins' dans les zones urbaines périphériques et les chefs-lieux de communes rurales. Dans ces points de vente agréés, le sac de maïs de 50 kg ou de sorgho est vendu à un tarif subventionné, nettement inférieur aux cours constatés sur les marchés libres. L'accès est régulé pour éviter les achats massifs de spéculateurs professionnels.",
            "<h2>Soutenir le tissu agricole local en amont</h2>",
            "Cette politique d'aide alimentaire repose sur une stratégie d'achat local en amont. La SONAGESS s'approvisionne en priorité auprès des unions de producteurs agricoles burkinabè lors des récoltes, garantissant un prix plancher rémunérateur pour les paysans et stockant les grains dans des silos départementaux sécurisés. Ce circuit court limite les coûts intermédiaires d'importation et renforce l'économie agricole nationale.",
            "<h2>Les défis d'acheminement logistique vers les zones isolées</h2>",
            "L'acheminement sécurisé des convois de céréales vers les régions isolées ou soumises à des restrictions de circulation constitue le principal défi logistique de l'opération. L'appui des forces armées s'avère indispensable pour escorter les camions de fret alimentaires et garantir que les vivres parviennent sans encombre aux populations nécessiteuses de l'Est et du Sahel.",
            "blockquote: 'Ces boutiques à prix social nous sauvent la vie pendant les mois difficiles. Sur le marché, le prix du mil a doublé. Grâce à la SONAGESS, je peux nourrir ma famille dignement en attendant la récolte.' - Harouna Diallo, habitant de Dori.",
            "La gestion efficace des stocks stratégiques de sécurité alimentaire demeure ainsi un outil de stabilité sociale essentiel pour traverser les périodes climatiques difficiles et préserver la cohésion nationale."
        ]
    }
]

# Database of video articles
VIDEO_ARTICLES = [
    {
        "slug": "video-siao-ouaga",
        "category": "videos",
        "title": "Reportage : L'excellence de l'artisanat d'art au SIAO Ouaga",
        "author": "Amina Sanou",
        "date": "14 Juillet 2026",
        "video_url": "../assets/videos/flower.webm",
        "duration": "15s",
        "img_id": "201",
        "summary": "Découvrez en images le travail exceptionnel des tisserands et potiers réunis à Ouagadougou. Ce clip court permet de tester les interactions et la complétion rapide du lecteur vidéo HTML5.",
        "content_blocks": [
            "Le Salon International de l'Artisanat de Ouagadougou (SIAO) bat son plein. Notre équipe est allée à la rencontre des maîtres artisans qui perpétuent et renouvellent les techniques traditionnelles.",
            "Dans ce court reportage de 15 secondes, observez le rythme précis du métier à tisser traditionnel et l'habileté de la potière façonnant l'argile rouge. Une véritable démonstration d'art de vivre burkinabè.",
            "Ce lecteur vidéo natif HTML5 est configuré pour vos tests d'audience. Vous pouvez cliquer sur play, mettre en pause, déplacer le curseur de lecture ou tester le mode plein écran."
        ]
    },
    {
        "slug": "video-fespaco-cinema",
        "category": "videos",
        "title": "Micro-trottoir : Ce que le cinéma représente pour la jeunesse ouagalaise",
        "author": "Amina Sanou",
        "date": "13 Juillet 2026",
        "video_url": "../assets/videos/sample-5s.webm",
        "duration": "15s",
        "img_id": "202",
        "summary": "Quel regard les jeunes Burkinabè portent-ils sur la création cinématographique africaine ? Réponse dans ce micro-trottoir court réalisé au cœur de la capitale.",
        "content_blocks": [
            "Alors que la préparation du prochain FESPACO bat son plein, nous avons tendu le micro aux étudiants de l'Université Joseph Ki-Zerbo.",
            "Pour beaucoup, le cinéma africain est un miroir indispensable de nos sociétés, un outil d'émancipation intellectuelle et un moyen de conter nos propres histoires au monde entier.",
            "Regardez cette vidéo de démonstration de 15 secondes pour valider le suivi des événements du lecteur natif."
        ]
    },
    {
        "slug": "video-agroecologie-sahel",
        "category": "videos",
        "title": "Documentaire : Les pionniers de l'agroécologie dans le Sahel burkinabè",
        "author": "Ibrahim Barry",
        "date": "12 Juillet 2026",
        "video_url": "../assets/videos/sample-10s.webm",
        "duration": "10 min",
        "img_id": "203",
        "summary": "Un documentaire complet sur la lutte contre l'avancée du désert dans les provinces du Nord. Ce format long est idéal pour tester les seuils de lecture à 25%, 50%, 75% et 100%.",
        "content_blocks": [
            "Dans le Nord du Burkina Faso, des coopératives agricoles redonnent vie à des sols stériles grâce aux méthodes de l'agroécologie sahélienne. Ce film retrace le quotidien de ces paysans visionnaires.",
            "À travers des images aériennes saisissantes et des témoignages poignants, mesurez l'impact du Zaï et de la régénération naturelle assistée sur la restauration de la biodiversité locale.",
            "Le film dure environ 10 minutes (utilisant la vidéo test Big Buck Bunny comme placeholder CDN). Ce format vous permettra de tester précisément les timers, les événements de mise en pause prolongée et les statistiques de rétention d'audience."
        ]
    },
    {
        "slug": "video-urbanisme-bobodjoulasso",
        "category": "videos",
        "title": "Reportage : Le renouveau urbain et architectural de Bobo-Dioulasso",
        "author": "Mariam Sawadogo",
        "date": "11 Juillet 2026",
        "video_url": "../assets/videos/sample-15s.webm",
        "duration": "9 min",
        "img_id": "204",
        "summary": "Plongez dans les avenues arborées et les quartiers en pleine transformation de la deuxième ville du pays. Un voyage visuel au croisement de la tradition coloniale et de la modernité.",
        "content_blocks": [
            "Bobo-Dioulasso, capitale économique et culturelle, connaît d'importants chantiers d'aménagement routier et d'embellissement public. Notre équipe s'est promenée dans le centre historique de Dioulassoba.",
            "Découvrez comment la préservation de la grande mosquée en terre de style soudano-sahélien cohabite avec la construction d'infrastructures commerciales modernes et durables.",
            "La vidéo de 9 minutes (utilisant le film d'animation Sintel comme démo technique) permet de tester le suivi du défilement et de la complétion sur un format moyen."
        ]
    },
    {
        "slug": "video-culture-burkina",
        "category": "videos",
        "title": "Portrait : Danse traditionnelle et expression moderne à Bobo-Dioulasso",
        "author": "Amina Sanou",
        "date": "09 Juillet 2026",
        "video_url": "../assets/videos/sample-20s.webm",
        "duration": "30s",
        "img_id": "205",
        "summary": "Portrait d'un jeune chorégraphe qui revisite les danses sacrées bobo pour les scènes contemporaines européennes. Vidéo configurée en lecture automatique (autoplay) et muette.",
        "content_blocks": [
            "Rencontre avec Issa, danseur professionnel formé à l'école des traditions et ouvert sur le monde de la danse contemporaine.",
            "Dans ce clip de 30 secondes, admirez la puissance physique et l'expression spirituelle de ses mouvements filmés en plein air. La vidéo démarre automatiquement en mode muet pour tester le tracking spécifique des comportements d'autoplay silencieux."
        ]
    },
    {
        "slug": "video-synthese-semaine",
        "category": "videos",
        "title": "Le résumé de la semaine : Actualités majeures en 3 clips",
        "author": "Ibrahim Barry",
        "date": "08 Juillet 2026",
        "video_url": "../assets/videos/sample-30s.webm",
        "duration": "45s total",
        "img_id": "206",
        "summary": "Une synthèse hebdomadaire compilant plusieurs sujets d'actualité en format court. Cette page contient plusieurs vidéos distinctes pour tester le tracking multi-lecteurs.",
        "content_blocks": [
            "Retrouvez les temps forts de l'actualité burkinabè de la semaine écoulée dans ce format condensé.",
            "Cette page présente plusieurs lecteurs vidéo autonomes et simultanés. C'est l'environnement idéal pour vérifier la distinction correcte entre les instances de tracking de votre script (séparation par ID, synchronisation des états globaux)."
        ]
    }
]

# Combined all articles to facilitate home listing and related searches
ALL_ARTICLES = []
for art in TEXT_ARTICLES:
    ALL_ARTICLES.append({**art, "is_video": False})
for art in VIDEO_ARTICLES:
    ALL_ARTICLES.append({**art, "is_video": True})

# Sort all articles by date fictive (simulated sequence)
# Keep them sorted for general list
ALL_ARTICLES.sort(key=lambda x: x["date"], reverse=True)

# Generate HTML Helper Functions
def get_nav_html(active_slug):
    nav_items_html = ""
    prefix = "../" if active_slug == "article-page" else ""
    for cat in CATEGORIES:
        active_class = "active" if cat["slug"] == active_slug else ""
        nav_items_html += f'<li class="nav-item {active_class}"><a href="{prefix}{cat["slug"]}.html" id="nav-link-{cat["slug"]}">{cat["label"]}</a></li>\n'
    
    return f"""
    <nav class="main-nav" id="main-nav-menu">
        <ul class="nav-list">
            <li class="nav-item {"active" if active_slug == "accueil" else ""}"><a href="{prefix}index.html" id="nav-link-home">Accueil</a></li>
            {nav_items_html}
            <li class="nav-item {"active" if active_slug == "a-propos" else ""}"><a href="{prefix}a-propos.html" id="nav-link-about">À propos</a></li>
            <li class="nav-item {"active" if active_slug == "contact" else ""}"><a href="{prefix}contact.html" id="nav-link-contact">Contact</a></li>
        </ul>
    </nav>
    """

def get_header_html(active_slug):
    nav_html = get_nav_html(active_slug)
    # Breaking news list
    breaking_news_html = ""
    for art in ALL_ARTICLES[:4]:
        link_prefix = "articles/" if active_slug != "article-page" else ""
        breaking_news_html += f'<li><a href="{link_prefix}{art["slug"]}.html">{art["title"]}</a></li>'

    logo_path = "index.html" if active_slug == "accueil" else "../index.html" if active_slug == "article-page" else "index.html"

    return f"""
    <header class="main-header">
        <div class="container">
            <div class="header-top">
                <a href="{logo_path}" class="logo-link" id="site-logo">
                    <div class="logo-flag">
                        <div class="logo-flag-red"></div>
                        <div class="logo-flag-green"></div>
                        <span class="logo-flag-star">★</span>
                    </div>
                    FASO<span class="horizon">HORIZON</span>
                </a>
                <div class="date-weather">
                    <span id="header-date-text">Mardi 14 Juillet 2026</span>
                    <span class="weather-badge" id="header-weather-badge">☼ Ouagadougou 34°C</span>
                </div>
                <button class="nav-toggle" id="nav-toggle-btn" aria-label="Menu principal">&#9776;</button>
            </div>
            <div class="nav-container">
                {nav_html}
            </div>
        </div>
        <div class="ticker-bar" id="breaking-ticker">
            <span class="ticker-label" id="ticker-lbl">ALERTE INFO</span>
            <div class="ticker-content">
                <ul class="ticker-items" id="ticker-list">
                    {breaking_news_html}
                </ul>
            </div>
        </div>
    </header>
    """

def get_footer_html(active_slug):
    link_prefix = "articles/" if active_slug != "article-page" else ""
    root_prefix = "" if active_slug != "article-page" else "../"
    
    return f"""
    <footer class="main-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-info">
                    <h4>
                        <div class="logo-flag" style="width: 24px; height: 16px; display: inline-flex; vertical-align: middle;">
                            <div class="logo-flag-red"></div>
                            <div class="logo-flag-green"></div>
                            <span class="logo-flag-star" style="font-size:10px;">★</span>
                        </div>
                        FasoHorizon
                    </h4>
                    <p>FasoHorizon est un portail d'information fictif simulant un média en ligne burkinabè. Cette plateforme sert exclusivement de cible d'instrumentation pour tester des trackers JS et des systèmes d'analyses d'audience dans des conditions réelles.</p>
                    <div class="footer-socials">
                        <a href="#" id="footer-social-fb" aria-label="Facebook">FB</a>
                        <a href="#" id="footer-social-tw" aria-label="Twitter">TW</a>
                        <a href="#" id="footer-social-yt" aria-label="YouTube">YT</a>
                    </div>
                </div>
                <div class="footer-links-col">
                    <h5>Rubriques</h5>
                    <ul class="footer-links">
                        <li><a href="{root_prefix}politique.html">Politique</a></li>
                        <li><a href="{root_prefix}economie.html">Économie</a></li>
                        <li><a href="{root_prefix}societe.html">Société</a></li>
                        <li><a href="{root_prefix}sport.html">Sport</a></li>
                        <li><a href="{root_prefix}culture.html">Culture</a></li>
                        <li><a href="{root_prefix}international.html">International</a></li>
                        <li><a href="{root_prefix}videos.html">Vidéos & Multimédia</a></li>
                    </ul>
                </div>
                <div class="footer-links-col">
                    <h5>Newsletter</h5>
                    <div class="newsletter-box">
                        <h4>Faso Actu Lettre</h4>
                        <p>Recevez l'essentiel de l'actualité burkinabè dans votre boîte mail.</p>
                        <form id="newsletter-form" action="#" method="POST">
                            <div class="form-group">
                                <input type="email" id="newsletter-email" class="form-input" placeholder="Votre adresse email" required>
                            </div>
                            <button type="submit" id="newsletter-submit" class="btn-primary">S'abonner</button>
                            <div id="newsletter-feedback" class="form-feedback"></div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 FasoHorizon. Tous droits réservés. Projet de test pour métriques d'audience.</p>
                <div class="footer-bottom-links">
                    <a href="{root_prefix}mentions-legales.html" id="footer-link-legal">Mentions Légales</a>
                    <a href="{root_prefix}a-propos.html" id="footer-link-about">À Propos</a>
                    <a href="{root_prefix}contact.html" id="footer-link-contact">Contact</a>
                </div>
            </div>
        </div>
    </footer>
    """

def get_sidebar_html(active_slug):
    # Sidebar features "Most read" and a weather widget. Let's build most read based on top 5 sorted articles
    most_read_html = ""
    link_prefix = "articles/" if active_slug != "article-page" else ""
    
    # We will pick a few articles to display in the "Most Read" sidebar
    most_read_list = ALL_ARTICLES[2:7]
    for idx, art in enumerate(most_read_list):
        category_label = next(c["label"] for c in CATEGORIES if c["slug"] == art["category"])
        most_read_html += f"""
        <li class="most-read-item">
            <span class="most-read-rank">0{idx+1}</span>
            <div class="most-read-info">
                <span class="most-read-category">{category_label}</span>
                <h5><a href="{link_prefix}{art["slug"]}.html" class="most-read-link" data-rank="{idx+1}">{art["title"]}</a></h5>
            </div>
        </li>
        """
        
    return f"""
    <aside class="sidebar">
        <!-- Warning Panel for Instrumentation -->
        <div class="tracking-alert-banner" id="test-mode-banner">
            <strong>⚙️ CIBLE DE TRACKING ACTIVED</strong>
            <span>Ce site ne contient aucun cookie tracker. Pour vos tests, insérez votre code d'acquisition juste avant la balise <code>&lt;/head&gt;</code> de chaque document HTML. Les formulaires et lecteurs vidéo possèdent des classes et des IDs stables.</span>
        </div>

        <!-- Most Read Widget -->
        <div class="widget" id="widget-most-read">
            <h4 class="widget-title">Les plus lus</h4>
            <ul class="most-read-list">
                {most_read_html}
            </ul>
        </div>
        
        <!-- Weather Widget -->
        <div class="widget" id="widget-weather">
            <h4 class="widget-title">Météo Locale</h4>
            <div class="weather-widget-full">
                <div class="weather-detail">
                    <span class="weather-temp">38°C</span>
                    <span>Beau temps ensoleillé</span>
                    <span style="font-size:0.8rem; color:var(--text-muted);">Vent: 14 km/h • Humidité: 28%</span>
                </div>
                <div style="font-size: 3rem; line-height: 1;">☀️</div>
            </div>
        </div>

        <!-- Local Quotes Widget -->
        <div class="widget" id="widget-quote">
            <h4 class="widget-title">Proverbe Faso</h4>
            <blockquote style="font-style: italic; color: var(--text-muted); border-left: 3px solid var(--secondary-color); padding-left: 15px; margin: 10px 0;">
                "L'eau de la jarre ne remplit pas la calebasse si la main n'y touche pas."
            </blockquote>
        </div>
    </aside>
    """

# ----------------- PAGE GENERATORS -----------------

def generate_page(filename, title, content_html, active_slug, custom_head=""):
    """
    Core HTML rendering function.
    Maintains stable CSS/JS paths and script injection points.
    """
    is_article_page = (active_slug == "article-page")
    css_path = "../assets/css/styles.css" if is_article_page else "assets/css/styles.css"
    js_path = "../assets/js/main.js" if is_article_page else "assets/js/main.js"
    
    header_html = get_header_html(active_slug)
    footer_html = get_footer_html(active_slug)
    
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FasoHorizon</title>
    <link rel="stylesheet" href="{css_path}">
    {custom_head}
    <!-- EXTRA_TRACKING_SCRIPTS_PLACEHOLDER -->
</head>
<body>
    {header_html}

    <main class="container mt-4 mb-4">
        {content_html}
    </main>

    {footer_html}

    <script src="{js_path}"></script>
</body>
</html>"""

    # Determine filepath
    filepath = f"articles/{filename}" if is_article_page else filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

# 1. Homepage Generation (index.html)
def build_homepage():
    # A la Une articles (indices 0 to 3)
    alaune = ALL_ARTICLES[:3]
    featured = alaune[0]
    side1 = alaune[1]
    side2 = alaune[2]
    
    # Recent articles (indices 3 to 13)
    recent = ALL_ARTICLES[3:13]
    
    # Render featured card
    feat_cat_label = next(c["label"] for c in CATEGORIES if c["slug"] == featured["category"])
    feat_badge = next(c["badge"] for c in CATEGORIES if c["slug"] == featured["category"])
    feat_link = f"articles/{featured['slug']}.html"
    featured_html = f"""
    <article class="hero-featured" id="featured-card">
        <div class="card-img-wrapper">
            <img src="https://picsum.photos/id/{featured['img_id']}/800/450" alt="{featured['title']}">
        </div>
        <div class="card-content">
            <div class="card-meta">
                <span class="badge {feat_badge}">{feat_cat_label}</span>
                <span>Par {featured['author']}</span>
                <span>{featured['date']}</span>
            </div>
            <h3><a href="{feat_link}">{featured['title']}</a></h3>
            <p>{featured['summary']}</p>
            <a href="{feat_link}" class="btn-read-more">Lire l'article</a>
        </div>
    </article>
    """
    
    # Render side cards
    side_html = ""
    for art in [side1, side2]:
        side_cat_label = next(c["label"] for c in CATEGORIES if c["slug"] == art["category"])
        side_badge = next(c["badge"] for c in CATEGORIES if c["slug"] == art["category"])
        side_link = f"articles/{art['slug']}.html"
        side_html += f"""
        <article class="side-card" id="side-card-{art['slug']}">
            <div class="card-img-wrapper">
                <img src="https://picsum.photos/id/{art['img_id']}/400/250" alt="{art['title']}">
            </div>
            <div class="card-content">
                <div class="card-meta">
                    <span class="badge {side_badge}">{side_cat_label}</span>
                </div>
                <h4><a href="{side_link}">{art['title']}</a></h4>
            </div>
        </article>
        """
        
    # Render recent articles list
    recent_grid_html = ""
    for art in recent:
        cat_label = next(c["label"] for c in CATEGORIES if c["slug"] == art["category"])
        badge = next(c["badge"] for c in CATEGORIES if c["slug"] == art["category"])
        link = f"articles/{art['slug']}.html"
        # If it's a video article, we might show a play icon or tag
        video_tag = " • 🎥 Vidéo" if art["is_video"] else ""
        
        recent_grid_html += f"""
        <article class="news-card" data-category="{art['category']}" id="recent-card-{art['slug']}">
            <div class="card-img-wrapper">
                <img src="https://picsum.photos/id/{art['img_id']}/400/250" alt="{art['title']}">
            </div>
            <div class="card-content">
                <div class="card-meta">
                    <span class="badge {badge}">{cat_label}</span>
                    <span>{art['date']}{video_tag}</span>
                </div>
                <h4><a href="{link}">{art['title']}</a></h4>
                <p>{art['summary']}</p>
                <a href="{link}" class="btn-read-more">Lire la suite</a>
            </div>
        </article>
        """
        
    sidebar_html = get_sidebar_html("accueil")
    
    homepage_content = f"""
    <div class="hero-section">
        <h2 class="section-title">À LA UNE <span style="font-size:0.8rem; color:var(--accent-color);">Breaking News</span></h2>
        <div class="hero-grid">
            {featured_html}
            <div class="hero-side-grid">
                {side_html}
            </div>
        </div>
    </div>
    
    <div class="main-layout">
        <div class="content-area">
            <h2 class="section-title">Dernières Actualités</h2>
            <div class="recent-grid" id="recent-articles-grid">
                {recent_grid_html}
            </div>
            <div class="pagination-container">
                <button id="load-more-btn" class="btn-load-more">Charger plus d'articles</button>
            </div>
        </div>
        {sidebar_html}
    </div>
    """
    
    generate_page("index.html", "L'actualité burkinabè en continu", homepage_content, "accueil")

# 2. Category Pages (politique.html, economie.html, etc.)
def build_category_pages():
    for cat in CATEGORIES:
        slug = cat["slug"]
        label = cat["label"]
        
        # Gather all articles under this category
        cat_articles = [art for art in ALL_ARTICLES if art["category"] == slug]
        
        # Grid HTML
        grid_html = ""
        if not cat_articles:
            grid_html = "<p>Aucun article disponible dans cette rubrique pour le moment.</p>"
        else:
            for art in cat_articles:
                badge = cat["badge"]
                link = f"articles/{art['slug']}.html"
                grid_html += f"""
                <article class="news-card" id="cat-card-{art['slug']}">
                    <div class="card-img-wrapper">
                        <img src="https://picsum.photos/id/{art['img_id']}/400/250" alt="{art['title']}">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="badge {badge}">{label}</span>
                            <span>{art['date']}</span>
                        </div>
                        <h4><a href="{link}">{art['title']}</a></h4>
                        <p>{art['summary']}</p>
                        <a href="{link}" class="btn-read-more">Lire la suite</a>
                    </div>
                </article>
                """
        
        sidebar_html = get_sidebar_html(slug)
        content_html = f"""
        <div class="main-layout">
            <div class="content-area">
                <h2 class="section-title">Rubrique : {label}</h2>
                <div class="recent-grid">
                    {grid_html}
                </div>
            </div>
            {sidebar_html}
        </div>
        """
        generate_page(f"{slug}.html", f"Actualités {label}", content_html, slug)

# 3. About Page (a-propos.html)
def build_about_page():
    content = """
    <div class="main-layout">
        <div class="content-area" style="background-color: var(--bg-card); padding: 40px; border-radius: var(--radius-md); border:1px solid var(--border-color);">
            <h1 style="font-family: var(--font-title); font-size:2.5rem; margin-bottom: 20px; color: var(--primary-color);">À Propos de FasoHorizon</h1>
            <p style="font-size: 1.1rem; margin-bottom: 20px; font-weight: 500;">FasoHorizon est la plateforme numérique de référence fictive pour l'actualité au Burkina Faso.</p>
            
            <h2 style="margin: 30px 0 15px 0; font-size: 1.6rem; color: var(--primary-color);">Notre Mission</h2>
            <p style="margin-bottom: 20px;">Notre objectif est de fournir une information impartiale, rigoureuse et de proximité sur l'ensemble du territoire burkinabè. De l'économie sahélienne à la diplomatie internationale de l'UEMOA, en passant par les scènes sportives et les innovations éducatives locales, nous couvrons la diversité des actualités avec dévouement.</p>
            
            <h2 style="margin: 30px 0 15px 0; font-size: 1.6rem; color: var(--primary-color);">Rôle Technique de Test</h2>
            <p style="margin-bottom: 20px;">Ce site a été conçu spécifiquement pour servir de <strong>cible d'instrumentation web stable</strong>. Il est destiné aux développeurs et analystes qui souhaitent tester des scripts d'acquisition de trafic, des outils de scraping en Playwright ou Cypress, ou valider le comportement de trackers d'audience complexes. Aucune restriction de sécurité Content Security Policy (CSP) n'est active, garantissant une injection aisée de scripts tiers.</p>
            
            <div style="background-color: var(--primary-light); border-left: 4px solid var(--primary-color); padding: 20px; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; margin: 30px 0;">
                <h3 style="margin-bottom: 10px; color: var(--primary-color);">Note pour l'intégration de trackers</h3>
                <p style="font-size:0.95rem;">Toutes les balises sémantiques importantes (formulaires de newsletter, boutons de partages, sections de commentaires, lecteurs vidéo native HTML5) possèdent des IDs clairs et immuables comme <code>id="newsletter-form"</code> ou <code>id="video-player-slug"</code> pour simplifier les sélections XPath/CSS.</p>
            </div>
        </div>
        """ + get_sidebar_html("a-propos") + "</div>"
        
    generate_page("a-propos.html", "À Propos", content, "a-propos")

# 4. Contact Page (contact.html)
def build_contact_page():
    content = """
    <div class="contact-container">
        <h2>Nous Contacter</h2>
        <p>Vous souhaitez des informations complémentaires ou faire une remarque sur la plateforme de test ? Remplissez ce formulaire. Les événements d'envoi sont interceptables par vos scripts.</p>
        
        <form id="contact-form" class="contact-form" action="#" method="POST">
            <div class="form-group">
                <label for="contact-name">Nom complet</label>
                <input type="text" id="contact-name" name="name" required placeholder="Ex: Seydou Kaboré">
            </div>
            
            <div class="form-group">
                <label for="contact-email">Adresse e-mail</label>
                <input type="email" id="contact-email" name="email" required placeholder="Ex: seydou@example.bf">
            </div>
            
            <div class="form-group">
                <label for="contact-subject">Objet du message</label>
                <input type="text" id="contact-subject" name="subject" required placeholder="Ex: Questions sur l'instrumentation">
            </div>
            
            <div class="form-group">
                <label for="contact-message">Message</label>
                <textarea id="contact-message" name="message" required placeholder="Écrivez votre message ici..."></textarea>
            </div>
            
            <button type="submit" id="contact-submit" class="btn-primary">Envoyer le message</button>
            <div id="contact-feedback" style="display:none; padding:15px; border-radius: var(--radius-sm); margin-top:15px; font-weight:bold;"></div>
        </form>
    </div>
    """
    generate_page("contact.html", "Contactez-nous", content, "contact")

# 5. Legal Notices (mentions-legales.html)
def build_legal_page():
    content = """
    <div class="main-layout">
        <div class="content-area" style="background-color: var(--bg-card); padding: 40px; border-radius: var(--radius-md); border:1px solid var(--border-color);">
            <h1 style="font-family: var(--font-title); font-size:2.5rem; margin-bottom: 20px; color: var(--primary-color);">Mentions Légales</h1>
            <p style="margin-bottom: 20px;">Conformément à la réglementation sur la communication numérique, voici les mentions légales relatives à FasoHorizon.</p>
            
            <h2 style="margin: 25px 0 10px 0; font-size: 1.4rem; color: var(--primary-color);">Éditeur du site</h2>
            <p style="margin-bottom: 15px;">FasoHorizon est un site de simulation d'actualités développé de façon fictive dans un but pédagogique et de démonstration technique.</p>
            
            <h2 style="margin: 25px 0 10px 0; font-size: 1.4rem; color: var(--primary-color);">Hébergement</h2>
            <p style="margin-bottom: 15px;">Le site est hébergé localement sur la machine de test de l'utilisateur ou sur son serveur Nginx privé.</p>
            
            <h2 style="margin: 25px 0 10px 0; font-size: 1.4rem; color: var(--primary-color);">Données Personnelles et Traceurs</h2>
            <p style="margin-bottom: 15px;">Ce site lui-même ne stocke, ne collecte ni ne traite aucune donnée nominative. Les formulaires de contact, de newsletter et de commentaires présents sur le site sont des simulations (mock) qui n'enregistrent aucune donnée dans une base réelle.</p>
            <p style="margin-bottom: 15px;">L'utilisateur final peut y injecter des scripts de tracking tiers pour tester des flux de collecte. Dans ce cas, les règles de RGPD applicables dépendent de la configuration du serveur externe d'acquisition.</p>
        </div>
        """ + get_sidebar_html("mentions-legales") + "</div>"
        
    generate_page("mentions-legales.html", "Mentions Légales", content, "mentions-legales")

# 6. Single Article Pages (both standard and video articles)
def build_individual_article_pages():
    # Pre-select some related articles for suggestions
    for art in ALL_ARTICLES:
        slug = art["slug"]
        category = art["category"]
        is_video = art["is_video"]
        
        # Category info
        cat_label = next(c["label"] for c in CATEGORIES if c["slug"] == category)
        badge = next(c["badge"] for c in CATEGORIES if c["slug"] == category)
        
        # Form related articles: exclude the current one and choose 3 from same category or random
        related_pool = [a for a in ALL_ARTICLES if a["slug"] != slug and (a["category"] == category or random.random() > 0.5)]
        related_selected = random.sample(related_pool, min(3, len(related_pool)))
        
        related_html = ""
        for rel in related_selected:
            rel_cat_label = next(c["label"] for c in CATEGORIES if c["slug"] == rel["category"])
            rel_badge = next(c["badge"] for c in CATEGORIES if c["slug"] == rel["category"])
            rel_video_mark = " 🎥" if rel["is_video"] else ""
            related_html += f"""
            <div class="related-card">
                <img src="https://picsum.photos/id/{rel['img_id']}/300/180" alt="{rel['title']}">
                <div class="related-card-content">
                    <span class="badge {rel_badge}" style="align-self: flex-start; margin-bottom:8px; font-size:0.65rem;">{rel_cat_label}{rel_video_mark}</span>
                    <h5><a href="{rel['slug']}.html" class="related-article-link" data-target-slug="{rel['slug']}">{rel['title']}</a></h5>
                </div>
            </div>
            """
            
        # Comments Generation (Mock 2 comments per article)
        mock_names = ["Aminata Diallo", "Boubacar Sanou", "Salif Sawadogo", "Fatoumata Barro", "Christian Zongo", "Pierre Kaboré"]
        mock_texts = [
            "Analyse très pertinente de la situation. On espère que les réformes sur le terrain suivront.",
            "C'est un sujet d'actualité très important pour notre pays. Merci pour cet article détaillé.",
            "Une excellente initiative qui mérite d'être soutenue par tous.",
            "Très bon reportage, les images illustrent bien la réalité locale."
        ]
        
        c_name1, c_name2 = random.sample(mock_names, 2)
        c_text1, c_text2 = random.sample(mock_texts, 2)
        
        comments_html = f"""
        <div class="comment-item">
            <div class="comment-avatar">{c_name1[0]}{c_name1.split()[-1][0]}</div>
            <div class="comment-content">
                <div class="comment-header">
                    <span class="comment-author">{c_name1}</span>
                    <span class="comment-date">Hier à 18:32</span>
                </div>
                <p class="comment-text">{c_text1}</p>
            </div>
        </div>
        <div class="comment-item">
            <div class="comment-avatar">{c_name2[0]}{c_name2.split()[-1][0]}</div>
            <div class="comment-content">
                <div class="comment-header">
                    <span class="comment-author">{c_name2}</span>
                    <span class="comment-date">Aujourd'hui à 09:15</span>
                </div>
                <p class="comment-text">{c_text2}</p>
            </div>
        </div>
        """
        
        # Build Body Content
        body_html = ""
        
        # Add player if video article
        if is_video:
            # Check if this is the "synthesis of the week" page with multiple videos, or single video
            if slug == "video-synthese-semaine" or "synthese" in slug:
                # Page with multiple videos to test multiple event listeners
                body_html += f"""
                <div class="video-playlist-container">
                    <h3 class="mb-4">Synthèse en 3 vidéos</h3>
                    <div class="video-grid-2col">
                        <div class="playlist-card">
                            <span class="badge badge-videos">Segment 1 : Évasions en images</span>
                            <div class="video-player-wrapper">
                                <video class="faso-video-player" id="video-player-segment-1" controls preload="metadata" data-video-title="Segment 1 : Evasions" data-video-duration="15s">
                                    <source src="../assets/videos/flower.webm" type="video/webm">
                                    Votre navigateur ne supporte pas le lecteur vidéo.
                                </video>
                            </div>
                            <p style="font-size:0.85rem; color:var(--text-muted);">Durée : 15s • Segment test d'interaction 1</p>
                        </div>
                        <div class="playlist-card">
                            <span class="badge badge-videos">Segment 2 : Incendies contrôlés</span>
                            <div class="video-player-wrapper">
                                <video class="faso-video-player" id="video-player-segment-2" controls preload="metadata" data-video-title="Segment 2 : Incendies" data-video-duration="15s">
                                    <source src="../assets/videos/sample-5s.webm" type="video/webm">
                                    Votre navigateur ne supporte pas le lecteur vidéo.
                                </video>
                            </div>
                            <p style="font-size:0.85rem; color:var(--text-muted);">Durée : 15s • Segment test d'interaction 2</p>
                        </div>
                    </div>
                </div>
                """
            else:
                # Single video
                autoplay_attr = "autoplay muted" if "culture" in slug else ""
                body_html += f"""
                <div class="video-player-wrapper">
                    <video class="faso-video-player" id="video-player-{slug}" controls {autoplay_attr} preload="metadata" data-video-title="{art['title']}" data-video-duration="{art['duration']}">
                        <source src="{art['video_url']}" type="video/webm">
                        Votre navigateur ne supporte pas le lecteur vidéo HTML5 natif.
                    </video>
                </div>
                """
        else:
            # Main image for text article
            body_html += f"""
            <div class="article-main-image">
                <img src="https://picsum.photos/id/{art['img_id']}/900/500" alt="{art['title']}">
                <div class="image-caption">Illustration : Zoom sur le reportage {art['title']} - Crédit photo : FasoHorizon</div>
            </div>
            """
            
        # Compile content blocks
        body_content_html = ""
        for block in art["content_blocks"]:
            if block.startswith("<h2>") or block.startswith("blockquote:"):
                if block.startswith("blockquote:"):
                    q_text = block.replace("blockquote:", "").strip()
                    body_content_html += f"<blockquote>{q_text}</blockquote>"
                else:
                    body_content_html += block
            else:
                body_content_html += f"<p>{block}</p>"
                
        body_html += f"""
        <div class="article-body">
            {body_content_html}
        </div>
        """
        
        # Complete template structure for an article page
        article_template = f"""
        <div class="main-layout">
            <article class="content-area" id="article-{slug}" data-category="{category}">
                <div class="article-header">
                    <div class="article-category">
                        <span class="badge {badge}">{cat_label}</span>
                    </div>
                    <h1 class="article-title">{art['title']}</h1>
                    
                    <div class="article-meta-bar">
                        <div class="author-info">
                            <div class="author-avatar">{art['author'][0]}{art['author'].split()[-1][0]}</div>
                            <div>
                                <strong>{art['author']}</strong><br>
                                <span>Publié le {art['date']}</span>
                            </div>
                        </div>
                        <div class="share-buttons">
                            <button class="share-btn share-facebook" id="share-fb-{slug}" title="Partager sur Facebook">FB</button>
                            <button class="share-btn share-twitter" id="share-tw-{slug}" title="Partager sur Twitter">X</button>
                            <button class="share-btn share-whatsapp" id="share-wa-{slug}" title="Partager sur WhatsApp">WA</button>
                        </div>
                    </div>
                </div>
                
                {body_html}
                
                <!-- Related Articles Area -->
                <div class="related-articles">
                    <h3 class="mb-4">Sur le même sujet</h3>
                    <div class="related-grid">
                        {related_html}
                    </div>
                </div>
                
                <!-- Comments Area -->
                <div class="comments-section" id="comments-section-{slug}">
                    <h3 class="comments-count" id="comments-count-{slug}">2 Commentaire(s)</h3>
                    <div class="comments-list" id="comments-list-{slug}">
                        {comments_html}
                    </div>
                    
                    <div class="comment-form-container">
                        <h4>Laisser un commentaire</h4>
                        <form id="comment-form-{slug}" class="comment-form" action="#" method="POST">
                            <div class="form-row">
                                <input type="text" id="comment-author" placeholder="Votre nom" required>
                            </div>
                            <div class="form-group">
                                <textarea id="comment-text" placeholder="Votre message..." required></textarea>
                            </div>
                            <button type="submit" id="comment-submit" class="btn-submit">Publier le commentaire</button>
                        </form>
                    </div>
                </div>
            </article>
            
            {get_sidebar_html("article-page")}
        </div>
        """
        
        # We generate this file inside 'articles/' folder.
        # So we pass "article-page" as active_slug to adjust asset relative paths
        generate_page(f"{slug}.html", art["title"], article_template, "article-page")

# Run build routines
print("Building FasoHorizon Homepage...")
build_homepage()

print("Building Category Pages...")
build_category_pages()

print("Building Informational Pages (About, Contact, Legal)...")
build_about_page()
build_contact_page()
build_legal_page()

print("Building Individual Articles & Video Pages...")
build_individual_article_pages()

print("FasoHorizon built successfully!")
