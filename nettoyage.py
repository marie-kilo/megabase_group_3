import pandas as pd
import json

def nettoyer_regions(data):
    regions = pd.DataFrame(data)

    regions = regions.rename(columns={"code": "code_region", "nom": "nom_region"})

    regions = regions[["code_region", "nom_region"]]

    regions = regions.drop_duplicates(subset=["code_region"])

    regions = regions.fillna("")

    return regions


def nettoyer_departements(data):
    departements = pd.DataFrame(data)

    departements = departements.rename(
        columns={
            "code": "code_departement",
            "nom": "nom_departement",
            "codeRegion": "code_region",
        }
    )

    departements = departements[["code_departement", "nom_departement", "code_region"]]

    departements = departements.drop_duplicates(subset=["code_departement"])

    departements = departements.fillna("")

    return departements


def nettoyer_communes(data):
    communes = pd.DataFrame(data)

    communes = communes.rename(
        columns={
            "code": "code_insee",
            "nom": "nom_commune",
            "codeDepartement": "code_departement",
            "population": "population",
        }
    )

    communes = communes[["code_insee", "nom_commune", "code_departement", "population"]]

    communes = communes.drop_duplicates(subset=["code_insee"])

    communes = communes.fillna("")

    return communes

def nettoyer_pharmacies(df):
    df = df.rename(columns={
        1: "finess",
        3: "nom",
        7: "numero_voie",
        8: "type_voie",
        9: "libelle_voie",
        12: "code_commune_3",
        13: "code_departement",
        15: "code_postal_ville",
        18: "code_categorie",
        19: "libelle_categorie"
    })

    pharmacies = df[
        df["libelle_categorie"].str.contains(
            "pharm|officine",
            case=False,
            na=False
        )
    ].copy()

    pharmacies["code_insee"] = (
        pharmacies["code_departement"].str.zfill(2)
        + pharmacies["code_commune_3"].str.zfill(3)
    )

    pharmacies["adresse"] = (
        pharmacies["numero_voie"].fillna("") + " " +
        pharmacies["type_voie"].fillna("") + " " +
        pharmacies["libelle_voie"].fillna("")
    ).str.strip()

    pharmacies["code_postal"] = pharmacies["code_postal_ville"].str.extract(r"(\d{5})")

    pharmacies_clean = pharmacies[
        [
            "finess",
            "nom",
            "adresse",
            "code_postal",
            "code_insee"
        ]
    ].copy()

    pharmacies_clean = pharmacies_clean.drop_duplicates(subset=["finess"])

    pharmacies_clean = pharmacies_clean.fillna("")

    pharmacies_clean = pharmacies_clean.reset_index(drop=True)

    return pharmacies_clean

def nettoyer_lycees(lycees_bruts):
    lycees_clean = []

    for l in lycees_bruts:
        uai = l.get("identifiant_de_l_etablissement")
        nom = l.get("nom_etablissement")
        code_insee = l.get("code_commune")

        adresse = " ".join([
            str(l.get("adresse_1") or ""),
            str(l.get("adresse_2") or ""),
            str(l.get("adresse_3") or "")
        ]).strip()

        latitude = l.get("latitude")
        longitude = l.get("longitude")

        # Champs obligatoires SQL
        if not nom or not code_insee:
            continue

        # code_insee doit faire 5 caractères
        code_insee = str(code_insee).zfill(5)

        lycee = {
            "uai": str(uai).strip() if uai else None,
            "nom": str(nom).strip()[:255],
            "adresse": adresse if adresse else None,
            "latitude": latitude,
            "longitude": longitude,
            "code_insee": code_insee
        }

        lycees_clean.append(lycee)

    return lycees_clean

def nettoyer_mairies(mairies_brutes):
    mairies_clean = []

    for m in mairies_brutes:

        try:
            adresses = json.loads(m.get("adresse", "[]"))
        except:
            adresses = []

        if adresses:
            adr = adresses[0]
        else:
            adr = {}

        adresse = " ".join(filter(None, [
            adr.get("numero_voie"),
            adr.get("code_postal"),
            adr.get("nom_commune")
        ])).strip()

        mairie = {
            "adresse": adresse if adresse else None,
            "latitude": adr.get("latitude"),
            "longitude": adr.get("longitude"),
            "code_insee": str(m.get("code_insee_commune")).zfill(5)
        }

        if mairie["code_insee"] != "None":
            mairies_clean.append(mairie)

    return mairies_clean

def nettoyer_colleges(colleges):
    colleges_clean = []

    for c in colleges:
        uai = c.get("identifiant_de_l_etablissement")
        nom = c.get("nom_etablissement")
        code_insee = c.get("code_commune")

        if not uai or not nom or not code_insee:
            continue

        adresse = " ".join([
            str(c.get("adresse_1") or ""),
            str(c.get("adresse_2") or ""),
            str(c.get("adresse_3") or "")
        ]).strip()

        colleges_clean.append({
            "uai": uai,
            "nom": nom,
            "adresse": adresse,
            "latitude": c.get("latitude"),
            "longitude": c.get("longitude"),
            "code_insee": code_insee,
            "nb_eleves": None
        })

    return colleges_clean

def nettoyer_gares(gares):
    gares_clean = []

    for g in gares:
        position = g.get("position_geographique") or {}

        code_uic = g.get("codes_uic")
        nom = g.get("nom")
        code_insee = g.get("codeinsee")

        if not code_uic or not nom or not code_insee:
            continue

        code_uic = str(code_uic).split(";")[0].split(",")[0].strip()

        gares_clean.append({
            "code_uic": code_uic,
            "nom": nom,
            "latitude": position.get("lat"),
            "longitude": position.get("lon"),
            "code_insee": str(code_insee).zfill(5),
            "voyageurs_par_an": None,
            "annee_mesure": None,
        })

    return gares_clean