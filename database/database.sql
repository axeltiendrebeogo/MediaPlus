CREATE DATABASE MediaDatabase;
USE MediaDatabase;

CREATE TABLE Visitor (
    id_visitor BIGSERIAL PRIMARY KEY,
    date_arrivee TIMESTAMP,
    date_depart TIMESTAMP,
    longitude BIGINT,
    laltitude BIGINT,
    device_type VARCHAR(255),
    os VARCHAR(255),
    ip_adress VARCHAR(255),
    navigator VARCHAR(255)
);

CREATE TABLE Event(
    id_event BIGSERIAL PRIMARY KEY,
    type VARCHAR(255),
    date_event DATE
);