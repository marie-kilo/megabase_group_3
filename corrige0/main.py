"""Build the megabase:
- on boucle sur les sources
    - on "pagine" sur chaque (i.e. on boucle sur les pages=chunks)
        - on recupère les chunks un par un
        - on nettoie chunk par chunk
        - on charge chunk par chunk
createdb megabase0
python3 main.py

- collect / clean / load logic : 3 fichiers
- ici, on agence juste la logique : i.e l'orchestration chunk par chunk
"""

import collect
import clean
import load

DEPT = "69"

EDUCATION = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets"
FINESS = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets"


SOURCES = [
    {
        "table": "lycee",
        "key": "uai",
        "url": f"{EDUCATION}/fr-en-annuaire-education/records",
        "where": f'code_departement="{DEPT.zfill(3)}" and type_etablissement="Lycée"',
        "select": "identifiant_de_l_etablissement,nom_etablissement,code_commune",
        "order_by": "identifiant_de_l_etablissement",
        "clean": clean.clean_education,
    },
    {
        "table": "college",
        "key": "uai",
        "url": f"{EDUCATION}/fr-en-annuaire-education/records",
        "where": f'code_departement="{DEPT.zfill(3)}" and type_etablissement="Collège"',
        "select": "identifiant_de_l_etablissement,nom_etablissement,code_commune",
        "order_by": "identifiant_de_l_etablissement",
        "clean": clean.clean_education,
    },
    {
        "table": "pharmacie",
        "key": "finess",
        "url": f"{FINESS}/healthref-france-finess/records",
        "where": f'dep_code="{DEPT}" and libcategetab like "Pharmacie"',
        "select": "nofinesset,rs,com_code",
        "order_by": "nofinesset",
        "clean": clean.clean_finess,
    },
]

conn = load.connect()
cur = conn.cursor()
load.create_schema(cur)

# Toutes les communes en 1 call. On garde la liste des communes connues
communes = collect.fetch_communes(DEPT)
known_communes = load.insert_communes(cur, communes)
conn.commit()
print(f"commune  : {len(known_communes)}")

# Loop of loops: loop sur les sources, puis loop sur les pages
for source in SOURCES:
    # reprise : on repart de là où un run précédent (interrompu) s'est arrêté,
    # en comptant les lignes déjà présentes dans la table
    offset = load.count_rows(cur, source["table"])
    seen = set()  # keys déjà vues (deduplication)
    while True:
        rows = collect.fetch_page(
            source["url"],
            source["where"],
            source["select"],
            source["order_by"],
            offset,
        )
        if not rows:
            break  # plus de pages

        # on nettoie le chunk, on garde les rows avec une key, une commune connue, pas encore vues
        chunk = []
        for row in rows:
            # Option 1 pour nettoyage
            # if source["table"] == "lycee":
            #     func_clean = clean.clean_education
            # elif source["table"] == "college":
            #     func_clean = clean.clean_education
            # elif source["table"] == "pharmacie":
            #     func_clean = clean.clean_finess
            # key, name, insee = func_clean(row)

            # Option 2 pour nettoyage
            key, name, insee = source["clean"](row)
            if key and insee in known_communes and key not in seen:
                seen.add(key)
                chunk.append((key, name, insee))

        load.insert_chunk(cur, source["table"], source["key"], chunk)
        conn.commit()  # on valide chaque page : si ça s'interrompt, c'est gardé

        offset += 100
        if offset >= 1_000_000:  # safety guard: the API refuse au délà de 1_000_000
            break
    print(f"{source['table']:9}: {load.count_rows(cur, source['table'])}")

conn.commit()
conn.close()
