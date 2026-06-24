# 03: Aide mémoire

```bash
#!/usr/bin/env bash
#
# ============================================================================
#  AIDE-MÉMOIRE GIT — workflow à plusieurs, commenté ligne par ligne
#  branche individuelle datée → feature → tests → main   (merge uniquement)
# ============================================================================
#
#  Légende des termes employés :
#   - HEAD        : pointeur "tu es ici". Désigne le commit/la branche courante.
#   - index/stage : la "zone de préparation". Photo en attente du prochain commit.
#   - remote      : le dépôt distant (sur GitHub). Son petit nom par défaut = origin.
#   - upstream    : la branche distante que ta branche locale "suit" (pull/push auto).
#
# ----------------------------------------------------------------------------


# ════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 1 — Partir de la feature à jour
# ════════════════════════════════════════════════════════════════════════════

 git checkout feature/clean-data
#  └─ QUOI : déplace HEAD sur la branche feature/clean-data et met à jour les
#            fichiers du dossier de travail pour qu'ils correspondent à CE commit.
#  └─ POURQUOI : on veut TOUJOURS partir de la branche d'intégration commune avant
#               de créer sa propre branche, sinon on construit sur une base périmée.
#  └─ PIÈGE : si tu as des modifs non committées qui entrent en conflit, Git refuse
#            de changer de branche. Solution : committer, ou `git stash` pour mettre
#            de côté temporairement. (Git ≥ 2.23 : `git switch feature/clean-data`
#            est l'équivalent moderne, plus lisible.)

 git pull
#  └─ QUOI : raccourci pour `git fetch` + `git merge`. Va chercher les nouveaux
#            commits sur origin/feature/clean-data et les fusionne dans ta copie locale.
#  └─ POURQUOI : ton binôme a peut-être déjà fusionné son travail dans la feature.
#               Tu récupères son code AVANT de partir, pour rester synchronisé.
#  └─ PIÈGE : si toi ET le remote avez avancé, un `pull` peut ouvrir un merge (voire
#            un conflit). Ne lance jamais pull avec un dossier "sale" plein de modifs
#            non sauvegardées : commit/stash d'abord.


# ════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 2 — Créer sa branche individuelle datée
# ════════════════════════════════════════════════════════════════════════════

 git checkout -b prenom/AAAA-MM-JJ
#  └─ QUOI : le `-b` CRÉE une nouvelle branche ET bascule dessus dans la foulée.
#            Elle naît exactement sur le commit où tu te trouves (la pointe de la
#            feature que tu viens de mettre à jour).
#  └─ POURQUOI : isoler ton travail. Tu pourras committer librement sans gêner
#               personne ; la date dans le nom (ex. alice/2026-06-23) rend
#               l'historique d'équipe lisible et triable.
#  └─ PIÈGE : remplace littéralement `prenom/AAAA-MM-JJ` par TES valeurs, ex.
#            `alice/2026-06-23`. Le `/` est juste une convention de nommage (ça ne
#            crée pas de sous-dossier). Équivalent moderne : `git switch -c …`.


# ════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 3 — Coder, puis sauvegarder
# ════════════════════════════════════════════════════════════════════════════

 git status
#  └─ QUOI : photographie l'état du dossier. Affiche 3 catégories : fichiers
#            "staged" (prêts à committer, en vert), "modified" non staged (en rouge),
#            et "untracked" (nouveaux fichiers que Git ne suit pas encore).
#  └─ POURQUOI : vérifier AVANT d'agir ce que tu t'apprêtes réellement à enregistrer.
#               C'est la commande la plus utile de Git : lance-la sans modération.
#  └─ PIÈGE : aucun — `git status` ne modifie rien, c'est une simple lecture.

 git add .
#  └─ QUOI : ajoute à l'index (zone de préparation) TOUTES les modifications du
#            dossier courant et de ses sous-dossiers — le `.` = "ici et en dessous".
#  └─ POURQUOI : tu déclares à Git ce qui fera partie du prochain commit. "add" ne
#               sauvegarde pas encore : il prépare la photo.
#  └─ PIÈGE : le `.` ratisse large et peut embarquer des fichiers non désirés
#            (gros CSV, secrets, dossiers temporaires). Mets un fichier `.gitignore`
#            en place pour les exclure. Pour cibler : `git add fichier1 fichier2`.

 git commit -m "message clair"
#  └─ QUOI : fige tout ce qui est dans l'index sous forme d'un commit (un point
#            d'historique immuable, avec son empreinte, ton nom et la date). Le `-m`
#            donne le message directement en ligne, sans ouvrir l'éditeur.
#  └─ POURQUOI : c'est l'unité de sauvegarde de Git. Un bon message décrit le
#               POURQUOI du changement, pas seulement le quoi (ex. "Corrige le
#               doublon de lignes dans le nettoyage CSV").
#  └─ PIÈGE : seul ce qui a été `git add`-é est inclus. Une modif oubliée à l'étape
#            précédente ne sera PAS dans le commit. (Vérifie avec `git status`.)

 git push -u origin prenom/AAAA-MM-JJ
#  └─ QUOI : envoie tes commits locaux vers le remote `origin`, sur une branche
#            distante du même nom. Le `-u` (= --set-upstream) établit le LIEN de
#            suivi entre ta branche locale et sa jumelle distante.
#  └─ POURQUOI : sauvegarde ton travail sur GitHub (utile même seul) et le rend
#               visible au binôme. Grâce au `-u`, les prochaines fois un simple
#               `git push` / `git pull` suffira, sans répéter le nom.
#  └─ PIÈGE : le `-u … <nom>` n'est nécessaire QUE pour le tout premier push d'une
#            branche neuve. Adapte `prenom/AAAA-MM-JJ` à ta vraie branche.


# ════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 4 — Remonter sa branche dans la feature (merge only)
# ════════════════════════════════════════════════════════════════════════════

 git checkout feature/clean-data
#  └─ QUOI : rebascule sur la branche feature : c'est ELLE qui va RECEVOIR ta fusion.
#  └─ POURQUOI : git merge se fait toujours "depuis la branche d'accueil". Pour
#               fusionner ta branche DANS la feature, il faut d'abord être SUR la feature.
#  └─ PIÈGE : erreur classique = fusionner dans le mauvais sens. On se place sur la
#            destination (feature), pas sur la source (ta branche datée).

 git pull
#  └─ QUOI : remet la feature locale à jour avec le remote (le binôme a pu fusionner
#            son travail entre-temps).
#  └─ POURQUOI : on fusionne dans une feature à jour, pour limiter les divergences et
#               donc la taille des conflits éventuels.
#  └─ PIÈGE : si un conflit surgit ici, résous-le avant de continuer (voir étape merge).

 git merge --no-ff prenom/AAAA-MM-JJ
#  └─ QUOI : intègre les commits de ta branche datée DANS la feature courante.
#            `--no-ff` (no fast-forward) FORCE la création d'un commit de fusion
#            dédié, même quand un simple avancement de pointeur aurait suffi.
#  └─ POURQUOI : ce commit de merge laisse une trace explicite et datée
#               ("ici, la branche d'Alice a été intégrée") → traçabilité du qui/quand,
#               essentielle à plusieurs. Les commits d'origine gardent leur identité :
#               rien n'est réécrit (toute la différence avec rebase).
#  └─ PIÈGE : si ton binôme et toi avez touché les mêmes lignes, Git s'arrête sur un
#            CONFLIT. Édite le fichier, retire les marqueurs <<<<<<< ======= >>>>>>>,
#            puis `git add <fichier>` et `git commit` pour finaliser la fusion.

 git push
#  └─ QUOI : publie la feature fusionnée (ton merge inclus) sur origin.
#  └─ POURQUOI : rendre l'intégration visible au binôme et la sauvegarder.
#  └─ PIÈGE : si le push est rejeté ("rejected / non-fast-forward"), c'est que le
#            remote a avancé : fais `git pull` (intègre), puis re-`git push`.


# ════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 5 — Tester la feature
# ════════════════════════════════════════════════════════════════════════════

 pytest        # ne passer à l'étape 6 que si c'est VERT
#  └─ QUOI : lance la suite de tests du projet (ici via pytest ; ça pourrait être
#            `python -m pytest`, `make test`, un script de validation de données…).
#  └─ POURQUOI : c'est le GARDE-FOU avant main. On ne fusionne en production que du
#               code dont les tests passent. En data engineering : vérifs de schéma,
#               de doublons, de qualité de données, etc.
#  └─ PIÈGE : si c'est ROUGE, on NE touche pas à main. On crée une nouvelle branche
#            datée pour corriger, on re-fusionne dans la feature, et on re-teste.


# ════════════════════════════════════════════════════════════════════════════
#  ÉTAPE 6 — Remonter la feature dans main
# ════════════════════════════════════════════════════════════════════════════

 git checkout main
#  └─ QUOI : bascule sur main, la branche de référence qui va recevoir la feature.
#  └─ POURQUOI : main est la destination finale ; on doit être dessus pour y fusionner.
#  └─ PIÈGE : main ne doit recevoir QUE du testé. Si tu n'es pas sûr que l'étape 5
#            est verte, n'avance pas.

 git pull
#  └─ QUOI : synchronise main local avec origin/main (d'autres ont pu y livrer).
#  └─ POURQUOI : éviter un push rejeté et fusionner sur une main à jour.
#  └─ PIÈGE : idem qu'avant — dossier propre obligatoire avant un pull.

 git merge --no-ff feature/clean-data
#  └─ QUOI : intègre toute la feature (Alice + Bob réunis et testés) dans main, avec
#            un commit de fusion dédié grâce à `--no-ff`.
#  └─ POURQUOI : on garde un point d'historique clair "la feature clean-data est
#               passée en production le … ". Lisible pour une revue ou une soutenance.
#  └─ PIÈGE : un conflit reste possible si main a divergé. Même procédure de
#            résolution : éditer, `git add`, `git commit`.

 git push
#  └─ QUOI : publie main mise à jour sur origin → c'est désormais la version officielle.
#  └─ POURQUOI : livrer. Le travail du binôme est intégré, testé et en ligne.
#  └─ PIÈGE : si rejeté, `git pull` puis re-`git push`. Ensuite, tu peux supprimer
#            les branches devenues inutiles (git branch -d …, git push origin --delete …).


# ════════════════════════════════════════════════════════════════════════════
#  BONUS — Visualiser l'historique à tout moment
# ════════════════════════════════════════════════════════════════════════════

 git log --graph --oneline --all
#  └─ QUOI : affiche l'historique des commits sous forme de graphe.
#       --graph   : dessine les branchements et fusions en ASCII (le côté gauche).
#       --oneline : un commit = une ligne (empreinte courte + message). Lisible.
#       --all     : montre TOUTES les branches, pas seulement la courante — idéal pour
#                   voir où en sont ta branche, celle du binôme, la feature et main.
#  └─ POURQUOI : comprendre visuellement l'ordre et la structure des commits, repérer
#               les points de fusion (commits à deux parents) et qui est en avance/retard.
#  └─ ASTUCE : ajoute `--topo-order` pour regrouper les commits par branche plutôt que
#             par date, ou `-10` pour limiter aux 10 derniers. `q` pour quitter l'affichage.
```