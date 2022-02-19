from variable import *
from fonctions import *
from upemtk import *
from time import sleep


if __name__ == '__main__':

	cree_fenetre(largeurFenetre,hauteurFenetre)
	
	while condition_ouverture:
		
		#initialisation
		rectangle(0,0,largeurFenetre,hauteurFenetre,couleur='white',remplissage='white')
		Choix_nombre_joueurs() #visuel de l'ecran de selection
		paquet = list(paquet_init)
		mur_visu=Mur_visuel()
		start=True
		#lst_possibilite_IA=possibilite_IA(nb_joueurs) (utile pour l'IA si on veut l'amelorier par la suite)
		nb_joueurs,jouer_bot,plancher,mur_id,score,condition_ouverture,nb_joueurs,jouer_bot,paquet,score,plancher,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu,possibilite_IA_lst=selection_nombre_de_joueur(start,jouer_bot,condition_ouverture,nb_joueurs,paquet,score,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu)
			
		while condition_ouverture:
			
			#remplissage des fabriques
			if fab_vide(toutes_fabriques,nb_fabrique) and reste_vide(total_reste): #si tout les endroits ou on peux choisir des tuiles sont vides
				condition_ouverture,tuile_reste,toutes_fabriques,mur_id,score,fabrique_vide,compt,ligne_motifs,plancher,plancher1,nb_fabrique,premier_reste,possibilite_IA_lst = remplir_fabrique_finir_jeu(ligne_motifs,mur_visu,mur_id,score,plancher,condition_ouverture,nb_joueurs,plancher1,toutes_fabriques,compt,nb_fabrique,paquet)
				if condition_ouverture==False:
					break

			#recuperations des coordonnées (dépend de qui joue)
			if jouer_bot and tour_bot:
				print('tour du bot :\n------------------------------------------------------------------------')
				if action_IA==0:
					meilleur_choix=meilleur_coup(total_reste,toutes_fabriques,len(toutes_fabriques),possibilite_IA_lst,ligne_motifs,mur_visu,mur_id)
				
				x,y,passage_joueur,action_IA = choix_bot(action_IA,meilleur_choix)
			else:
				x,y,_ = attente_clic()
				print('tour du Joueur :\n------------------------------------------------------------------------')
				print('le joueur courant est : ',joueur)



			#affichage des motifs
			if ligne_motifs: #Si il y a quelquechose dans les motif des joueurs on l'affiche
				grille_joueur(joueur,ligne_motifs)
				visu_plancher(plancher,joueur)

			#selection des tuiles
			lst_reste,colonne_a_vider,select_tuile_verif,plancher1,lst_carre,fabrique_selection,choix_dans_reste = selection_tuiles_fonctions(x,y,toutes_fabriques,select_tuile_verif,lst_carre,colonne_a_vider,plancher1,choix_dans_reste,lst_reste,fabrique_selection,total_reste,nb_fabrique)
			print('les carrés sélectionné sont : ',lst_carre,'\n')
			print('la fabrique sélectionnée est : ',fabrique_selection,'\n')
			print('le joueur a choisi dans le reste : ',choix_dans_reste,'\n')

			#selection des lignes
			ligne_recup_verif,plancher1,select_row = selection_lignes_fonction(x,y,joueur,plancher,ligne_recup_verif,ligne_motifs,lst_carre,plancher1,select_row)
			print('la ligne sélectionnée est : ',select_row,'\n')


			#quand on appuies sur le bouton jouer
			if (largeurFenetre*3/5>x>largeurFenetre*2/5) and (hauteurFenetre*5/6<y<hauteurFenetre): #quand on clique sur le bouton 'jouer'
				fabrique_vide,select_tuile_verif,plancher,total_reste,joueur,tour_bot,compt,toutes_fabriques,plancher1,premier_reste,ligne_motifs,choix_dans_reste,possibilite_IA_lst = selections_tuiles_fabriques_restes(select_tuile_verif,ligne_recup_verif,select_row,joueur,ligne_motifs,total_reste,lst_reste,plancher,premier_reste,plancher1,fabrique_selection,toutes_fabriques,colonne_a_vider,passage_joueur,jouer_bot,tour_bot,compt,fabrique_vide,lst_carre,nb_joueurs,choix_dans_reste,mur_visu,mur_id,possibilite_IA_lst)
				print('les planchers sont : ', plancher,'\n')
				print('les fabriques sont : ', toutes_fabriques,'\n')
				sauvegarde(nb_joueurs,jouer_bot,paquet,score,plancher,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu)

			if redemarrer(x,y):
				efface_tout()
				break

			if  not fermeture(x,y):   
				condition_ouverture = False 
				break

	ferme_fenetre()