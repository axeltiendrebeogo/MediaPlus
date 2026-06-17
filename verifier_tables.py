# -*- coding: utf-8 -*-
"""
verifier_tables.py — Affiche le contenu de chaque table dans le terminal
"""
import psycopg2
from config import DB_CONFIG

def separateur(titre):
    print(f'\n{"="*70}')
    print(f'  TABLE : {titre}')
    print('='*70)

def afficher(conn, nom_table, colonnes, ordre=None):
    separateur(nom_table)
    try:
        with conn.cursor() as c:
            c.execute(f'SELECT COUNT(*) FROM {nom_table}')
            total = c.fetchone()[0]
            print(f'  Total : {total} lignes')
            if total == 0:
                print('  (table vide)')
                return
            cols  = ', '.join(colonnes)
            order = f'ORDER BY {ordre}' if ordre else ''
            c.execute(f'SELECT {cols} FROM {nom_table} {order} LIMIT 10')
            lignes = c.fetchall()
            # En-tete
            largeurs = [20] * len(colonnes)
            ligne_header = '  ' + ' | '.join(str(c).ljust(l) for c, l in zip(colonnes, largeurs))
            print(f'\n{ligne_header}')
            print('  ' + '-' * (sum(largeurs) + 3 * len(largeurs)))
            for ligne in lignes:
                row = '  ' + ' | '.join(str(v if v is not None else '')[:l].ljust(l)
                                        for v, l in zip(ligne, largeurs))
                print(row)
            if total > 10:
                print(f'\n  ... et {total - 10} autres lignes non affichees')
    except Exception as e:
        print(f'  ERREUR : {e}')

def resume_global(conn):
    tables = [
        'medias', 'wayback_pages', 'whois_data', 'google_trends',
        'yt_chaines', 'yt_videos', 'sb_chaines', 'sb_daily',
        'fb_pages', 'fb_posts'
    ]
    print('\n' + '='*70)
    print('  RESUME GLOBAL — BASE mcd_medias')
    print('='*70)
    for table in tables:
        try:
            with conn.cursor() as c:
                c.execute(f'SELECT COUNT(*) FROM {table}')
                n = c.fetchone()[0]
                statut = '✓' if n > 0 else '✗'
                print(f'  {statut}  {table:<20} {n:>6} lignes')
        except Exception:
            print(f'  ?  {table:<20} table inexistante')

def main():
    conn = psycopg2.connect(**DB_CONFIG)

    # Resume global
    resume_global(conn)

    # Table medias
    afficher(conn, 'medias',
        ['nom_media', 'url_media', 'type_media'],
        ordre='nom_media')

    # Table wayback_pages
    afficher(conn, 'wayback_pages',
        ['nom_media', 'url_page', 'date_publication', 'nom_page'],
        ordre='date_publication DESC')

    # Table whois_data
    afficher(conn, 'whois_data',
        ['nom_media', 'domaine', 'adresse_ip', 'registrar', 'date_expiration'],
        ordre='nom_media')

    # Table google_trends
    afficher(conn, 'google_trends',
        ['nom_media', 'semaine', 'interet', 'geo'],
        ordre='semaine DESC')

    # Table yt_chaines
    afficher(conn, 'yt_chaines',
        ['nom_media', 'abonnes', 'vues_total', 'nb_videos', 'pays'],
        ordre='abonnes DESC')

    # Table yt_videos
    afficher(conn, 'yt_videos',
        ['nom_media', 'nom_page', 'nb_vues', 'nb_likes', 'date_publication'],
        ordre='nb_vues DESC')

    # Table sb_chaines
    afficher(conn, 'sb_chaines',
        ['nom_media', 'abonnes_total', 'vues_total', 'date_collecte'],
        ordre='abonnes_total DESC')

    # Table sb_daily
    afficher(conn, 'sb_daily',
        ['nom_media', 'date_stat', 'abonnes', 'delta_abonnes', 'vues', 'delta_vues'],
        ordre='date_stat DESC, nom_media')

    # Table fb_pages
    afficher(conn, 'fb_pages',
        ['nom_media', 'nom_page', 'followers', 'likes', 'categorie'],
        ordre='followers DESC')

    # Table fb_posts
    afficher(conn, 'fb_posts',
        ['nom_media', 'message', 'date_publication', 'nb_likes', 'nb_partages'],
        ordre='date_publication DESC')

    conn.close()
    print(f'\n{"="*70}')
    print('  VERIFICATION TERMINEE')
    print('='*70 + '\n')

if __name__ == '__main__':
    main()
