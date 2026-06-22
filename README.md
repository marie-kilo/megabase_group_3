# Les briefs du projet méga-base

- Le projet s'ouvre par un brief d'organisation (00), puis se mène en six briefs, dans l'ordre. 
- Chacun réutilise le précédent. 
- Le brief d'organisation via la méthode agile est le **deuxième** brief. Tous les autres briefs sont des briefs techniques.


| # | Brief | Ce qu'on produit | Durée indicative |
|---|---|---|---|
| 00 | [Modéliser et créer la base](00_brief_modelisation.md) | setup, dépôt du groupe, schéma relationnel | 1 jour |
| 01 | [Préparer son organisation de travail](01_brief_agile.md) | rôles, sprints, tableau de suivi, 2-3 slides | 2 heures |
| 02 | [Collecter et nettoyer une source](02_brief_collecte_nettoyage.md) | collecte paramétrée, nettoyage du code INSEE | 1 jour |
| 03 | [Intégrer plusieurs sources](03_brief_integration.md) | le plus de sources possible, reliées par la commune | 2 jours |
| 04 | [Créer le data warehouse](04_brief_entrepot.md) | entrepôt en étoile, ETL, requêtes OLAP | 2 jours |
| 05 | [dbt](05_brief_dbt.md) | transformations versionnées et testées | 1 jour |
| 06 | [Déployer et restituer](06_brief_deploiement.md) | mise en ligne Scalingo, accès analyste, soutenance | 1 jour |

Soit environ huit jours (modules réglementaires non compris).

Tous les briefs suivent le même format: 
- situation professionnelle
- étapes numérotées
- livrables
- indicateurs de performance
- compétences visées et durée

> 💫 Faites bien attention à prendre en compte ces 5 éléments lors de vos travaux.

Le travail se mène en groupe et en méthode agile (sprints, point quotidien, tableau de suivi), comme décrit dans le brief 01.

## Glossaire des sigles

Les sigles employés dans les briefs, développés une fois ici.

- **API** : interface de programmation. Une adresse web qui renvoie des données lisibles par un programme (souvent du JSON).
- **BAN** : Base Adresse Nationale. Le service public de géocodage des adresses françaises.
- **B2G** : business to government. La prospection ou la vente vers le secteur public.
- **BTP** : bâtiment et travaux publics.
- **CTE** : common table expression. Une sous-requête nommée, le `WITH` en SQL.
- **dbt** : data build tool. Un outil qui organise les transformations SQL en modèles versionnés et testés.
- **DWH** : data warehouse. L'entrepôt de données (le schéma `dwh` du projet).
- **EHPAD** : établissement d'hébergement pour personnes âgées dépendantes.
- **ELT** : extract, load, transform. On charge le brut, puis on transforme dans la base.
- **ETL** : extract, transform, load. On extrait, on transforme, puis on charge.
- **FINESS** : le répertoire national des établissements sanitaires et sociaux.
- **MCD** : modèle conceptuel de données (entités, associations, cardinalités).
- **MLD** : modèle logique de données (clés primaires et étrangères).
- **NAF** : nomenclature d'activités française. Les codes d'activité des entreprises.
- **OLAP** : online analytical processing. Une base organisée pour analyser et croiser : l'entrepôt.
- **OLTP** : online transaction processing. Une base organisée pour écrire proprement : la base relationnelle.
- **RNCP** : Répertoire national des certifications professionnelles. Le titre visé porte le numéro 37638.
- **SNCF** : Société nationale des chemins de fer français.
- **SQL** : structured query language. Le langage des bases de données relationnelles.
- **URL** : uniform resource locator. Une adresse, ici la chaîne de connexion à la base.
