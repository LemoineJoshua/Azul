Implémentations:

Pour la phase 3 nous avons décidé d'implémenter une IA.
L'IA est fonctionnelle et nous avons corrigés tous lesb ugs que nous avons rencontrés durant notre phase de test.
L'IA est de difficulté moyenne voir avancée, elle gagne souvent et il faut prendre le temps de reflechir à chaque coup pour la battre.
Des tests on été effectués sur les machines de L'IUT et le programme est fonctionnel sur ces dernières.

L'organisation du programme:

le programme utilise 5 fichiers .py et .txt qui sont :
    - le main (on exécute le programme ici)
    - Un fichier “fonctions” dans lequel on implémente toutes les fonctions qui vont s'appeler soit entre elles ou dans le main. Triées par actions, par exemple les fonctions graphiques vont se trouver les unes à la suite des autre etc.
    - Un fichier “variables” dans lequel on initie toutes les variables pour qu'elles soient plus facile d'accès et pour une meilleur visibilité.
    - le module upemtk utilisé pour les fonctions graphiques ainsi que la récupération des coordonnées du clic de la souris.
    - Un fichier 'selec_mur' qui contient les différents murs de jeux

Choix technique:

L'IA se base sur 5 fonctions:
    -choix_bot qui renvoie des coordonnés
    -possibilite_IA qui indique dans quelles fabriques l'IA peut piocher
    -possibilite_IA_reste qui indique dans quelle partie du reste L'IA peut piocher
    -coordonnee_motif_IA qui indique le meilleur coup possible avec un ensemble de tuile donné
    -meilleur_coup qui compare tout les résultats de coordonnee_motif_IA avec tout les ensemble de tuiles récupérables dans les fabrique et le reste

Problème:

Certain ralentissement sont provoqués par la superposition de plusieur formes du modules upemtk, ils peuvent être réglés grace à la fonction efface_tout
Nous avons donc implémenté cette fonction a la fin de chaque manche pour avoir un équilibre entre ne jamais reset le plateau de jeu et le reset à chaque action.