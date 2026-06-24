-- Table des communes (ton pivot)
CREATE TABLE IF NOT EXISTS commune (
    code_insee VARCHAR(5) PRIMARY KEY,
    nom_commune VARCHAR(255) NOT NULL
);

-- Table des EHPAD
CREATE TABLE IF NOT EXISTS ehpad (
    finess_id VARCHAR(10) PRIMARY KEY, -- noFinesset
    nom VARCHAR(255) NOT NULL,         -- title
    adresse TEXT,                      -- coordinates.street
    capacite_lits INTEGER,             -- capacity
    code_insee VARCHAR(5) NOT NULL,    -- À créer via nettoyage
    latitude DECIMAL(9,6),             -- coordinates.latitude
    longitude DECIMAL(9,6),            -- coordinates.longitude
    CONSTRAINT fk_commune FOREIGN KEY (code_insee) REFERENCES commune(code_insee)
);