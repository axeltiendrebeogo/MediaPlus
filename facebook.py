# -*- coding: utf-8 -*-
"""
facebook.py — Collecte des stats Facebook via API Graph (Token d'application)
"""
import requests, time, psycopg2
from datetime import datetime
from psycopg2.extras import execute_values
from config import DB_CONFIG

FB_ACCESS_TOKEN = '1516949579617877|uu7-lj5dRjkcmIUwueN04_8nviU'

PAGES_FACEBOOK = {
    'RTB Burkina': 'RTB',
    'Burkina 24':  'Burkina24',
    'Omega BF':    'RadioOmegafmOfficiel',
    'Sidwaya':     'ESidwaya',
    'Lefaso.net':  'lefaso.net',
}

BASE_URL  = 'https://graph.facebook.com/v19.0'
ADLIB_URL = 'https://graph.facebook.com/v19.0/ads_archive'

CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS fb_pages (
    id              SERIAL PRIMARY KEY,
    nom_media       VARCHAR(100) UNIQUE,
    page_id         VARCHAR(50),
    nom_page        VARCHAR(200),
    followers       BIGINT,
    likes           BIGINT,
    date_creation   DATE,
    categorie       VARCHAR(100),
    collecte_le     TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS fb_posts (
    id               SERIAL PRIMARY KEY,
    nom_media        VARCHAR(100),
    post_id          VARCHAR(100) UNIQUE,
    message          TEXT,
    date_publication TIMESTAMP,
    nb_likes         INTEGER DEFAULT 0,
    nb_commentaires  INTEGER DEFAULT 0,
    nb_partages      INTEGER DEFAULT 0,
    url_post         TEXT,
    collecte_le      TIMESTAMP DEFAULT NOW()
);
"""

def safe_int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0

def get_page_info(page_name):
    params = {
        'fields':       'id,name,followers_count,fan_count,category,about',
        'access_token': FB_ACCESS_TOKEN,
    }
    try:
        resp = requests.get(f'{BASE_URL}/{page_name}', params=params, timeout=20)
        data = resp.json()
        if 'error' in data:
            code = data['error'].get('code', 0)
            msg  = data['error']['message']
            if code == 190:
                print(f'  ✗ Token invalide ou expire')
            elif code == 10:
                print(f'  ✗ Permission refusee')
            elif 'does not exist' in msg.lower():
                print(f'  ✗ Page "{page_name}" introuvable')
            else:
                print(f'  ✗ Erreur {code} : {msg}')
            return None
        return {
            'page_id':       data.get('id'),
            'nom_page':      data.get('name'),
            'followers':     safe_int(data.get('followers_count')),
            'likes':         safe_int(data.get('fan_count')),
            'date_creation': None,
            'categorie':     data.get('category'),
        }
    except Exception as e:
        print(f'  ✗ Exception : {e}')
        return None

def get_ads(page_id, nom_media):
    params = {
        'access_token':         FB_ACCESS_TOKEN,
        'ad_type':              'ALL',
        'ad_reached_countries': "['BF']",
        'search_page_ids':      page_id,
        'fields':               'id,ad_creation_time,ad_creative_bodies,page_name',
        'limit':                50,
    }
    try:
        resp = requests.get(ADLIB_URL, params=params, timeout=20)
        data = resp.json()
        if 'error' in data:
            print(f'  ⚠ Ad Library : {data["error"]["message"]}')
            return []
        posts = []
        for ad in data.get('data', []):
            bodies  = ad.get('ad_creative_bodies', [])
            message = bodies[0] if bodies else ''
            try:
                dt = datetime.strptime(ad.get('ad_creation_time', '')[:19], '%Y-%m-%dT%H:%M:%S')
            except Exception:
                dt = None
            posts.append({
                'post_id':          ad.get('id', ''),
                'message':          message[:1000],
                'date_publication': dt,
                'nb_likes':         0,
                'nb_commentaires':  0,
                'nb_partages':      0,
                'url_post':         f'https://facebook.com/ads/library/?id={ad.get("id","")}',
            })
        return posts
    except Exception as e:
        print(f'  ✗ Exception Ad Library : {e}')
        return []

def save_page(conn, nom_media, info):
    with conn.cursor() as c:
        c.execute("""
            INSERT INTO fb_pages
                (nom_media, page_id, nom_page, followers, likes, date_creation, categorie)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (nom_media) DO UPDATE SET
                followers   = EXCLUDED.followers,
                likes       = EXCLUDED.likes,
                collecte_le = NOW()
        """, (
            nom_media, info['page_id'], info['nom_page'],
            info['followers'], info['likes'],
            info['date_creation'], info['categorie'],
        ))
        conn.commit()
    print(f'  ✓ {nom_media} : {info["followers"]:,} followers | ID={info["page_id"]}')

def save_posts(conn, nom_media, posts):
    if not posts:
        print(f'  → Aucune pub trouvee pour {nom_media}')
        return
    rows = [(
        nom_media, p['post_id'], p['message'], p['date_publication'],
        p['nb_likes'], p['nb_commentaires'], p['nb_partages'], p['url_post']
    ) for p in posts]
    with conn.cursor() as c:
        execute_values(c, """
            INSERT INTO fb_posts
                (nom_media, post_id, message, date_publication,
                 nb_likes, nb_commentaires, nb_partages, url_post)
            VALUES %s
            ON CONFLICT (post_id) DO UPDATE SET collecte_le = NOW()
        """, rows)
        conn.commit()
    print(f'  ✓ {len(posts)} pubs inserees pour {nom_media}')

def main():
    print('=== FACEBOOK COLLECTOR ===')
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as c:
        c.execute(CREATE_TABLES)
        conn.commit()
    print('[DB] Tables fb_pages et fb_posts pretes\n')

    for nom_media, page_name in PAGES_FACEBOOK.items():
        print(f'--- {nom_media} ({page_name}) ---')
        info = get_page_info(page_name)
        if not info:
            continue
        save_page(conn, nom_media, info)
        if info.get('page_id'):
            ads = get_ads(info['page_id'], nom_media)
            save_posts(conn, nom_media, ads)
        time.sleep(1)

    conn.close()
    print('\n=== TERMINE ===')

if __name__ == '__main__':
    main()