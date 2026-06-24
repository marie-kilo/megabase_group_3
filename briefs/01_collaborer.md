# 01: Travailler à plusieurs 

> Cette partie prolonge le tutoriel `git_step_by_step`. On part du principe que vous
> maîtrisez déjà la routine **status → add → commit → push**, et on
> ajoute une seule chose : **une deuxième personne**.

Scénario : **Alice** et **Bob** codent ensemble (live coding) sur le même dépôt.
**On va mettre en place un vrai workflow d'équipe**, du type de ceux utilisés en data
engineering, en n'utilisant **que `merge`** (jamais `rebase` — on en parle plus bas,
mais on ne s'en sert pas).

---

## Le workflow cible

L'objectif est une chaîne à trois niveaux :

```
   branche individuelle datée   ─merge─►   branche feature   ─(tests OK)─►   main
   (alice/2026-06-23)                      (feature/clean-data)              (production)
   (bob/2026-06-23)
```

Pourquoi cette structure plutôt que « tout le monde pousse sur `main` » ?

- **La branche individuelle datée** isole le travail de chacun. Personne ne casse le
  code de l'autre en direct. La date dans le nom donne un historique lisible de
  « qui a travaillé quoi, quand ».
- **La branche feature** est le point de rassemblement du binôme. C'est là qu'on
  réunit le travail d'Alice et de Bob pour la fonctionnalité en cours.
- **Les tests** se lancent sur la feature, une fois tout réuni. On ne pollue jamais
  `main` avec du code non testé.
- **`main`** ne reçoit que du code testé et qui fonctionne. C'est la branche de
  référence.

La règle d'or : **on remonte la chaîne, jamais l'inverse.** On code en bas, on
fusionne vers le haut, et `main` reste propre.

---

## 0. Préparer la collaboration sur GitHub

Le dépôt appartient à une personne (disons Alice). Pour que Bob puisse pousser
dessus, Alice l'ajoute comme **collaborateur** :

> Sur GitHub : onglet **Settings** du dépôt → **Collaborators** → **Add people** →
> entrer le pseudo de Bob. Bob reçoit une invitation par mail et l'accepte.

Ensuite, **chacun de son côté** clone le dépôt :

```bash
 git clone https://github.com/Alice/git_step_by_step.git
 cd git_step_by_step/
```

Une personne (Alice) crée la branche feature et la pousse pour que Bob la voie :

```bash
 git checkout main
 git checkout -b feature/clean-data   # créer la branche feature à partir de main
 git push -u origin feature/clean-data  # -u = la "brancher" sur le remote (première fois)
```

Bob la récupère :

```bash
 git fetch origin
 git checkout feature/clean-data   # Git crée la branche locale qui suit le remote
```

---

## 1. Créer sa branche individuelle datée

**Convention de nommage :** `prénom/AAAA-MM-JJ` (on peut ajouter un sujet :
`alice/2026-06-23-nettoyage-csv`). La date permet de retrouver et trier le travail.

Chacun crée **sa** branche **à partir de la feature** :

```bash
 git checkout feature/clean-data
 git pull                         # toujours partir de la dernière version
 git checkout -b alice/2026-06-23 # Alice (Bob fait : git checkout -b bob/2026-06-23)
 git branch                       # vérifier sur quelle branche on est (l'étoile *)
```

---

## 2. Coder et committer sur sa branche

Là, c'est exactement la routine de la Partie 1, mais sur **sa propre branche**.
Alice modifie `file_1.txt`, Bob crée `file_2.txt` :

```bash
 # côté Alice
 open file_1.txt                  # écrire quelque chose, enregistrer
 git status
 git add file_1.txt
 git commit -m "Alice : ajout d'une ligne dans file_1.txt"
```

```bash
 # côté Bob
 touch file_2.txt
 open file_2.txt                  # écrire quelque chose, enregistrer
 git status
 git add file_2.txt
 git commit -m "Bob : création de file_2.txt"
```

Tant qu'on est sur sa branche individuelle, **on commit autant qu'on veut** sans
gêner l'autre. On peut aussi pousser sa branche pour la sauvegarder sur GitHub :

```bash
 git push -u origin alice/2026-06-23
```

---

## 3. Fusionner sa branche dans la branche feature (merge uniquement)

Quand votre morceau est prêt, vous le remontez **dans la feature**. On se place sur
la feature, on récupère les dernières nouveautés, puis on fusionne sa branche :

```bash
 git checkout feature/clean-data
 git pull                                  # récupérer ce que l'autre a déjà fusionné
 git merge --no-ff alice/2026-06-23        # fusionner SA branche DANS la feature
 git push                                  # publier la feature mise à jour
```

