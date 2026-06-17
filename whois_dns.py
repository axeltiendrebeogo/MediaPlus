import whois, requests, socket, time, psycopg2
from datetime import datetime
from config import DB_CONFIG, MEDIAS_WEB, WHOISXML_KEY

def create_table(conn):
    sql = '''
        CREATE TABLE IF NOT EXISTS whois_data (
            id               SERIAL PRIMARY KEY,
            nom_media        VARCHAR(100) UNIQUE,
            domaine          VARCHAR(100),
            registrant_nom   VARCHAR(200),
            registrant_email VARCHAR(200),
            registrant_pays  VARCHAR(100),
            date_creation    DATE,
            date_expiration  DATE,
            registrar        VARCHAR(200),
            nameservers      TEXT,
            adresse_ip       VARCHAR(50),
            source           VARCHAR(20),
            collecte_le      TIMESTAMP DEFAULT NOW()
        );
    '''
    with conn.cursor() as c:
        c.execute(sql)
        conn.commit()
    print('[DB] Table whois_data prete')

def whois_local(domaine):
    try:
        w = whois.whois(domaine)
        def clean(v):
            if isinstance(v, list): v = v[0]
            return str(v).strip() if v else None
        def clean_date(d):
            if isinstance(d, list): d = d[0]
            return d.date() if hasattr(d, 'date') else None
        ns = None
        if w.name_servers:
            ns = ','.join(w.name_servers)[:500]
        return {
            'registrant_nom':   clean(w.name),
            'registrant_email': clean(getattr(w, 'emails', None)),
            'registrant_pays':  clean(w.country),
            'date_creation':    clean_date(w.creation_date),
            'date_expiration':  clean_date(w.expiration_date),
            'registrar':        clean(w.registrar),
            'nameservers':      ns,
            'source': 'python-whois',
        }
    except Exception as e:
        print(f'[WHOIS-LOCAL] {domaine}: {e}')
        return {}

def whois_xml(domaine):
    if not WHOISXML_KEY or WHOISXML_KEY == 'at_aycYTSWDjBZseLfg7736dZoy5dLZ4':
        return {}
    url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'
    params = {'apiKey': WHOISXML_KEY, 'domainName': domaine,
              'outputFormat': 'JSON', 'da': '2'}
    try:
        resp = requests.get(url, params=params, timeout=15)
        wr = resp.json().get('WhoisRecord', {})
        ri = wr.get('registrant', {})
        def gdate(k):
            v = wr.get(k, '')
            try: return datetime.fromisoformat(v[:10]).date()
            except: return None
        ns = wr.get('nameServers', {}).get('hostNames', [])
        ns_str = ','.join(ns)[:500] if ns else None
        return {
            'registrant_nom':   ri.get('name') or ri.get('organization'),
            'registrant_email': ri.get('email'),
            'registrant_pays':  ri.get('country'),
            'date_creation':    gdate('createdDate'),
            'date_expiration':  gdate('expiresDate'),
            'registrar':        wr.get('registrarName'),
            'nameservers':      ns_str,
            'source': 'xmlapi',
        }
    except Exception as e:
        print(f'[WHOIS-XML] {domaine}: {e}')
        return {}

def whois_viewdns(domaine):
    """
    FIX : 3eme recours via viewdns.info (gratuit, sans cle API)
    Utile quand python-whois et whoisxmlapi ne retournent pas l'email
    """
    url = f'https://api.viewdns.info/whois/?domain={domaine}&output=json&apikey=freemium'
    try:
        resp = requests.get(url, timeout=15)
        data = resp.json()
        result = data.get('response', {}).get('registrant', {})
        if not result:
            return {}
        def gdate(v):
            for fmt in ('%Y-%m-%d', '%d-%b-%Y', '%Y/%m/%d'):
                try:
                    return datetime.strptime(v[:10], fmt).date()
                except Exception:
                    continue
            return None
        return {
            'registrant_nom':   result.get('name'),
            'registrant_email': result.get('email'),
            'registrant_pays':  result.get('country'),
            'date_creation':    gdate(data.get('response', {}).get('created', '')),
            'date_expiration':  gdate(data.get('response', {}).get('expires', '')),
            'registrar':        data.get('response', {}).get('registrar', {}).get('name'),
            'nameservers':      None,
            'source': 'viewdns',
        }
    except Exception as e:
        print(f'[WHOIS-VIEWDNS] {domaine}: {e}')
        return {}

def get_ip(domaine):
    try:
        return socket.gethostbyname(domaine)
    except:
        return None

def collecter(nom, domaine):
    print(f'[WHOIS] {nom} ({domaine})')
    data = whois_local(domaine)

    # 2eme recours : whoisxmlapi si email manquant
    if not data.get('registrant_email'):
        xml = whois_xml(domaine)
        for k, v in xml.items():
            if not data.get(k):
                data[k] = v

    # FIX : 3eme recours : viewdns.info si email toujours manquant
    if not data.get('registrant_email'):
        print(f'  → Tentative viewdns.info...')
        vdns = whois_viewdns(domaine)
        for k, v in vdns.items():
            if not data.get(k):
                data[k] = v

    data['nom_media']  = nom
    data['domaine']    = domaine
    data['adresse_ip'] = get_ip(domaine)
    print(f'  IP: {data["adresse_ip"]} | Email: {data.get("registrant_email","non disponible")} | Source: {data.get("source","?")}')
    return data

def save_to_db(conn, d):
    sql = '''
        INSERT INTO whois_data
        (nom_media, domaine, registrant_nom, registrant_email,
         registrant_pays, date_creation, date_expiration,
         registrar, nameservers, adresse_ip, source)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (nom_media) DO UPDATE SET
            registrant_nom   = EXCLUDED.registrant_nom,
            registrant_email = EXCLUDED.registrant_email,
            registrant_pays  = EXCLUDED.registrant_pays,
            date_creation    = EXCLUDED.date_creation,
            date_expiration  = EXCLUDED.date_expiration,
            registrar        = EXCLUDED.registrar,
            nameservers      = EXCLUDED.nameservers,
            adresse_ip       = EXCLUDED.adresse_ip,
            source           = EXCLUDED.source,
            collecte_le      = NOW()
    '''
    with conn.cursor() as c:
        c.execute(sql, (
            d.get('nom_media'), d.get('domaine'),
            d.get('registrant_nom'), d.get('registrant_email'),
            d.get('registrant_pays'), d.get('date_creation'),
            d.get('date_expiration'), d.get('registrar'),
            d.get('nameservers'), d.get('adresse_ip'), d.get('source'),
        ))
        conn.commit()
    print(f'[DB] {d["nom_media"]} sauvegarde')

if __name__ == '__main__':
    print('=== WHOIS DNS COLLECTOR ===')
    conn = psycopg2.connect(**DB_CONFIG)
    create_table(conn)
    for nom, domaine in MEDIAS_WEB.items():
        data = collecter(nom, domaine)
        save_to_db(conn, data)
        time.sleep(6)
    conn.close()
    print('=== TERMINE ===')
