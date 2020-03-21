# Riw
Projet RIW pour l'ecole

Ce notebook contient toute ma vie. Prenez en soin.

Non plus sérieusement c'est le projet de RIW, il va se construire de la facon suivante :

## Livrable

* Mettre en place un SRI avec des modules permettant de faire des recherches d'infos sur la collection CS276, c'est à dire au moins :

  * Un module d'indexation

  * Un module de recherche

  * De la compression d'index

    * En bonus des modèles de langue

    * Des approches de ranking récentes

* Un notebook contenant les justifications statistiques et explications des choix techniques

* Un ReadMe permettant de faire facilement tourner le code si on le découvre

## Démarche

Pour le moment les td de cours permettent de mettre en place rapidement ces modules pourvus qu'ils aient été faits (ce qui est le cas).

Le SRI sera évalué avec des requêtes types.

Les données sont la collection CS276

## Comment naviguer ce repo et utiliser le script

### Script de recherche et d'indexation

Les librairies tierces sont dans `requirements.txt`:

* `pip install -r requirements.txt`

Le script se trouve dans `sample.py`. Pour l'utiliser :

* `python sample.py indexation`

	* Lance le module d'indexation
	
	* Crée les fichiers d'index dans le dossier `Indexes/`

* `python sample.py recherche --query zedezd.zed`

	* Lance le module de recherche

	* Nécessite une query dans un fichier texte pour fonctionner : `--query zedezd.zed`

	* Optionnellement le modèle de recherche est paramétrable : `--model_type [boolean, vectorial]`

	* Sauvegarde les résultats et leurs métriques dans `Output/`

### Justifications techniques

Un notebook retraçant les différentes étapes du script de façon visuelle est disponible. Il affiche sous forme de graphes et de métriques les différentes données qui ont contribué au choix dans les modèles.
	