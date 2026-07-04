CREATE DATABASE MediaDatabase;
USE MediaDatabase;

CREATE TABLE Visitor (
    id_visitor BIGSERIAL PRIMARY KEY,
    date_visite DATE,
    langue VARCHAR(255),
    ip_address VARCHAR(255),
    platform VARCHAR(255)
);

CREATE TABLE media(
    id_media  BIGSERIAL PRIMARY KEY,
    name      VARCHAR(50),
    type      VARCHAR(20),
    url       VARCHAR(500),
    date_ajout DATE
);

CREATE TABLE pageweb(
    id_pageweb  BIGSERIAL PRIMARY KEY,
    id_media    BIGINT NOT NULL REFERENCES media(id_media),
    url         VARCHAR(500) UNIQUE,
    titre       TEXT NULL,
    collecte_le TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE interactions (
    id_event    BIGSERIAL PRIMARY KEY,
    id_visitor  BIGINT NOT NULL REFERENCES visitor(id_visitor),
    id_pageweb  BIGINT NOT NULL REFERENCES pageweb(id_pageweb),
    event_type  VARCHAR(50) NOT NULL,
    valeur      TEXT NULL,
    date_interaction TIMESTAMPTZ
);