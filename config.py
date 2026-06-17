# fichier : C:\collecte_mcd\config.py

DB_CONFIG = {
    'host':     '127.0.0.1',   # IP de ton serveur PostgreSQL
    'port':     5432,
    'database': 'mcd_medias',
    'user':     'postgres',
    'password': '1123' ,
    'options':  '-c client_encoding=UTF8'
}

YOUTUBE_API_KEY = 'AIzaSyAQJhGeCJbqxawm88-782mB370p9SLlKm8'
WHOISXML_KEY    = 'at_aycYTSWDjBZseLfg7736dZoy5dLZ4'

MEDIAS_WEB = {
    'Lefaso.net':  'lefaso.net',
    'Burkina 24':  'burkina24.net',
    'RTB Burkina': 'rtb.bf',
    'Omega BF':    'omegabf.net',
    'Sidwaya':     'sidwaya.bf',
}

CHAINES_YOUTUBE = {
    'RTB Burkina': 'UCZl9utbYlPMssMhgrGUqXZA',
    'Burkina 24':  'UCJtaDORHQO20XA-tFwpJysQ',  # ← corrigé
    'Omega BF':    'UCeU9FNoeeoTUvomvx5LXFqA',
    'Sidwaya':     'UCb7uGnNY6iez-Rr6DU8c39A',
    'Lefaso.net':  'UCwkWRScl4-urG_nhpLNLf3w',
}
MEDIAS_TRENDS = ['RTB Burkina', 'Burkina 24', 'Omega BF', 'Sidwaya', 'Lefaso.net']