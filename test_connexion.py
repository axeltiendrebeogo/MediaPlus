import psycopg2
from config import DB_CONFIG

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute('SELECT version();')
    version = cur.fetchone()
    print('CONNEXION REUSSIE !')
    print(f'Version PostgreSQL : {version[0]}')
    conn.close()
except Exception as e:
    print(f'ECHEC : {e}')