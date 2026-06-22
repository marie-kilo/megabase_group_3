# Brief 00 : modéliser et créer la base + setup

> Avant d'écrire une seule donnée en base, on conçoit sa structure. Ce brief a pour but de poser les fondations : l'environnement de travail, le dépôt du groupe, et le schéma de la base, avec la commune au centre.

> Compétence visée (RNCP-37638) : **C11, niveau 2** (créer une base de données en
> élaborant les modèles conceptuels et physiques). Réinvestit la modélisation
> MERISE.

## Le projet

- Le groupe construit une base de données qui réunit le plus de sources possible sur les communes françaises (lycées, pharmacies, gares, entreprises du bâtiment, bibliothèques...), toutes reliées entre elles **🔴 au moins par la commune**. 

- Plus on intègre de sources correctement reliées, plus la base est riche. 

> Ce premier brief pose les fondations sur lesquelles tous les suivants s'appuient.



## Le catalogue des typologies

| Typologie | Source principale (open data) | Mesure d'activité | Lieux d'intérêt suggérés | Cas métier |
|---|---|---|---|---|
| Lycées | annuaire de l'éducation + API `data.education.gouv.fr` (effectifs) | nombre d'élèves (voie générale) | cafés, fast-foods, boulangeries | implantation d'une offre jeunes (typologie par défaut : corrigé et données de secours fournis) |
| Mairies | API découpage administratif (`geo.api.gouv.fr`) + annuaire de l'administration (data.gouv.fr) | population de la commune | papeteries, imprimeurs, cafés | services aux administrés, prospection B2G |
| Entreprises du BTP | API recherche d'entreprises (`recherche-entreprises.api.gouv.fr`), codes NAF 41/42/43 | effectif salarié (tranche) | fournisseurs de matériaux, loueurs d'engins, restaurants ouvriers | implantation d'un négoce de matériaux |
| Pharmacies | base FINESS (data.gouv.fr) | population de la commune (proxy de patientèle) | médecins, laboratoires d'analyses, EHPAD | maillage officinal, zones sous-dotées |
| Bibliothèques | base des bibliothèques (data.culture.gouv.fr) | nombre d'inscrits ou population | écoles, cafés, librairies | politique de lecture publique |
| Gares voyageurs | open data SNCF (fréquentation des gares) | voyageurs par an | hôtels, loueurs de vélos, cafés | services en gare |
| Collèges | annuaire de l'éducation + effectifs collèges | nombre d'élèves | équipements sportifs, fast-foods | carte scolaire et abords |
| EHPAD | base FINESS | capacité d'accueil (lits) | pharmacies, cabinets infirmiers, fleuristes | services aux résidents et familles |

Une typologie hors catalogue est possible si vous la faites valider : il faut une source open data fiable avec géolocalisation (ou adresse géocodable via la BAN, `api-adresse.data.gouv.fr`) et une mesure d'activité.


## Situation professionnelle

> Vous êtes data engineer dans une agence qui veut bâtir un observatoire des territoires. On vous demande de poser le modèle avant de collecter quoi que ce soit : quelles tables, quelles clefs, comment tout se relie. 

🔴 **Attention :** un modèle bâclé vous compliquera l'ajout de sources supplémentaires.

## 1. Mettre en place l'environnement (pyenv et Git)

Un dépôt par groupe. Un membre le crée, les autres membres le rejoignent.

- Un membre crée un dépôt GitHub privé (au format `megabase-groupe-<GROUP_NUMBER>` par exemple `megabase-groupe-3`) et ajoute les autres membres et le formateur comme collaborateurs. Tout le monde le clone.
- L'environnement Python avec pyenv :

  ```bash
  pyenv install 3.14.5
  pyenv local 3.14.5
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt        # requests, psycopg2-binary, python-dotenv
  ```

- Les secrets hors du dépôt : la connexion à la base va dans un `.env` (jamais versionné), on versionne un `.env.example` avec les clefs vides.
- Le `.gitignore` dès le départ : `env`, `.env`, `__pycache__`, `.ipynb_checkpoints`...

## 2. Adopter la structure du projet

Le code s'organise par responsabilité, un script par rôle. Reproduisez cette
arborescence dans votre dépôt :

```
megabase-groupe-1/
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── schema.sql           la structure de la base (la commune au centre)
├── collecte.py          les appels aux API open data (🔴 pour plus tard)
├── nettoyage.py         la normalisation du code INSEE (🔴 pour plus tard)
├── chargement.py        la création du schéma et l'insertion (🔴 pour plus tard)
├── analyses.sql         les requêtes qui croisent les sources (🔴 pour plus tard)
└── main.py              le point d'entrée : collecte, nettoie, charge (🟢)
```

> 🟢 Vous pouvez d'ores et déjà créer votre BDD en exécutant le `schema.sql` depuis le `main.py`

(La structure s'étoffera au fur et à mesure des briefs suivants : entrepôt, dbt, déploiement.)

## 3. Modéliser avec MERISE

Quelle que soit la source, on retombe sur les mêmes briques :

- **l'établissement** : le point principal (un lycée, une pharmacie...), avec un
  identifiant stable, une position, et **rattaché à une commune** ;
- 🌈 **la commune** : le point de rattachement commun à toutes les sources. Réfléchissez bien à la façon dont vous gérerez ces points de rattachement d'un point de vue SQL.
- Parfois seulement **une mesure** : un indicateur d'activité daté (nombre d'élèves, population...) ;

Produisez le modèle conceptuel (MCD : entités, associations, cardinalités) puis le modèle logique (MLD : clefs primaires et étrangères explicites). La commune doit être au centre, 🔴 **vous choisirez comment identifier les communes**.

## 4. Écrire `schema.sql` et créer la base

Traduisez le modèle en `CREATE TABLE` PostgreSQL :

- une table `commune` (choisir une clef primaire) ;
- une première table de typologie (par exemple `lycee`), reliée à `commune` par une
  **clef étrangère** sur le code INSEE ;
- les contraintes qui protègent la base : `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`.

Créez la base locale `megabase` et appliquez le schéma.


## 5. Ajouter au `schema.sql` les tables pour les autres typologies
- une table par typologie, reliée à `commune` par une **clef étrangère**


## Livrables

| Livrable | Forme |
|---|---|
| Dépôt GitHub du groupe, environnement reproductible | dépôt + `requirements.txt` + `.env.example` |
| Le modèle conceptuel et logique | MCD et MLD (schéma versionné) |
| Le schéma physique | `schema.sql` appliqué sur la base |
| Liste des commandes utilisées | `commands.md` (toutes les commandes que vous utiliserez au cours du **projet**) |

## Indicateurs de performance

- l'environnement est reproductible (pyenv, venv, `requirements.txt`) et les secrets
  sont hors du dépôt ;
- le modèle fait apparaître la commune au centre et les bonnes cardinalités ;
- `schema.sql` crée la base sans erreur (lorsqu'exécuté depuis `main.py`), avec des contraintes (clefs, `NOT NULL`) ;
- l'arborescence et les noms de scripts sont respectés.

## Modalités

- Travail en groupe
- Prérequis : bases de SQL, exécution de SQL avec Python (psycopg2), notions de MERISE.
- Durée indicative : une journée.
