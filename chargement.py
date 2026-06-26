import psycopg2
import os


def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def charger_regions(regions):
    conn = get_connection()
    cur = conn.cursor()

    for _, r in regions.iterrows():
        cur.execute(
            """
            INSERT INTO region (
                code_region,
                nom_region
            )
            VALUES (%s, %s)
            ON CONFLICT (code_region) DO NOTHING;
        """,
            (r["code_region"], r["nom_region"]),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("regions chargés.")

def charger_departements(departements):
    conn = get_connection()
    cur = conn.cursor()

    for _, d in departements.iterrows():
        cur.execute(
            """
            INSERT INTO departement (
                code_departement,
                nom_departement,
                code_region
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (code_departement) DO NOTHING;
        """,
            (d["code_departement"], d["nom_departement"], d["code_region"]),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("departements chargés.")

def charger_communes(communes):
    conn = get_connection()
    cur = conn.cursor()

    for _, c in communes.iterrows():
        cur.execute(
            """
            INSERT INTO commune (
                code_insee,
                nom_commune,
                code_departement,
                population
            )
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (code_insee) DO NOTHING;
        """,
            (c["code_insee"], c["nom_commune"], c["code_departement"], c["population"]),
        )

    conn.commit()
    cur.close()
    conn.close()

    print("Communes chargés.")

def charger_pharmacies(pharmacies):
    conn = get_connection()
    cur = conn.cursor()

    for _, p in pharmacies.iterrows():
        cur.execute(
            """
            INSERT INTO pharmacie (
                finess,
                nom,
                adresse,
                code_postal,
                code_insee
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (finess) DO NOTHING;
            """,
            (
                p["finess"],
                p["nom"],
                p["adresse"],
                p["code_postal"],
                p["code_insee"],
            ),
        )

    conn.commit()

    cur.close()
    conn.close()

    print("Pharmacies chargées.")

def charger_lycees(lycees_clean):
    conn = get_connection()
    cur = conn.cursor()

    for lycee in lycees_clean:
        cur.execute(
            """
            INSERT INTO lycee (
                uai,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee
            )
            SELECT %s, %s, %s, %s, %s, %s
            WHERE EXISTS (
                SELECT 1
                FROM commune
                WHERE code_insee = %s
            )
            ON CONFLICT (uai) DO UPDATE SET
                nom = EXCLUDED.nom,
                adresse = EXCLUDED.adresse,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                code_insee = EXCLUDED.code_insee;
            """,
            (
                lycee["uai"],
                lycee["nom"],
                lycee["adresse"],
                lycee["latitude"],
                lycee["longitude"],
                lycee["code_insee"],
                lycee["code_insee"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

    #print(" Lycées chargés")


def charger_mairies(mairies_clean):
    conn = get_connection()
    cur = conn.cursor()

    for mairie in mairies_clean:
        cur.execute(
            """
            INSERT INTO mairie (
                code_insee,
                adresse,
                latitude,
                longitude
            )
            SELECT %s, %s, %s, %s
            WHERE EXISTS (
                SELECT 1
                FROM commune
                WHERE code_insee = %s
            )
            ON CONFLICT (code_insee) DO NOTHING;
            """,
            (
                mairie["code_insee"],
                mairie["adresse"],
                mairie["latitude"],
                mairie["longitude"],
                mairie["code_insee"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

    print(" Mairies chargés")

def charger_colleges(colleges_clean):
    conn = get_connection()
    cur = conn.cursor()

    for college in colleges_clean:
        cur.execute(
            """
            INSERT INTO college (
                uai,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee,
                nb_eleves
            )
            SELECT %s, %s, %s, %s, %s, %s, %s
            WHERE EXISTS (
                SELECT 1
                FROM commune
                WHERE code_insee = %s
            )
            ON CONFLICT (uai) DO UPDATE SET
                nom = EXCLUDED.nom,
                adresse = EXCLUDED.adresse,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                code_insee = EXCLUDED.code_insee,
                nb_eleves = EXCLUDED.nb_eleves;
            """,
            (
                college["uai"],
                college["nom"],
                college["adresse"],
                college["latitude"],
                college["longitude"],
                college["code_insee"],
                college["nb_eleves"],
                college["code_insee"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

    # print("Collèges chargés")

def charger_gares(gares_clean):
    conn = get_connection()
    cur = conn.cursor()

    for gare in gares_clean:
        cur.execute(
            """
            INSERT INTO gare (
                code_uic,
                nom,
                latitude,
                longitude,
                code_insee,
                voyageurs_par_an,
                annee_mesure
            )
            SELECT %s, %s, %s, %s, %s, %s, %s
            WHERE EXISTS (
                SELECT 1
                FROM commune
                WHERE code_insee = %s
            )
            ON CONFLICT (code_uic) DO UPDATE SET
                nom = EXCLUDED.nom,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                code_insee = EXCLUDED.code_insee,
                voyageurs_par_an = EXCLUDED.voyageurs_par_an,
                annee_mesure = EXCLUDED.annee_mesure;
            """,
            (
                gare["code_uic"],
                gare["nom"],
                gare["latitude"],
                gare["longitude"],
                gare["code_insee"],
                gare["voyageurs_par_an"],
                gare["annee_mesure"],
                gare["code_insee"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()

    #print(f"{len(gares_clean)} gares chargées.")