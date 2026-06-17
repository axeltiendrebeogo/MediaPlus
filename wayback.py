import requests, time, psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from config import DB_CONFIG, MEDIAS_WEB

CDX_URL = 'http://web.archive.org/cdx/search/cdx'

def create_table(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS wayback_pages (
            id               SERIAL PRIMARY KEY,
            nom_media        VARCHAR(100),
            url_page         TEXT,
            date_publication TIMESTAMP,
            timestamp_raw    VARCHAR(20),
            domaine          VARCHAR(100),
            collecte_le      TIMESTAMP DEFAULT NOW(),
            UNIQUE(url_page, timestamp_raw)
        );
        CREATE INDEX IF NOT EXISTS idx_wb_media ON wayback_pages(nom_media);
        CREATE INDEX IF NOT EXISTS idx_wb_date  ON wayback_pages(date_publication);
    '''
    with conn.cursor() as c:
        c.execute(sql)
        conn.commit()
    print('[DB] Table wayback_pages prete')

def appeler_cdx(domaine, limit=200):
    params = {
        'url':      f'{domaine}/*',
        'output':   'json',
        'fl':       'timestamp,original',
        'limit':    limit,
        'filter':   'statuscode:200',
        'collapse': 'urlkey',
        'from':     '20230101',
    }
    print(f'[CDX] Requete pour {domaine} ...')
    try:
        resp = requests.get(CDX_URL, params=params, timeout=90)
        if resp.status_code != 200:
            print(f'[CDX] Erreur HTTP {resp.status_code}')
            return []
        # FIX : verifier que la reponse n'est pas vide avant de parser le JSON
        # Sidwaya et d'autres domaines peu archives renvoient une reponse vide
        if not resp.text.strip():
            print(f'[CDX] Reponse vide — domaine non archive ou peu presente sur Wayback')
            return []
        data = resp.json()
        if not data:
            print(f'[CDX] Aucune donnee retournee')
            return []
        # Ignore la premiere ligne qui est toujours l'en-tete ["timestamp","original"]
        lignes = data[1:] if data[0] == ['timestamp', 'original'] else data
        print(f'[CDX] {len(lignes)} URLs recues')
        return lignes
    except ValueError:
        # FIX : attrape l'erreur JSON quand la reponse n'est pas du JSON valide
        print(f'[CDX] Reponse invalide (pas du JSON) — domaine probablement non archive')
        return []
    except Exception as e:
        print(f'[ERREUR CDX] {e}')
        return []

def to_datetime(ts):
    try:
        return datetime.strptime(ts[:14], '%Y%m%d%H%M%S')
    except:
        return None

def save_to_db(conn, nom_media, domaine, lignes):
    rows = []
    for ligne in lignes:
        if not ligne or len(ligne) < 2:
            continue
        ts  = str(ligne[0]).strip()
        url = str(ligne[1]).strip()
        if not ts.isdigit() or len(ts) != 14:
            continue
        dt = to_datetime(ts)
        if dt and url:
            rows.append((nom_media, url, dt, ts, domaine))

    if not rows:
        print('[DB] Aucune ligne valide')
        return

    sql = '''
        INSERT INTO wayback_pages
        (nom_media, url_page, date_publication, timestamp_raw, domaine)
        VALUES %s
        ON CONFLICT (url_page, timestamp_raw) DO NOTHING
    '''
    with conn.cursor() as c:
        execute_values(c, sql, rows, page_size=200)
        conn.commit()
    print(f'[DB] {len(rows)} pages inserees pour {nom_media}')

if __name__ == '__main__':
    print('=== WAYBACK MACHINE COLLECTOR ===')
    conn = psycopg2.connect(**DB_CONFIG)
    create_table(conn)
    for nom, domaine in MEDIAS_WEB.items():
        print(f'--- {nom} ---')
        lignes = appeler_cdx(domaine, limit=200)
        if lignes:
            save_to_db(conn, nom, domaine, lignes)
        time.sleep(8)
    conn.close()
    print('=== TERMINE ===')