import requests
import pandas as pd

def collecter_page(url, where=None, offset=0, limit=100):
    params = {
        "limit": limit,
        "offset": offset,
        "timezone": "Europe/Paris",
        "lang": "fr"
    }

    if where:
        params["where"] = where

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("results", [])

def collecter_regions():
    url = "https://geo.api.gouv.fr/regions"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []


def collecter_departements():
    url = "https://geo.api.gouv.fr/departements"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []


def collecter_communes():
    url = "https://geo.api.gouv.fr/communes?fields=nom,code,codeDepartement,population&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []


def collecter_pharmacies():
    url = (
        "https://www.data.gouv.fr/api/1/datasets/r/98f3161f-79ff-4f16-8f6a-6d571a80fea2"
    )

    df = pd.read_csv(
        url,
        sep=";",
        encoding="latin1",
        skiprows=1,
        header=None,
        dtype=str,
        low_memory=False,
    )

    return df


def collecter_page_lycees(offset, limit=100):
    url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/records"

    params = {
        "limit": limit,
        "offset": offset,
        "where": 'type_etablissement LIKE "LYCEE%"',
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("results", [])


def collecter_mairies():
    url = "https://api-lannuaire.service-public.gouv.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/exports/json"

    response = requests.get(url, params={"where": 'pivot LIKE "mairie"'}, timeout=30)
    response.raise_for_status()

    return response.json()

def collecter_colleges(limit=100):
    url_annuaire = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/records"
    url_effectifs = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-college-effectifs-niveau-sexe-lv/records"

    colleges = []
    offset = 0

    while True:
        params = {
            "limit": limit,
            "offset": offset,
            "where": "type_etablissement = 'Collège'"
        }

        response = requests.get(url_annuaire, params=params)
        response.raise_for_status()

        batch = response.json().get("results", [])

        if not batch:
            break

        colleges.extend(batch)
        offset += limit

    effectifs = []
    offset = 0

    while True:
        params = {
            "limit": limit,
            "offset": offset
        }

        response = requests.get(url_effectifs, params=params)
        response.raise_for_status()

        batch = response.json().get("results", [])

        if not batch:
            break

        effectifs.extend(batch)
        offset += limit

    return colleges, effectifs
