-- Simple schema: the commune at the center, typologies linked by the INSEE code.
-- Tables are kept across runs: an interrupted load can resume where it stopped.

CREATE TABLE IF NOT EXISTS commune (
    insee_code TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    population INTEGER
);

CREATE TABLE IF NOT EXISTS lycee (
    uai        TEXT PRIMARY KEY,
    name       TEXT,
    insee_code TEXT REFERENCES commune (insee_code)
);

CREATE TABLE IF NOT EXISTS college (
    uai        TEXT PRIMARY KEY,
    name       TEXT,
    insee_code TEXT REFERENCES commune (insee_code)
);

CREATE TABLE IF NOT EXISTS pharmacie (
    finess     TEXT PRIMARY KEY,
    name       TEXT,
    insee_code TEXT REFERENCES commune (insee_code)
);
