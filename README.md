# Light_Ninja
Projet LU1IN021
Il y a 8 éléments dans le fichier de notre projet.
	- Le programme app.py contient le code python du serveur flask, le code gérant les URL, les chemins et des données.
	- Le programme operations_base contient les fonctions de modifications d'ajout et d'extraction de données de la base de données.
	- Le programme led_setup contient la classe et les fonctions qui permettent d'allumer les rgb.
	- Le programme jeux contient le code des jeux ainsi que les fonctions permettent de faire fonctionner les boutons.
	- Le programme init_base est là où les tables sont créées, où elles peuvent être vidées.
	- Le fichier data contient la base de données avec les données utilisateurs et les données de chaque partie pour chaque jeu.
	- Le fichier static contient le css, le JavaScript ainsi que les images de notre site.
	- Le fichier templates contient le HTML de notre site. 
	- Le fichier venv contient le serveur de notre site.


Pour démarrer le projet depuis le Raspberry py, il faut:
	Aller dans le terminal du Raspberry py.
	Entrer la commande 'cd Documents', puis 'source venv/bin/activate', puis 'python app.py'.
	Ouvrir un navigateur et entrer le lien 'http://127.0.0.1:5000'.


Pour démarrer le projet depuis un ordinateur, il faut :
	Aller dans le terminal de l'ordinateur.
	Aller dans le répertoire du projet, puis entrer la commande 'python app.py.
	Ouvrir un navigateur et entrer le lien 'http://127.0.0.1:5000'.
