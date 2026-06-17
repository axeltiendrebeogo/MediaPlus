# -*- coding: utf-8 -*-
"""
wayback_titres.py — Recupere le titre HTML des pages archivees sur Wayback
Enrichit la table wayback_pages avec le champ nom_page (titre de l'article)
"""
import requests, time, psycopg2
from bs4 import BeautifulSoup
from config import DB_CONFIG

def add_column(conn):
    """Ajoute la colonne nom_page si elle n'existe pas encore."""
    with conn.cursor() as c:
        c.execute("""
            ALTER TABLE wayback_pages
            ADD COLUMN IF NOT EXISTS nom_page TEXT
        """)
        conn.commit()
    print('[DB] Colonne nom_page prete')

def get_urls_sans_titre(conn, limite=500):
    """Recupere les URLs qui n'ont pas encore de titre."""
    with conn.cursor() as c:
        # FIX : ne pas utiliser %s dans LIMIT — psycopg2 ne le supporte pas correctement
        c.execute(f"""
            SELECT id, timestamp_raw, url_page, nom_media
            FROM wayback_pages
            WHERE nom_page IS NULL
            AND url_page LIKE '%http%'
            ORDER BY date_publication DESC
            LIMIT {int(limite)}
        """)
        return c.fetchall()

def get_titre_wayback(timestamp, url):
    """
    Recupere le titre HTML de la page via l'URL Wayback archivee.
    Format : https://web.archive.org/web/TIMESTAMP/URL
    """
    wayback_url = f'https://web.archive.org/web/{timestamp}/{url}'
    try:
        resp = requests.get(wayback_url, timeout=20, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'lxml')
        # 1. Balise <title>
        if soup.title and soup.title.string:
            titre = soup.title.string.strip()
            for suffixe in [' | Lefaso.net', ' - Lefaso.net', ' | RTB', ' - RTB',
                            ' | Burkina 24', ' | Sidwaya', ' | Omega BF']:
                titre = titre.replace(suffixe, '')
            return titre[:500] if titre else None
        # 2. Balise h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)[:500]
        return None
    except Exception:
        return None

def save_titre(conn, id_page, titre):
    with conn.cursor() as c:
        c.execute("UPDATE wayback_pages SET nom_page = %s WHERE id = %s", (titre, id_page))
        conn.commit()

def main():
    print('=== WAYBACK TITRES — Enrichissement nom_page ===')
    conn = psycopg2.connect(**DB_CONFIG)
    add_column(conn)

    lignes = get_urls_sans_titre(conn, limite=500)
    print(f'[DB] {len(lignes)} pages sans titre a traiter')

    if not lignes:
        print('[DB] Toutes les pages ont deja un titre')
        conn.close()
        return

    ok, echec = 0, 0
    for i, (id_page, timestamp, url, nom_media) in enumerate(lignes, 1):
        titre = get_titre_wayback(timestamp, url)
        if titre:
            save_titre(conn, id_page, titre)
            print(f'  [{i}/{len(lignes)}] {nom_media} — {titre[:70]}')
            ok += 1
        else:
            echec += 1
            if i % 20 == 0:
                print(f'  [{i}/{len(lignes)}] ... {ok} titres, {echec} echecs')
        time.sleep(2)

    conn.close()
    print(f'\n=== TERMINE — {ok} titres recuperes, {echec} echecs ===')

if __name__ == '__main__':
    main()