Pourquoi **`--no-ff`** ? (`no fast-forward`)

- Sans `--no-ff`, si la feature n'a pas bougé, Git fait un **fast-forward** : il
  avance simplement le pointeur, **sans créer de commit de fusion**. L'historique
  devient plat et on perd la trace « ici, la branche d'Alice a été intégrée ».
- Avec `--no-ff`, Git crée **toujours un commit de merge**. On garde une trace
  explicite et datée de chaque intégration. Pour un travail à plusieurs (et pour une
  soutenance / un suivi pédagogique), cette traçabilité est précieuse.

La **deuxième** personne à fusionner (Bob, après Alice) n'aura de toute façon pas de
fast-forward possible : les deux historiques ont divergé, Git **doit** fabriquer un
commit de merge. C'est le moment où un **conflit** peut apparaître (voir § 5).

---

## 4. Comprendre l'ordre des commits

C'est le point clé. Déroulons un exemple précis avec les horaires des commits.

Au départ, `feature` et `main` sont au commit **C0**. Alice et Bob partent tous les
deux de C0 :

```
          A1(10:00) ── A2(10:30)          ← alice/2026-06-23
         /
C0 (09:00)                                 ← feature/clean-data, main
         \
          B1(10:15) ── B2(10:45)          ← bob/2026-06-23
```

**Alice fusionne en premier** (`git merge --no-ff alice/2026-06-23`). Git crée le
commit de merge **M_A** :

```
          A1 ── A2
         /        \
C0 ───────────────  M_A                    ← feature (Alice intégrée)
         \
          B1 ── B2                         ← bob/2026-06-23 (pas encore fusionné)
```

**Bob fusionne ensuite** (après `git pull` pour récupérer M_A, puis
`git merge --no-ff bob/2026-06-23`). Git crée le commit de merge **M_B**, qui a
**deux parents** : M_A (la feature) et B2 (la branche de Bob) :

```
          A1 ── A2
         /        \
C0 ───────────────  M_A ───────────  M_B   ← feature (Alice + Bob intégrés)
         \                          /
          B1 ──────────────────── B2
```

### Ce que montre `git log`

Visualisez la structure avec :

```bash
 git log --graph --oneline --all
```

Maintenant, l'ordre. Par défaut, `git log` liste les commits **du plus récent au
plus ancien, par date**. Les commits d'Alice et de Bob **s'entremêlent** donc selon
l'heure :

```
M_B   (merge, ~10:55)
M_A   (merge, ~10:50)
B2    (10:45)
A2    (10:30)
B1    (10:15)
A1    (10:00)
C0    (09:00)
```

C'est normal et ça peut surprendre : `B2` apparaît **avant** `A2` parce qu'il a été
committé plus tard, même s'il vient d'une autre branche. Pour voir les commits
**regroupés par branche** plutôt que par horloge :

```bash
 git log --graph --oneline --topo-order
```

### Le point essentiel à retenir

