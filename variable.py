################initialisation de variables############
joueur = 0
nb_joueurs = 0
action_IA=0
colonne_a_vider = None
plancher1 = None
lst_reste = None
fabrique_selection = None
select_row = None
ligne_motifs=None
lst_carre=None
mur_visu = None
mur_id = None
toutes_fabriques = None


###################conditions##############

condition_ouverture = True
start = True
choix_dans_reste=False
ligne_recup_verif = False
joueurs_choisis = True
fabrique_vide = True
selection_tuiles = False
selection_lignes = False
select_tuile_verif = False
select_ligne_verif = False
premier_reste = True
passage_joueur=True
tour_bot = False
jouer_bot = False

################tableaux###################

lst_couleur = ['red','blue','green','yellow','black']
paquet_init = ['red','blue','green','black','yellow']*20

total_reste = [[],[],[],[],[]]
score=[0]
compt=0
nb_fabrique=0



################taille de la fenetre et diverses coordonnées#####################

largeurFenetre=1000
hauteurFenetre=largeurFenetre//2

x_cercle = largeurFenetre/4   
y_cercle = hauteurFenetre/8	 

rayon=largeurFenetre//25
ancien_cote_carre = rayon/6 #une première mesure qu'on à utilisisé un peu partout mais qui ne correspond pas à la taille d'un coté de carré
cote_carre = ancien_cote_carre * 4 #la longueur du coté d'un carré
ecart_cercle= largeurFenetre/8

liste_coord_cercles_x = [largeurFenetre/2-largeurFenetre/6-rayon,  largeurFenetre/2-4*rayon, largeurFenetre/2, largeurFenetre/2+4*rayon, largeurFenetre/2+largeurFenetre/6+rayon, largeurFenetre/2-largeurFenetre/12, largeurFenetre/2+largeurFenetre/12,  largeurFenetre/2+rayon, largeurFenetre/2-rayon]
liste_coord_cercles_y = [y_cercle, y_cercle+ecart_cercle/1.5, y_cercle+ecart_cercle*1.25, y_cercle+ecart_cercle/1.5, y_cercle, y_cercle, y_cercle, y_cercle+ecart_cercle/1.5, y_cercle+ecart_cercle/1.5]

lst_select_carre1 = [-1.5,-4.5,-1.5,1.5]
lst_select_carre2 = [1.5,-1.5,1.5,4.5]
lst_select_carre3 = [1.5,-1.5,-4.5,-1.5]
lst_select_carre4 = [4.5,1.5,-1.5,1.5]

lst_select_carre1_visu = [-1.5,-4.5,1.5,4.5]
lst_select_carre2_visu = [1.5,-1.5,-1.5,1.5]
lst_select_carre3_visu = [1.5,-1.5,-1.5,1.5]
lst_select_carre4_visu = [4.5,1.5,-4.5,-1.5]