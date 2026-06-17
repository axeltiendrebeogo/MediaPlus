import time, isodate, psycopg2
from psycopg2.extras import execute_values
from googleapiclient.discovery import build
from datetime import datetime
from config import DB_CONFIG, YOUTUBE_API_KEY, CHAINES_YOUTUBE

def create_tables(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS yt_chaines (
            id             SERIAL PRIMARY KEY,
            nom_media      VARCHAR(100) UNIQUE,
            channel_id     VARCHAR(50),
            url_media      TEXT,
            abonnes        BIGINT,
            vues_total     BIGINT,
            nb_videos      INTEGER,
            pays           VARCHAR(5),
            date_creation  DATE,
            collecte_le    TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS yt_videos (
            id               SERIAL PRIMARY KEY,
            nom_media        VARCHAR(100),
            video_id         VARCHAR(20) UNIQUE,
            nom_page         TEXT,
            url_page         TEXT,
            date_publication TIMESTAMP,
            auteur_page      VARCHAR(200),
            nb_vues          BIGINT,
            nb_likes         INTEGER,
            nb_commentaires  INTEGER,
            duree_ecoute     INTEGER,
            collecte_le      TIMESTAMP DEFAULT NOW()
        );
    '''
    with conn.cursor() as c:
        c.execute(sql)
        conn.commit()
    print('[DB] Tables YouTube pretes')

# FIX : convertit en int de façon sécurisée, renvoie 0 si vide ou absent
def safe_int(val, default=0):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default

def get_chaine(yt, channel_id):
    res = yt.channels().list(part='snippet,statistics', id=channel_id).execute()
    if not res.get('items'):
        return None
    item = res['items'][0]
    s, st = item['snippet'], item['statistics']
    try:
        dc = datetime.fromisoformat(s['publishedAt'][:10]).date()
    except:
        dc = None
    return {
        'channel_id':    channel_id,
        'url_media':     f'https://youtube.com/channel/{channel_id}',
        'abonnes':       safe_int(st.get('subscriberCount')),   # FIX : était int(..., 0) qui plante si valeur vide
        'vues_total':    safe_int(st.get('viewCount')),
        'nb_videos':     safe_int(st.get('videoCount')),
        'pays':          s.get('country', 'BF'),
        'date_creation': dc,
    }

def get_videos(yt, channel_id, max_res=100):
    videos, page = [], None
    while len(videos) < max_res:
        params = dict(part='snippet', channelId=channel_id,
                      order='date', type='video',
                      maxResults=min(50, max_res - len(videos)))
        if page:
            params['pageToken'] = page
        res = yt.search().list(**params).execute()
        videos.extend(res.get('items', []))
        page = res.get('nextPageToken')
        if not page:
            break
        time.sleep(1)
    return videos

def get_stats(yt, video_ids):
    stats = {}
    for i in range(0, len(video_ids), 50):
        lot = video_ids[i:i+50]
        res = yt.videos().list(
            part='statistics,contentDetails',
            id=','.join(lot)).execute()
        for item in res.get('items', []):
            vid = item['id']
            st  = item.get('statistics', {})
            dur = item.get('contentDetails', {}).get('duration', 'PT0S')
            try:
                sec = int(isodate.parse_duration(dur).total_seconds())
            except:
                sec = 0
            stats[vid] = {
                'vues':  safe_int(st.get('viewCount')),
                'likes': safe_int(st.get('likeCount')),    # FIX : absent si likes desactives
                'comms': safe_int(st.get('commentCount')), # FIX : absent si commentaires desactives
                'duree': sec,
            }
        time.sleep(0.5)
    return stats

def save_chaine(conn, nom, info):
    sql = '''
        INSERT INTO yt_chaines
        (nom_media, channel_id, url_media, abonnes, vues_total, nb_videos, pays, date_creation)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (nom_media) DO UPDATE SET
            abonnes=EXCLUDED.abonnes, vues_total=EXCLUDED.vues_total,
            nb_videos=EXCLUDED.nb_videos, collecte_le=NOW()
    '''
    with conn.cursor() as c:
        c.execute(sql, (nom, info['channel_id'], info['url_media'],
                        info['abonnes'], info['vues_total'], info['nb_videos'],
                        info['pays'], info['date_creation']))
        conn.commit()
    print(f'[DB] {nom} : {info["abonnes"]:,} abonnes')

def save_videos(conn, nom, videos, stats):
    rows = []
    for v in videos:
        vid_id = v['id'].get('videoId', '')
        if not vid_id:
            continue
        sn = v['snippet']
        st = stats.get(vid_id, {})
        try:
            dp = datetime.fromisoformat(sn['publishedAt'][:19])
        except:
            dp = None
        rows.append((
            nom, vid_id,
            sn.get('title', '')[:500],
            f'https://youtube.com/watch?v={vid_id}',
            dp,
            sn.get('channelTitle', ''),
            st.get('vues', 0), st.get('likes', 0),
            st.get('comms', 0), st.get('duree', 0),
        ))
    sql = '''
        INSERT INTO yt_videos
        (nom_media, video_id, nom_page, url_page, date_publication,
         auteur_page, nb_vues, nb_likes, nb_commentaires, duree_ecoute)
        VALUES %s
        ON CONFLICT (video_id) DO UPDATE SET
            nb_vues=EXCLUDED.nb_vues, nb_likes=EXCLUDED.nb_likes,
            nb_commentaires=EXCLUDED.nb_commentaires, collecte_le=NOW()
    '''
    with conn.cursor() as c:
        execute_values(c, sql, rows)
        conn.commit()
    print(f'[DB] {len(rows)} videos inserees pour {nom}')

if __name__ == '__main__':
    print('=== YOUTUBE API COLLECTOR ===')
    yt   = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    conn = psycopg2.connect(**DB_CONFIG)
    create_tables(conn)
    for nom, cid in CHAINES_YOUTUBE.items():
        print(f'--- {nom} ---')
        info = get_chaine(yt, cid)
        if not info:
            print(f'Chaine introuvable : {cid}')
            continue
        save_chaine(conn, nom, info)
        vids    = get_videos(yt, cid, max_res=100)
        vid_ids = [v['id']['videoId'] for v in vids if v.get('id', {}).get('videoId')]
        stats   = get_stats(yt, vid_ids)
        save_videos(conn, nom, vids, stats)
        time.sleep(2)
    conn.close()
    print('=== TERMINE ===')