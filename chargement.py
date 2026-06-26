import os
import requests
import psycopg2
import pandas as pd

from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        os.getenv("DATABASE_URL")
    )


def creer_schema(chemin_schema="schema.sql"):

    with open(chemin_schema, "r", encoding="utf-8") as f:
        sql = f.read()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

    print("schema.sql appliqué avec succès.")


def charger_regions(df_regions):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_regions.iterrows():

        cur.execute("""
            INSERT INTO region(
                code_region,
                nom_region
            )
            VALUES (%s,%s)

            ON CONFLICT (code_region)
            DO NOTHING
        """,
        (
            row["code_region"],
            row["nom_region"]
        ))

    conn.commit()
    cur.close()
    conn.close()



def charger_departements(df_departements):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_departements.iterrows():

        cur.execute("""
            INSERT INTO departement(
                code_departement,
                nom_departement,
                code_region
            )
            VALUES (%s,%s,%s)

            ON CONFLICT (code_departement)
            DO NOTHING
        """,
        (
            row["code_departement"],
            row["nom_departement"],
            row["code_region"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_communes():

    conn = get_connection()
    cur = conn.cursor()

    df_departements = pd.read_sql(
        """
        SELECT code_departement
        FROM departement
        """,
        conn
    )

    for code_dept in df_departements[
        "code_departement"
    ]:

        print(
            f"Collecte département {code_dept}"
        )

        url = (
            f"https://geo.api.gouv.fr/"
            f"departements/{code_dept}/communes"
        )

        params = {
            "fields":
            "nom,code,population"
        }

        response = requests.get(
            url,
            params=params
        )

        if response.status_code != 200:
            continue

        communes = response.json()

        for commune in communes:

            cur.execute("""
                INSERT INTO commune(
                    code_insee,
                    nom_commune,
                    code_departement,
                    population
                )
                VALUES (%s,%s,%s,%s)

                ON CONFLICT (code_insee)
                DO NOTHING
            """,
            (
                commune["code"],
                commune["nom"],
                code_dept,
                commune.get(
                    "population",
                    0
                )
            ))

    conn.commit()
    cur.close()
    conn.close()


def charger_mairies():

    conn = get_connection()
    cur = conn.cursor()

    url = (
        "https://api-lannuaire.service-public.gouv.fr/api/explore/v2.1/"
        "catalog/datasets/"
        "api-lannuaire-administration/records"
    )

    params = {
        "where": 'pivot="mairie"',
        "limit": 100
    }

    response = requests.get(
        url,
        params=params
    )

    if response.status_code != 200:
        return

    resultats = response.json()

    for mairie in resultats.get(
        "results",
        []
    ):

        # noms de champs à vérifier  : l'API ne documente pas
        # toujours bien sa structure.faire un print(mairie) une fois pour
        # confirmer les clefs exactes avant de lancer la collecte complète.
        cur.execute("""
            INSERT INTO mairie(
                code_insee,
                nom_mairie,
                adresse,
                telephone,
                url
            )
            VALUES (%s,%s,%s,%s,%s)

            ON CONFLICT (code_insee)
            DO NOTHING
        """,
        (
            mairie.get("code_insee_commune"),
            mairie.get("nom"),
            mairie.get("adresse"),
            mairie.get("telephone"),
            mairie.get("url")
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_lycees(df_lycees):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_lycees.iterrows():

        cur.execute("""
            INSERT INTO lycee(
                uai,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee
            )
            VALUES (%s,%s,%s,%s,%s,%s)

            ON CONFLICT (uai)
            DO NOTHING
        """,
        (
            row["uai"],
            row["nom"],
            row["adresse"],
            row["latitude"],
            row["longitude"],
            row["code_insee"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_colleges(df_colleges):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_colleges.iterrows():

        cur.execute("""
            INSERT INTO college(
                uai,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee,
                nb_eleves
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)

            ON CONFLICT (uai)
            DO NOTHING
        """,
        (
            row["uai"],
            row["nom"],
            row["adresse"],
            row["latitude"],
            row["longitude"],
            row["code_insee"],
            row.get("nb_eleves")
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_mesures_lycee(df_mesures):
    """
    mesure_lycee référence id_lycee (clef technique) et pas l'UAI :
    on va chercher l'id_lycee correspondant avant d'insérer la mesure.
    Un lycée non trouvé (pas encore chargé) est simplement ignoré.
    """

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_mesures.iterrows():

        cur.execute("""
            SELECT id_lycee
            FROM lycee
            WHERE uai = %s
        """,
        (row["uai"],))

        resultat = cur.fetchone()

        if resultat is None:
            continue

        id_lycee = resultat[0]

        cur.execute("""
            INSERT INTO mesure_lycee(
                id_lycee,
                annee,
                nb_eleves
            )
            VALUES (%s,%s,%s)

            ON CONFLICT (id_lycee, annee)
            DO NOTHING
        """,
        (
            id_lycee,
            row["annee"],
            row["nb_eleves"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_pharmacies(df_pharmacies):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_pharmacies.iterrows():

        cur.execute("""
            INSERT INTO pharmacie(
                finess,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee
            )
            VALUES (%s,%s,%s,%s,%s,%s)

            ON CONFLICT (finess)
            DO NOTHING
        """,
        (
            row["finess"],
            row["nom"],
            row["adresse"],
            row["latitude"],
            row["longitude"],
            row["code_insee"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_ehpad(df_ehpad):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_ehpad.iterrows():

        cur.execute("""
            INSERT INTO ehpad(
                finess,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee,
                capacite_lits
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)

            ON CONFLICT (finess)
            DO NOTHING
        """,
        (
            row["finess"],
            row["nom"],
            row["adresse"],
            row["latitude"],
            row["longitude"],
            row["code_insee"],
            row.get("capacite_lits")
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_gares(df_gares):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_gares.iterrows():

        cur.execute("""
            INSERT INTO gare(
                code_uic,
                nom,
                latitude,
                longitude,
                code_insee
            )
            VALUES (%s,%s,%s,%s,%s)

            ON CONFLICT (code_uic)
            DO NOTHING
        """,
        (
            row["code_uic"],
            row["nom"],
            row["latitude"],
            row["longitude"],
            row["code_insee"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_frequentation_gares(df_frequentations):
    """
    Ici on veut vraiment mettre à jour la valeur si elle existe déjà
    (une fréquentation se rafraîchit d'une année sur l'autre) : DO NOTHING
    ne suffit pas, il faut DO UPDATE sur ce cas précis.
    """

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_frequentations.iterrows():

        cur.execute("""
            UPDATE gare
            SET voyageurs_par_an = %s,
                annee_mesure = %s
            WHERE code_uic = %s
        """,
        (
            row["voyageurs_par_an"],
            row["annee_mesure"],
            row["code_uic"]
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_bibliotheques(df_bibliotheques):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_bibliotheques.iterrows():

        cur.execute("""
            INSERT INTO bibliotheque(
                identifiant_source,
                nom,
                adresse,
                latitude,
                longitude,
                code_insee,
                nb_inscrits
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)

            ON CONFLICT (identifiant_source)
            DO NOTHING
        """,
        (
            row["identifiant_source"],
            row["nom"],
            row["adresse"],
            row["latitude"],
            row["longitude"],
            row["code_insee"],
            row.get("nb_inscrits")
        ))

    conn.commit()
    cur.close()
    conn.close()


def charger_entreprises_btp(df_entreprises):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df_entreprises.iterrows():

        cur.execute("""
            INSERT INTO entreprise_btp(
                siren,
                raison_sociale,
                code_naf,
                adresse,
                latitude,
                longitude,
                code_insee,
                tranche_effectif
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

            ON CONFLICT (siren)
            DO NOTHING
        """,
        (
            row["siren"],
            row["raison_sociale"],
            row.get("code_naf"),
            row.get("adresse"),
            row.get("latitude"),
            row.get("longitude"),
            row["code_insee"],
            row.get("tranche_effectif")
        ))

    conn.commit()
    cur.close()
    conn.close()
