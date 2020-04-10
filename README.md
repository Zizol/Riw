# Riw
Projet RIW pour l'ecole

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

Le SRI sera évalué avec des requêtes types.

Les données sont la collection CS276

## Comment naviguer ce repo et utiliser le script

### Script de recherche et d'indexation

Les librairies tierces sont dans `requirements.txt`:

* `pip install -r requirements.txt`

Le script se trouve dans `sample.py`. Pour l'utiliser :

* `python sample.py indexation`

	* Lance le module d'indexation
	
	    * Comme il y a beaucoup de documents, il est possible de n'indexer qu'une partie de ceux ci : 
	    ajouter `--doc_type html` ou `--doc_type php` n'indexe que les fichiers .html ou .php. 
	    
	    * Par défaut seuls les fichiers html sont indexés, si on veut tous les indexer, `--doc_type all`
	
	* Crée les fichiers d'index dans le dossier `Indexes/`
	
Comme cette étape prend du temps, il est suggéré de la lancer tôt, puis de regarder le notebook pour passer le temps

* `python sample.py recherche --query /path/to/query.4`

	* Lance le module de recherche

	* Nécessite une query dans un fichier texte pour fonctionner

	* Optionnellement le modèle de recherche est paramétrable : `--model_type [boolean, vectorial]`
	
	* Par défaut le modèle est binaire
	
	    * De plus si le modèle est vectoriel, il faut choisir la stratégie de poids : `--weigth_query ["binary", "frequency"] --weigth_doc ["binary", "frequency", "tf_idf_normalize", "tf_idf_logarithmic", "tf_idf_logarithmic_normalize"]`
	    
	    * Par défaut les poids sont binaire et binaire

	* Sauvegarde les résultats et leurs métriques dans `Output/`

### Justifications techniques

Un notebook retraçant les différentes étapes du script de façon visuelle est disponible. 
Il affiche sous forme de graphes et de métriques les différentes données qui ont contribué aux choix dans les modèles.
	