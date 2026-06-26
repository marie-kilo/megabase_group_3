from dotenv import load_dotenv
import psycopg2
from psycopg2 import errors
import os

from collecte import (
    collecter_regions,
    collecter_departements,
    collecter_communes,
    #collecter_mairies,
    #collecter_pharmacies,
    #collecter_page_lycees,
    #collecter_colleges,
    collecter_page
)

from nettoyage import (
    nettoyer_regions,
    nettoyer_departements,
    nettoyer_communes,
    nettoyer_mairies,
    #nettoyer_pharmacies,
    nettoyer_lycees,
    nettoyer_colleges,
    nettoyer_gares,
)

from chargement import (
    charger_regions,
    charger_departements,
    charger_communes,
    charger_mairies,
    #charger_pharmacies,
    charger_lycees,
    charger_colleges,
    charger_gares,
)

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME_INIT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

conn.autocommit = True

cur = conn.cursor()

try:
    cur.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
except errors.DuplicateDatabase:
    print("La base existe déjà")

cur.close()
conn.close()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cur = conn.cursor()

with open("schema.sql", "r", encoding="utf-8") as f:
    sql = f.read()

cur.execute(sql)

conn.commit()

cur.close()
conn.close()

print("Base créée avec succès")

educ = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets"
gare = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/gares-de-voyageurs/records"

SOURCES = [
    {
        "table": "lycee",
        "key": "uai",
        "url": f"{educ}/fr-en-annuaire-education/records",
        "where": 'type_etablissement LIKE "LYCEE%"',
        "select": (
            "identifiant_de_l_etablissement,"
            "nom_etablissement,"
            "adresse_1,"
            "adresse_2,"
            "adresse_3,"
            "latitude,"
            "longitude,"
            "code_commune"
        ),
        "order_by": "identifiant_de_l_etablissement",
        "clean": nettoyer_lycees,
    },
    {
        "table": "college",
        "key": "uai",
        "url": f"{educ}/fr-en-annuaire-education/records",
        "where": "type_etablissement = 'Collège'",
        "select": (
            "identifiant_de_l_etablissement,"
            "nom_etablissement,"
            "adresse_1,"
            "adresse_2,"
            "adresse_3,"
            "latitude,"
            "longitude,"
            "code_commune"
        ),
        "order_by": "identifiant_de_l_etablissement",
        "clean": nettoyer_colleges,
    },
    {
        "table": "gare",
        "key": "code_uic",
        "url": gare,
        "where": None,
        "clean": nettoyer_gares,
    },
]


# collecte des données régions departement communes  :
regions = collecter_regions()
departements = collecter_departements()
communes = collecter_communes()

# nettoyage des données régions departement communes :
regions_clean = nettoyer_regions(regions)
departements_clean = nettoyer_departements(departements)
communes_clean = nettoyer_communes(communes)
communes_clean = communes_clean[
    communes_clean["code_departement"].isin(departements_clean["code_departement"])
]

# chargement des données régions departement communes :
charger_regions(regions_clean)
charger_departements(departements_clean)
charger_communes(communes_clean)

# --------------------------------------------------------------------------

# collecte nettoyage et chargement de mairie :
# mairies_brutes = collecter_mairies()
# mairies_clean = nettoyer_mairies(mairies_brutes)
# charger_mairies(mairies_clean)

for source in SOURCES:
    print(f"Traitement de {source['table']}")

    offset = 0
    limit = 100

    while True:
        data = collecter_page(
            url=source["url"],
            where=source["where"],
            offset=offset,
            limit=limit
        )

        if not data:
            break

        data_clean = source["clean"](data)

        if source["table"] == "lycee":
            charger_lycees(data_clean)

        elif source["table"] == "college":
            charger_colleges(data_clean)

        elif source["table"] == "gare":
            charger_gares(data_clean)

        offset += limit

    print(f"{source['table']} terminé")


# collecte nettoyage et chargement de lycee via pagination  :

# LIMIT = 100

# offset = 0

# while True:
#     lycees = collecter_page_lycees(offset, LIMIT)

#     if not lycees:
#         break

#     lycees_clean = nettoyer_lycees(lycees)
#     charger_lycees(lycees_clean)

#     # print(f"{len(lycees_clean)} lycées chargés")

#     offset += LIMIT

# print("Import terminé.")

# collecte nettoyage et chargement de pharmacie

# pharmacies = collecter_pharmacies()
# pharmacies_clean = nettoyer_pharmacies(pharmacies)
# pharmacies_clean = pharmacies_clean[
#     pharmacies_clean["code_insee"].isin(communes_clean["code_insee"])
# ]
# charger_pharmacies(pharmacies_clean)clear