Avec `merge`, **chaque commit garde son identité d'origine** : son auteur, son
message, sa date, son empreinte (hash). Rien n'est réécrit. L'historique est un
**enregistrement fidèle** de qui a fait quoi et quand, et les commits de merge
(M_A, M_B) marquent les points d'intégration. C'est exactement ce qui distingue
`merge` de `rebase` (voir l'avant-dernière section).

---

## 5. Gérer un conflit de merge

Un conflit arrive quand Alice **et** Bob ont modifié **les mêmes lignes du même
fichier** (typiquement `file_1.txt`). Au moment du `git merge`, Git ne sait pas
quelle version garder et s'arrête :

```bash
 git merge --no-ff bob/2026-06-23
 # Auto-merging file_1.txt
 # CONFLICT (content): Merge conflict in file_1.txt
 # Automatic merge failed; fix conflicts and then commit the result.
```

Ouvrez le fichier : Git y a inséré des marqueurs :

```
<<<<<<< HEAD
ligne écrite côté feature (Alice)
=======
ligne écrite par Bob
>>>>>>> bob/2026-06-23
```

Vous **choisissez à la main** ce qu'il faut garder (l'une, l'autre, ou les deux),
**vous supprimez les marqueurs** `<<<<<<<`, `=======`, `>>>>>>>`, puis :

```bash
 git add file_1.txt          # dire à Git que le conflit est résolu
 git commit                  # finaliser le commit de merge (message déjà pré-rempli)
 git push
```

Conseil pratique en live coding : **fusionnez souvent et à deux devant l'écran**.
Plus on attend, plus les branches divergent, plus les conflits sont gros.

---

## 6. Tester la branche feature

C'est l'étape « data engineer » : **on ne fusionne dans `main` que si les tests
passent**. Sur la feature, une fois Alice et Bob intégrés :

```bash
 git checkout feature/clean-data
 git pull
 pytest                       # ou : python -m pytest, make test, un script de validation…
```

Par exemple, si votre feature transforme des données, vous pouvez avoir un
`test_transform.py` qui vérifie le résultat :

```python
# test_transform.py
from transform import clean

def test_clean_supprime_les_doublons():
    assert clean([1, 1, 2]) == [1, 2]
```

```bash
 pytest -q
 # ......                     [100%]
 # 2 passed in 0.04s
```

- **Tests verts** → on passe à l'étape 7.
- **Tests rouges** → on **reste sur la feature**, on crée une nouvelle branche
  individuelle datée pour corriger, et on re-fusionne. `main` n'est jamais touchée.

---

## 7. Fusionner la branche feature dans main

Dernière étape, une seule fois que tout est testé :

```bash
 git checkout main
 git pull
 git merge --no-ff feature/clean-data   # intégrer la feature complète dans main
 git push
```

À nouveau `--no-ff` pour garder un commit de merge clair : « la feature
*clean-data* a été intégrée à `main` à telle date ». On peut ensuite supprimer les
branches devenues inutiles :

```bash
 git branch -d alice/2026-06-23 bob/2026-06-23   # local
 git push origin --delete alice/2026-06-23        # remote (si poussées)
```

---

## Et le rebase ? (on en parle, on ne l'utilise pas)

Vous entendrez forcément parler de `git rebase`. Voici ce que c'est, et **pourquoi on
ne l'utilise pas dans ce workflow**.

**Ce que fait `rebase` :** au lieu de relier deux historiques par un commit de
merge, `rebase` **rejoue** vos commits **par-dessus** une autre base, comme s'ils
avaient été écrits après. L'historique devient **linéaire**, sans commit de fusion :

```
   merge (ce qu'on fait)              rebase (ce qu'on évite)

   A1 ── A2                           C0 ── B1 ── B2 ── A1' ── A2'
  /        \                          (ligne droite, mais A1/A2 sont RÉÉCRITS
 C0 ──────  M ── …                     → nouveaux hashs : A1', A2')
  \        /
   B1 ── B2
```

**Pourquoi c'est tentant :** un historique tout droit est plus « propre » à lire,
sans les embranchements des commits de merge.

**Pourquoi on l'évite ici :**

1. **`rebase` réécrit l'historique.** Les commits changent d'empreinte (A1 → A1').
   La **règle d'or du rebase** : *ne jamais rebaser une branche déjà partagée /
   poussée que quelqu'un d'autre utilise.* En live coding à deux sur les mêmes
   branches, c'est précisément le cas à éviter — on risque de désynchroniser le
   binôme et de provoquer des « divergences » très pénibles à réparer.
2. **On perd la trace réelle.** Notre objectif (branche datée → feature → test →
   main) repose sur une **traçabilité** : qui a fusionné quoi, quand. Les commits de
   merge `--no-ff` racontent cette histoire. Le rebase, lui, l'efface au profit d'une
   ligne droite reconstruite.
3. **Pour apprendre, `merge` est plus sûr et plus transparent :** rien n'est réécrit,
   chaque commit garde sa date et son auteur (cf. § 4).

> À titre culturel : il existe aussi `git pull --rebase`, et le rebase interactif
> `git rebase -i` pour nettoyer ses propres commits **avant** de les partager. Ce
> sont des outils utiles plus tard, sur **vos** branches non partagées. Dans ce
> tutoriel : **merge uniquement.**

---

## Aide-mémoire — routine à plusieurs

```bash
# 1. Partir de la feature à jour
 git checkout feature/clean-data
 git pull

# 2. Créer sa branche individuelle datée
 git checkout -b prenom/AAAA-MM-JJ

# 3. Coder, puis sauvegarder
 git status
 git add .
 git commit -m "message clair"
 git push -u origin prenom/AAAA-MM-JJ

# 4. Remonter dans la feature (merge only)
 git checkout feature/clean-data
 git pull
 git merge --no-ff prenom/AAAA-MM-JJ
 git push

# 5. Tester la feature
 pytest        # ne passer à l'étape 6 que si c'est VERT

# 6. Remonter dans main
 git checkout main
 git pull
 git merge --no-ff feature/clean-data
 git push

# Visualiser l'historique à tout moment
 git log --graph --oneline --all
```