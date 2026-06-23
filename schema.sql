
CREATE TABLE communes (
    code_insee VARCHAR(5) PRIMARY KEY,
    nom_commune VARCHAR(100) NOT NULL,
    code_postal VARCHAR(10),
    departement VARCHAR(100),
    region VARCHAR(100),
    population INTEGER,
    latitude NUMERIC(10,7),
    longitude NUMERIC(10,7)
 CONSTRAINT fk_commune_departement
        FOREIGN KEY(code_insee)
        REFERENCES commune(code_insee)
);


CREATE TABLE IF NOT EXISTS ehpad (
    finess_id VARCHAR(10) PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    adresse TEXT,
    capacite_lits INTEGER,
    code_insee VARCHAR(5) NOT NULL,
    -- La contrainte qui garantit le lien avec la table commune
    CONSTRAINT fk_commune 
        FOREIGN KEY (code_insee) 
        REFERENCES commune(code_insee) 
        ON DELETE CASCADE
);


