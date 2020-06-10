# Projet-8 : Créez une plateforme pour amateurs de Nutella
----------------------------------------------------------

# 1 Informations générales
--------------------------
Ce projet est le 8ème projet de ma formation de développeur d'application en python auprès de l'établissement formateur OpenClassrooms.

## 1.1 Description du projet
-----------------------------
Le but du projet est de créer une application web qui permettrait aux utilisateurs de se créer un compte (et de s'y connecter), de pouvoir rechercher des produits à substituer ainsi qu'enregistrer des favoris qu'ils pourront consulter ultérieurement sur une autre page du site.
  
## 1.2 Description du parcours utilisateur
-------------------------------------------
L'utilisateur entre l'url de la page web correspondante au projet. Il arrive alors sur la page web d'accueil. Tant que celui-ci n'est pas connecté à un compte utilisateur, ses actions sont limitées. S'il souhaite se connecter à un compte, il doit se rendre sur la page de login ou sur la page de création de compte s'il n'a pas encore de compte.
Lorsque celui-ci est connecté, il peut alors rechercher des aliments par mot-clef via une barre de recherche. En fonction des résultats de sa recherche, il peut essayer de trouver un substitut plus sain à l'aliment qu'il souhaite substituer. Il peut enregistrer des favoris lorsqu'il est satisfait du produit et du substitut qu'il a trouvé.

## 1.3 Fonctionnalités du projet
---------------------------------
- Affichage du champ de recherche dès la page d’accueil
- La recherche ne doit pas s’effectuer en AJAX
- Interface responsive
- Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de - passe pour le moment.

# 2 Prérequis pour l'utilisation du projet
-------------------------------------------

## 2.1 Langages utilisés
-------------------------
le langage de programmation utilisé dans ce projet est python.
Les langages pour la partie "web" sont le HTML, le CSS et le javascript   
Lien pour télécharger python : https://www.python.org/downloads/  
version de python lors du développement : 3.8
Le projet a été développé avec le framework python 'Django'.
Lien vers la documentation Django : https://docs.djangoproject.com/en/3.0/


## 2.2 librairies utilisées:
-----------------------------
Vous pouvez retrouver l'ensemble des librairies utilisées pour ce projet dans le
fichier requirements.txt et tout installer directement via ce fichier grâce à une
commande pip. 
  
# 3 Structure du projet
-------------------------
Il est à noter que le code associé au projet respecte la PEP8  
Le projet est structuré comme un projet Django 'classique', c'est à dire avec plusieurs applications au sein du projet principal.
Les différentes applications sont les suivantes :
- favorites : contient tout le code lié à la gestion des favoris (ajout, récupération, etc...) et leurs affichages
- openfoodfacts : contient tout le code lié à la gestion de l'Appel à l'api du même nom + le traitement des données récupérées
- pages : contient tout le code lié aux pages statiques (mentions légales, ...)
- products : contient tout le code lié à la gestion des produits et catégories de produits
- profile : contient le code lié à l'affichage du profil utilisateur
- PureBeurre : application générée par django et contenant différents fichiers de configuration
- search : contient le code lié à la recherche de produits en base de données par rapport à des mots-clefs ou lorsqu'on recherche des substituts à des produits
- static : dossier contenant les fichiers statiques 'communs' aux applications
- templates : dossier contenant les templates "communs" aux applications
- users : application contenant le code lié à la gestion de l'utilisateur, sa connexion, sa création de compte,...

Chaque application a en général un fichier models.py contenant les modèles de l'application, un fichier views.py contenant les views de l'application, un fichier tests.py contenant les tests des fonctions et méthodes de l'application et dans certains cas, un fichier managers.py lorsque les modèles de l'application avaient besoin de managers. Chaque application (ou presque) a aussi un fichier templates et static pour tous les fichiers statiques et les templates qui sont propre à l'application. 
Les tests fonctionnels se situent dans l'application 'PureBeurre'.
Les commandes 'personnalisées' se situent dans des dossiers 'management/commands'.


# 4 Informations complémentaires
----------------------------------

## 4.1. Acteurs
----------------
développeur = Geoffrey Remacle

## 4.2. Utilisation d'API
--------------------------
Le projet utilise l'API 'OpenFoodfacts'
lien vers la documentation de l'API : https://wiki.openfoodfacts.org/API

## 4.3. Langue du code
-----------------------
les noms de classes, fonctions, variables, les commentaires, les docstrings,... sont écrits en anglais.

## 4.4 Déploiement
------------------
L'application est déployé avec Heroku
vous pouvez retrouvé l'application à cette adresse : https://geoffrey-remacle-purbeurre.herokuapp.com/

## 4.5 Utilisation de base de données
-------------------------------------
Le projet utilise une base de données PostGreSQL en production et SQLite en développement

## 4.6. Liens
--------------
Lien vers le repository github:  
https://github.com/GeoffreyRe/Project_8
  
Lien vers la page de la formation "Développeur d'Application python":  
https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python   


