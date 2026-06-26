"""Clean: une ligne de l'API -> tuple (key, name, insee_code)."""

# Lyon arrondissements ne sont pas dans la liste des commuunes:
# on les ramène dans Lyon
DISTRICTS = {str(c): "69123" for c in range(69381, 69390)}


def normalize_insee(code):
    code = str(code).strip()
    return DISTRICTS.get(code, code)


def clean_education(row):
    return (
        row.get("identifiant_de_l_etablissement"),
        row.get("nom_etablissement"),
        normalize_insee(row.get("code_commune")),
    )


def clean_finess(row):
    return (row.get("nofinesset"), row.get("rs"), normalize_insee(row.get("com_code")))
