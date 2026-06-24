# 02: Note à propos `switch` et `checkout`

Dans le tuto on utilise `git checkout` pour changer de branche. Mais vous verrez parfois `git switch` à la place : voici la différence, vite fait.


## `checkout`, le vieux couteau suisse

`git checkout` fait **plein de choses différentes** (c'est pratique, mais ça prête à confusion) :

```bash
git checkout new_branch # changer de branche
git checkout -b new_branch # créer une branche ET aller dessus
git checkout master # retourner sur master
git checkout -- file_1.txt # ☢️☢️ annuler les modifs pas encore enregistrées d'un fichier
```

Le problème : la même commande sert à la fois à se balader entre les branches **et** à toucher aux fichiers. On peut se tromper sans faire exprès.


## `switch` (et `restore`), les versions claires

Depuis Git 2.23, le couteau suisse a été coupé en deux commandes plus lisibles (c'est faire une chose à la fois) :

- `git switch` → **juste** pour les branches (changer, créer)
- `git restore` → **juste** pour les fichiers (annuler des modifs)


## Les équivalences à retenir

| Ce qu'on veut faire | Ancienne façon (`checkout`) | Nouvelle façon |
| --- | --- | --- |
| Changer de branche | `git checkout new_branch` | `git switch new_branch` |
| Créer une branche et aller dessus | `git checkout -b new_branch` | `git switch -c new_branch` |
| Retourner sur master | `git checkout master` | `git switch master` |
| Annuler les modifs d'un fichier | `git checkout -- file_1.txt` | `git restore file_1.txt` |

> Le `-c` de `git switch -c` veut dire "create" (créer), comme le `-b` de `checkout -b`.


## Lequel utiliser ?

- Les deux marchent, vous ne casserez rien.
- `switch` / `restore` sont plus clairs : on recommande de prendre cette habitude.
- Mais `checkout` est encore **partout** dans les tutos (dont le nôtre), donc il faut savoir le lire. **Cette commande est beaucoup plus utilisée que** `switch` et `restore`.

En résumé : dans nos exemples on garde `checkout` pour rester cohérent, mais si vous tapez `git switch`, c'est tout aussi bien (et même un peu mieux).