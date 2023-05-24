# Keyboard Master


## Cahier des charges
**Ne connaissant pas les consignes exactes, j'ai du adapter et improviser**
- [x] Système de détection de touches
- [x] Système multijoueur de versus online et matchmaking
- [x] Backend externe sur un serveur d'accès à la database
- [x] *Belle* interface tkinter
- [x] Solidement documenté

<br>



## Structure du projet

```
├── README.md             # Documentation du projet (vous êtes ico)
├── .editorconfig         # Configuration de l'éditeur de texte
├── .gitignore            # Fichier à ignorer pour git
├── app/                  # Directoire pour l'application Python 
|   ├── ico/              # Images pour la fenêtre Tkinter
|   ├── src/              # Scripts généraux/globaux Python
|   |   └── frames/       # Frames de la fenêtre Tkinter
|   ├── main.py           # Script d'entrée de l'application
|   └── requirements.txt  # Packages requis pour Python (pip)
└── server/               # Directoire pour la backend JavaScript
    ├── package.json      # Packages requis pour NodeJS (npm)
    ├── api/              # Fonctions serverless appelables par l'app Python
    └── src/              # Scripts additionnels JavaScript
        └── models/       # Models pour la database MongoDB Atlas
```

<br>


## Installation

### Prérequis
Pour lancer ce projet, vous aurez besoin de :

- Python (3.10 ou supérieur)
- pip (Package Installer for Python)


### Setup
*Selon votre version de python, il faudra utiliser* `py`*,* `python` *ou* `python3`*, et soit* `pip` *soit* `pip3`
1. Télécharger une release du projet disponible [ici]().
2. Installer les packages nécessaires avec la commande : `py -m pip install -r requirements.txt`
3. Lancer le fichier principal avec la commande : `py main.py`
