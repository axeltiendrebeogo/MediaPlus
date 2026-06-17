from googleapiclient.discovery import build

YOUTUBE_API_KEY = 'AIzaSyAQJhGeCJbqxawm88-782mB370p9SLlKm8'
yt = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# FIX : termes de recherche optimises pour Google (pas forcement le nom en BD)
chaines = {
    'RTB Burkina':  'RTB Burkina',
    'Burkina 24':   'Burkina24 TV',
    'Omega BF':     'Omega BF Burkina',
    'Sidwaya':      'Sidwaya Burkina',
    'Lefaso.net':   'Lefaso',
}

def get_stats(channel_id):
    """Recupere abonnes, vues et pays pour un channel_id."""
    try:
        res = yt.channels().list(
            part='statistics,snippet',
            id=channel_id
        ).execute()
        items = res.get('items', [])
        if not items:
            return None
        st = items[0].get('statistics', {})
        sn = items[0].get('snippet', {})
        return {
            'abonnes': int(st.get('subscriberCount', 0)),
            'vues':    int(st.get('viewCount', 0)),
            'pays':    sn.get('country', '??'),
        }
    except Exception:
        return None

print("=" * 55)
print("RECHERCHE DES IDs DE CHAINES YOUTUBE")
print("=" * 55)

ids_recommandes = {}

for nom_media, terme in chaines.items():
    res = yt.search().list(
        part='snippet',
        q=terme,
        type='channel',
        maxResults=3
    ).execute()

    print(f'\n>>> {nom_media}  (recherche : "{terme}")')
    print('-' * 55)

    items = res.get('items', [])
    if not items:
        print('  Aucun resultat trouve')
        continue

    meilleur_id    = None
    meilleur_score = -1

    for i, item in enumerate(items, 1):
        titre      = item['snippet']['title']
        channel_id = item['snippet']['channelId']
        desc       = item['snippet'].get('description', '')[:60]

        # FIX : on recupere les stats pour aider a choisir
        stats = get_stats(channel_id)
        if stats:
            abonnes_str = f"{stats['abonnes']:,}"
            pays        = stats['pays']
            score       = stats['abonnes'] + (100000 if pays == 'BF' else 0)
        else:
            abonnes_str = '?'
            pays        = '??'
            score       = 0

        # Le meilleur = plus d'abonnes, avec bonus si pays = BF
        if score > meilleur_score:
            meilleur_score = score
            meilleur_id    = channel_id

        print(f'  Resultat {i}:')
        print(f'    Titre    : {titre}')
        print(f'    ID       : {channel_id}')
        print(f'    Abonnes  : {abonnes_str}')
        print(f'    Pays     : {pays}')
        print(f'    Desc     : {desc}...')
        print(f'    URL      : https://youtube.com/channel/{channel_id}')

    if meilleur_id:
        ids_recommandes[nom_media] = meilleur_id
        print(f'\n  ✓ Recommande : {meilleur_id}')

# Affiche le bloc config.py pret a copier-coller
print("\n" + "=" * 55)
print("COPIE CE BLOC DANS config.py  (remplace CHAINES_YOUTUBE)")
print("=" * 55)
print()
print("CHAINES_YOUTUBE = {")
for nom, cid in ids_recommandes.items():
    print(f"    '{nom}': '{cid}',")
print("}")
print()
print("=" * 55)
print("Verifie les IDs avant de coller (regarde le nombre d'abonnes)")
print("=" * 55)