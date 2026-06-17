import time, psycopg2
from psycopg2.extras import execute_values
from googleapiclient.discovery import build
from datetime import datetime, date
from config import DB_CONFIG, YOUTUBE_API_KEY, CHAINES_YOUTUBE

# REMPLACEMENT COMPLET : Social Blade bloque les scrapers depuis 2024.
# On utilise l'API YouTube directement — memes donnees, meme structure de tables.

def create_tables(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS sb_chaines (
            id            SERIAL PRIMARY KEY,
            nom_media     VARCHAR(100) UNIQUE,
            username      VARCHAR(100),
            url_chaine    TEXT,
            abonnes_total BIGINT,
            vues_total    BIGINT,
            date_collecte DATE,
            collecte_le   TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS sb_daily (
            id            SERIAL PRIMARY KEY,
            nom_media     VARCHAR(100),
            date_stat     DATE,
            abonnes       BIGINT,
            delta_abonnes INTEGER,
            vues          BIGINT,
            delta_vues    BIGINT,
            collecte_le   TIMESTAMP DEFAULT NOW(),
            UNIQUE(nom_media, date_stat)
        );
    '''
    with conn.cursor() as c:
        c.execute(sql)
        conn.commit()
    print('[DB] Tables Social Blade pretes')

def safe_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0

def get_chaine_youtube(yt, channel_id):
    """Recupere les stats de la chaine via YouTube API."""
    res = yt.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()
    if not res.get('items'):
        return None
    item    = res['items'][0]
    snippet = item['snippet']
    stats   = item['statistics']
    # username = handle YouTube (@rtburkina) ou channel_id si absent
    username = snippet.get('customUrl', channel_id).lstrip('@')
    return {
        'username':      username,
        'url_chaine':    f'https://youtube.com/@{username}',
        'abonnes_total': safe_int(stats.get('subscriberCount')),
        'vues_total':    safe_int(stats.get('viewCount')),
        'date_collecte': date.today(),
    }

def get_previous_daily(conn, nom_media):
    """Recupere les stats du dernier jour enregistre pour calculer le delta."""
    with conn.cursor() as c:
        c.execute('''
            SELECT abonnes, vues FROM sb_daily
            WHERE nom_media = %s
            ORDER BY date_stat DESC
            LIMIT 1
        ''', (nom_media,))
        return c.fetchone()  # (abonnes_prec, vues_prec) ou None

def save_chaine(conn, nom_media, info):
    sql = '''
        INSERT INTO sb_chaines
        (nom_media, username, url_chaine, abonnes_total, vues_total, date_collecte)
        VALUES (%s,%s,%s,%s,%s,%s)
        ON CONFLICT (nom_media) DO UPDATE SET
            abonnes_total = EXCLUDED.abonnes_total,
            vues_total    = EXCLUDED.vues_total,
            date_collecte = EXCLUDED.date_collecte,
            collecte_le   = NOW()
    '''
    with conn.cursor() as c:
        c.execute(sql, (
            nom_media,
            info['username'],
            info['url_chaine'],
            info['abonnes_total'],
            info['vues_total'],
            info['date_collecte'],
        ))
        conn.commit()
    print(f'[DB] {nom_media} : {info["abonnes_total"]:,} abonnes, {info["vues_total"]:,} vues')

def save_daily(conn, nom_media, info):
    """Insere la ligne du jour avec delta par rapport au jour precedent."""
    prev = get_previous_daily(conn, nom_media)
    if prev:
        delta_abonnes = info['abonnes_total'] - prev[0]
        delta_vues    = info['vues_total']    - prev[1]
    else:
        delta_abonnes = 0
        delta_vues    = 0

    sql = '''
        INSERT INTO sb_daily
        (nom_media, date_stat, abonnes, delta_abonnes, vues, delta_vues)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (nom_media, date_stat) DO UPDATE SET
            abonnes       = EXCLUDED.abonnes,
            delta_abonnes = EXCLUDED.delta_abonnes,
            vues          = EXCLUDED.vues,
            delta_vues    = EXCLUDED.delta_vues,
            collecte_le   = NOW()
    '''
    with conn.cursor() as c:
        c.execute(sql, (
            nom_media,
            date.today(),
            info['abonnes_total'],
            delta_abonnes,
            info['vues_total'],
            delta_vues,
        ))
        conn.commit()

    signe_a = '+' if delta_abonnes >= 0 else ''
    signe_v = '+' if delta_vues    >= 0 else ''
    print(f'[DB] {nom_media} aujourd\'hui : '
          f'abonnes={info["abonnes_total"]:,} ({signe_a}{delta_abonnes:,}) | '
          f'vues={info["vues_total"]:,} ({signe_v}{delta_vues:,})')

if __name__ == '__main__':
    print('=== SOCIAL BLADE COLLECTOR (via YouTube API) ===')
    yt   = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    conn = psycopg2.connect(**DB_CONFIG)
    create_tables(conn)

    for nom_media, channel_id in CHAINES_YOUTUBE.items():
        print(f'--- {nom_media} ---')
        info = get_chaine_youtube(yt, channel_id)
        if not info:
            print(f'[ERREUR] Chaine introuvable : {channel_id}')
            continue
        save_chaine(conn, nom_media, info)
        save_daily(conn, nom_media, info)
        time.sleep(1)

    conn.close()
    print('=== TERMINE ===')