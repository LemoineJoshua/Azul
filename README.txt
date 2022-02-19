Bonjour à tous,
Ce programmes est un premier projet fait en BUT informatique, il consistait à simuler le jeu de plateau Azul.
Il n'est pas parfait mais nous en sommesplutôt fier et il est amusant à utiliser. Il est important de noter que 
la programmation orienté object nous était interdite c'est donc pour cela que vous n'en verrez pas ici, même si cela 
aurait été bien plus pratique j'en convient. Tout ce qui suit est une explication, la plus clair possible j'espère, du contenu du programme.
Bonne lecture!


L'organisation du programme:

le programme utilise 5 fichiers .py et .txt qui sont :
    - le main (on exécute le programme ici)
    - Un fichier “fonctions” dans lequel on implémente toutes les fonctions qui vont s'appeler soit entre elles ou dans le main. Triées par actions, par exemple les fonctions graphiques vont se trouver les unes à la suite des autre etc.
    - Un fichier “variables” dans lequel on initie toutes les variables pour qu'elles soient plus facile d'accès et pour une meilleur visibilité.
    - le module upemtk utilisé pour les fonctions graphiques ainsi que la récupération des coordonnées du clic de la souris.
    - Un fichier 'selec_mur' qui contient les différents murs de jeux

Choix technique:

La fenetre:
    -La fenetre est adaptable à l'envie en changeant la variable 'largeurfenetre' dans le fichier 'variable'
    -La fenetre est en deux temps: d'abord un menu qui permet de choisir le nombre de joueur/si on veut jouet contre une IA/si on veut charger une partie précédente. Ensuite il y a le plateau de jeu à proprement parler qui s'affiche quand un choix est effectué

Les .txt:
    -La sauvegarde est automatique et se fait à chaque fois qu'un joueur appuie sur le bouton 'jouer'
    -selec_mur est un fichier permettant de changer une partie du plateau, le programme fonctionne même si il est incorect ou inexistant. Cependant il faut suivre une certaine syntaxe pour le faire fonctionner ce qui n'est pas des plus ergonomique. Cependant l'utilisation de se dernier est expliqué dans le fichier lui même.

L'IA se base sur 5 fonctions:
    -choix_bot qui renvoie des coordonnés
    -possibilite_IA qui indique dans quelles fabriques l'IA peut piocher
    -possibilite_IA_reste qui indique dans quelle partie du reste L'IA peut piocher
    -coordonnee_motif_IA qui indique le meilleur coup possible avec un ensemble de tuile donné
    -meilleur_coup qui compare tout les résultats de coordonnee_motif_IA avec tout les ensemble de tuiles récupérables dans les fabrique et le reste

Problème principal:

Certain ralentissement sont provoqués par la superposition de plusieur formes du modules upemtk, ils peuvent être réglés grace à la fonction efface_tout
Nous avons donc implémenté cette fonction a la fin de chaque manche pour avoir un équilibre entre ne jamais reset le plateau de jeu et le reset à chaque action.
