
CREATE TABLE IF NOT EXISTS google_trends (
    id          SERIAL PRIMARY KEY,
    nom_media   VARCHAR(100),
    semaine     DATE,
    interet     INTEGER,
    geo         VARCHAR(5)  DEFAULT 'BF',
    collecte_le TIMESTAMP   DEFAULT NOW(),
    UNIQUE(nom_media, semaine)
);


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

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;