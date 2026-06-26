---schema.sql — Megabase 
-- La commune est au centre, toutes les typologies s'y rattachent
-- par clef étrangère sur le code INSEE.
-- ============================================================

-- Ordre de suppression : tables dépendantes avant la table mère (commune)
DROP TABLE IF EXISTS mesure_lycee CASCADE;
DROP TABLE IF EXISTS ehpad CASCADE;
DROP TABLE IF EXISTS college CASCADE;
DROP TABLE IF EXISTS entreprise_btp CASCADE;
DROP TABLE IF EXISTS bibliotheque CASCADE;
DROP TABLE IF EXISTS gare CASCADE;
DROP TABLE IF EXISTS pharmacie CASCADE;
DROP TABLE IF EXISTS lycee CASCADE;
DROP TABLE IF EXISTS mairie CASCADE;
DROP TABLE IF EXISTS commune CASCADE;
DROP TABLE IF EXISTS departement CASCADE;
DROP TABLE IF EXISTS region CASCADE;

-- 0a. Région (référentiel geo.api.gouv.fr : code région INSEE 2 chiffres)
--
CREATE TABLE region (
    code_region  VARCHAR(2) PRIMARY KEY,
    nom_region   VARCHAR(100) NOT NULL
);


-- 0b. Département (code sur 2 ou 3 caractères : Corse 2A/2B, DOM 971-976)
--
CREATE TABLE departement (
    code_departement VARCHAR(3) PRIMARY KEY,
    nom_departement  VARCHAR(100) NOT NULL,
    code_region      VARCHAR(2) NOT NULL,
    CONSTRAINT fk_departement_region
        FOREIGN KEY (code_region)
        REFERENCES region (code_region)
);


----1. La commune : point de rattachement central

CREATE TABLE commune (
    code_insee        VARCHAR(5) PRIMARY KEY,
    nom_commune       VARCHAR(100) NOT NULL,
    code_postal       VARCHAR(10),
    code_departement  VARCHAR(3) NOT NULL,
    population        INTEGER,
    latitude          NUMERIC(10,7),
    longitude         NUMERIC(10,7),
    CONSTRAINT fk_commune_departement
        FOREIGN KEY (code_departement)
        REFERENCES departement (code_departement)
);

--Mairie (1 mairie par commune en général)

CREATE TABLE mairie (
    code_insee   VARCHAR(5) PRIMARY KEY,
    adresse      TEXT,
    latitude     NUMERIC(10,7),
    longitude    NUMERIC(10,7),
    CONSTRAINT fk_mairie_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);

-----Lycées

CREATE TABLE lycee (
    id_lycee     SERIAL PRIMARY KEY,
    uai          VARCHAR(20) UNIQUE,
    nom          VARCHAR(255) NOT NULL,
    adresse      TEXT,
    latitude     NUMERIC(10,7),
    longitude    NUMERIC(10,7),
    code_insee   VARCHAR(5) NOT NULL,
    CONSTRAINT fk_lycee_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);

-- Mesure d'activité datée du lycée (nombre d'élèves, voie générale)
-- séparée de l'établissement car c'est une mesure qui varie dans le temps
CREATE TABLE mesure_lycee (
    id_mesure    SERIAL PRIMARY KEY,
    id_lycee     INTEGER NOT NULL,
    annee        INTEGER NOT NULL,
    nb_eleves    INTEGER,
    CONSTRAINT fk_mesure_lycee
        FOREIGN KEY (id_lycee)
        REFERENCES lycee (id_lycee),
    CONSTRAINT uq_mesure_lycee_annee UNIQUE (id_lycee, annee)
);


----Pharmacies (base FINESS)

CREATE TABLE pharmacie (
    id_pharmacie SERIAL PRIMARY KEY,
    finess       VARCHAR(20) UNIQUE,
    nom          VARCHAR(255) NOT NULL,
    adresse      TEXT,
    code_postal  VARCHAR(10),
    latitude     NUMERIC(10,7),
    longitude    NUMERIC(10,7),
    code_insee   VARCHAR(5) NOT NULL,
    CONSTRAINT fk_pharmacie_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);


----Gares voyageurs (open data SNCF)

CREATE TABLE gare (
    id_gare      SERIAL PRIMARY KEY,
    code_uic     VARCHAR(50) UNIQUE,
    nom          VARCHAR(255) NOT NULL,
    latitude     NUMERIC(10,7),
    longitude    NUMERIC(10,7),
    code_insee   VARCHAR(5) NOT NULL,
    voyageurs_par_an BIGINT,
    annee_mesure     INTEGER,
    CONSTRAINT fk_gare_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);


-----Bibliothèques (data.culture.gouv.fr)

CREATE TABLE bibliotheque (
    id_bibliotheque    SERIAL PRIMARY KEY,
    identifiant_source VARCHAR(50) UNIQUE,
    nom                VARCHAR(255) NOT NULL,
    adresse            TEXT,
    latitude           NUMERIC(10,7),
    longitude          NUMERIC(10,7),
    code_insee         VARCHAR(5) NOT NULL,
    nb_inscrits        INTEGER,
    CONSTRAINT fk_bibliotheque_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);


-----Entreprises du BTP (recherche-entreprises.api.gouv.fr, NAF 41/42/43)

CREATE TABLE entreprise_btp (
    id_entreprise SERIAL PRIMARY KEY,
    siren         VARCHAR(9) UNIQUE NOT NULL,
    raison_sociale VARCHAR(255) NOT NULL,
    code_naf      VARCHAR(10),
    adresse       TEXT,
    latitude      NUMERIC(10,7),
    longitude     NUMERIC(10,7),
    code_insee    VARCHAR(5) NOT NULL,
    tranche_effectif VARCHAR(20),
    CONSTRAINT fk_btp_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);


-------Collèges (annuaire de l'éducation)

CREATE TABLE college (
    id_college   SERIAL PRIMARY KEY,
    uai          VARCHAR(20) UNIQUE,
    nom          VARCHAR(255) NOT NULL,
    adresse      TEXT,
    latitude     NUMERIC(10,7),
    longitude    NUMERIC(10,7),
    code_insee   VARCHAR(5) NOT NULL,
    nb_eleves    INTEGER,
    CONSTRAINT fk_college_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);


------EHPAD (base FINESS)

CREATE TABLE ehpad (
    id_ehpad     SERIAL PRIMARY KEY,
    finess       VARCHAR(20) UNIQUE,
    nom          VARCHAR(255) NOT NULL,
    adresse      TEXT,
    latitude     NUMERIC(10,7),
    longitude    NUMERIC(10,7),
    code_insee   VARCHAR(5) NOT NULL,
    capacite_lits INTEGER,
    CONSTRAINT fk_ehpad_commune
        FOREIGN KEY (code_insee)
        REFERENCES commune (code_insee)
);
