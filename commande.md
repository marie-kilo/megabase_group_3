## Les commandes git à faire (dans un terminal gitbash):

- git init

- creation du repo pour le groupe dans github avec une visibilité en private (BP)

- git clone du repo du gestionnaire

- git add . ou git add nom du fichier  pour ajouter un ou des fichiers

- git commit -m "message du commit"

- git push pour pousser son code vers le repo distant

- git status permet de voir tous les changements

- git branch permet de lister les branches rattacher au repo

- git checkout -b ma-branche permet de créer sa branche et de basculer dessus

- git push -u origin ma-branche permet de push et de rattacher le local au distant

- git pull permet de recuperer les changements d'autres

- git merge permet de fusionner les changements entre les differentes branches

- git log permet de voir l'historique des commits et des changements

- git diff permet de voir les differences de changements


## Les commandes pyenv (dans un terminal powershell) :

- pyenv install 3.14.5

- pyenv local 3.14.5

- python -m venv .env

- .\.env\Scripts\Activate.ps1 ou .env\Scripts\activate

- pip install -r requirements.txt permet d'installer toutes les libraisries necessaires et les dépendances

- Remove-Item -Recurse -Force .env  pour surpprimer .env si ça bloque

* template par projet :

 - python -m venv env
 - .\env\Scripts\Activate.ps1
 - pip install -r requirements.txt
 - python -m ipykernel install --user --name nom_du_projet --display-name "Python (nom_du_projet)"

###

