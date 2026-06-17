import sys, time
import psycopg2
from psycopg2.extras import execute_values
from pytrends.request import TrendReq
from config import DB_CONFIG, MEDIAS_TRENDS

# FIX : correspondance nom_media → terme exact tape sur Google
# Permet d'eviter les noms mal reconnus (ex: "Burkina 24" vs "Burkina24")
TERMES_RECHERCHE = {
    'RTB Burkina': 'RTB Burkina',
    'Burkina 24':  'Burkina 24',
    'Omega BF':    'Omega BF',
    'Sidwaya':     'Sidwaya',
    'Lefaso.net':  'Lefaso',
}

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print('[DB] Connexion reussie')
        return conn
    except Exception as e:
        print(f'[ERREUR DB] {e}')
        sys.exit(1)

def create_table(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS google_trends (
            id          SERIAL PRIMARY KEY,
            nom_media   VARCHAR(100),
            semaine     DATE,
            interet     INTEGER,
            geo         VARCHAR(5)  DEFAULT 'BF',
            collecte_le TIMESTAMP   DEFAULT NOW(),
            UNIQUE(nom_media, semaine)
        );
    '''
    with conn.cursor() as c:
        c.execute(sql)
        conn.commit()
    print('[DB] Table google_trends prete')

def collecter():
    pytrends = TrendReq(hl='fr-BF', tz=0, timeout=(10,25), retries=3, backoff_factor=2)
    resultats = []

    # FIX : on travaille avec les termes de recherche, pas les noms internes
    # On construit un mapping terme → nom_media pour retrouver le bon nom en BD
    termes_a_nom = {terme: nom for nom, terme in TERMES_RECHERCHE.items()
                    if nom in MEDIAS_TRENDS}
    termes = list(termes_a_nom.keys())

    groupes = [termes[i:i+5] for i in range(0, len(termes), 5)]
    for groupe in groupes:
        print(f'[TRENDS] Requete : {groupe}')
        pytrends.build_payload(
            kw_list=groupe,
            cat=0,
            timeframe='today 12-m',
            geo='BF',
            gprop=''
        )
        df = pytrends.interest_over_time()
        if df.empty:
            print('[TRENDS] Aucune donnee')
            continue
        df = df.drop(columns=['isPartial'], errors='ignore')

        for terme in groupe:
            if terme not in df.columns:
                print(f'[TRENDS] Terme absent des resultats : {terme}')
                continue
            # FIX : on enregistre en BD avec le nom_media, pas le terme de recherche
            nom_media = termes_a_nom[terme]
            for date_idx, row in df.iterrows():
                resultats.append({
                    'nom_media': nom_media,
                    'semaine':   date_idx.date(),
                    'interet':   int(row[terme])
                })
        time.sleep(3)

    return resultats

def save_to_db(conn, data):
    if not data:
        print('[DB] Aucune donnee')
        return
    rows = [(d['nom_media'], d['semaine'], d['interet']) for d in data]
    sql = '''
        INSERT INTO google_trends (nom_media, semaine, interet)
        VALUES %s
        ON CONFLICT (nom_media, semaine) DO UPDATE
            SET interet = EXCLUDED.interet, collecte_le = NOW()
    '''
    with conn.cursor() as c:
        execute_values(c, sql, rows)
        conn.commit()
    print(f'[DB] {len(rows)} lignes inserees dans google_trends')

if __name__ == '__main__':
    print('=== GOOGLE TRENDS COLLECTOR ===')
    conn = connect_db()
    create_table(conn)
    data = collecter()
    save_to_db(conn, data)
    conn.close()
    print(f'Termine. {len(data)} points collectes.')