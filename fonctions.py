from random import choice,randint
from variable import *
from upemtk import *
from math import sqrt
import os

######################################FONCTIONNEL###############################################

def paquets():
	'''fonction qui crée un paquet de 100 tuiles pour le début de la partie'''
	tuiles=['rouge','bleue','verte','noir','jaune']
	paquet=[]
	for i in range(100):
		paquet.append(choice(tuiles))
		
	return paquet
	
def fabriques(nb_joueur):
	'''Fonction qui va créer une matrice, chaque ligne correspondant à une fabrique'''
	fabriques=[]
	for i in range(1+nb_joueur*2): 
		fabriques.append([])
	
	return fabriques

def remplissage_fabriques(fabriques,paquet):
	'''fonction qui remplies les fabriques et piochant de le paquet'''
	lignes= len(fabriques)
	compt = lignes
	
	if len(paquet) >= lignes*4:
		for i in range(lignes): #pour chaque fabrique
			for j in range(4):	#on les remplies de 4 tuiles
				choix=choice(paquet) #on choisie une tuile
				fabriques[i].append(choix) #on l'ajoute à la fabrique
				paquet.remove(choix) #on l'enlève du paquet
	else:
		compt = 0
		for i in range(len(paquet)//4):
			for j in range(4):	#on les remplies de 4 tuiles
				choix=choice(paquet) #on choisie une tuile
				fabriques[i].append(choix) #on l'ajoute à la fabrique
				paquet.remove(choix) #on l'enlève du paquet
			compt +=1
	return fabriques,compt
	
def Mur_reel():
	'''fonction qui crée le tableau de jeu'''
	Mur=[] #ce tableau va devenir une matrice carré de coté 5
	lignes=['blue','red','yellow','green','black']
	for i in range(5):
		Mur.append(list(lignes)) #on ajoute la ligne
		lignes.insert(0,lignes[4]) #sur la ligne on déplace la dernière case en première position
		lignes.pop() #une fois déplacé on la supprime
		
	return Mur

def Mur_id_simple():
	'''Fonction qui crée un matrice de 5*5 remplie de 0'''
	Mur_id=[]
	for i in range(5):
		Mur_id.append([])
		for j in range(5):
			Mur_id[i].append(0)

	return Mur_id

def Mur_id_complet(nombre_joueur):
	'''Fonction qui crée une liste de Matrice 5*5 en fonction du nombre de joueur'''
	Mur_id_complet=[]
	for i in range(nombre_joueur):
		ajout=Mur_id_simple()
		Mur_id_complet.append(ajout)
	
	return Mur_id_complet

def lignes_motifs_init(nombre_joueur):

	'''créer les lignes que vont remplir les joueurs au cours de leur partie en fonction du nombre de joueurs.'''

	lignes = []
	for i in range(nombre_joueur):
		lignes.append([])
		for j in range(5):
			lignes[i].append([])
	return lignes

def remplissage_reste(lst_reste,lst_total_reste): 
	
	''' fonction permettant de remplir les colones de restes en fonction des couleurs de listes reste'''
	
	if lst_reste == None or lst_reste == []:
		return None
	for i in lst_reste:
		for j in range(5):
			if i == lst_couleur[j]:
				lst_total_reste[j].append(i)
	return lst_total_reste

def remplissage_ligne(ligne_motifs,tuiles,joueur,ligne,espace_disp):

	'''remplis la ligne sélectionner par le joueur de la liste de tuiles qu'il veut mettre'''

	for i in range(espace_disp):
		ligne_motifs[joueur][ligne].append(tuiles[0])
	return ligne_motifs

def remplissage_plancher(plancher1,lst_carre,joueur,surplus):
	'''met le surplus d'une ligne dans la copie du plancher'''
	for i in range(len(lst_carre)-surplus,len(lst_carre)):
		plancher1[joueur].insert(0,lst_carre[i])
		if 'light grey' in plancher1[joueur]:
			plancher1[joueur].remove('light grey')
	return plancher1

def plancher_joueurs(nombre_joueurs):

	'''créer des listes non-vide en fonction du nombres de joueurs qui permettent d'afficher la liste des planchers par joueurs'''

	lst = []
	for i in range(nombre_joueurs):
		lst.append(['light grey','light grey','light grey','light grey','light grey','light grey','light grey'])
	return lst

def remplissage_malus(plancher1,joueur):
	'''ajoute la tuile de malus dans la copie de plancher'''
	for i in plancher1:
		if 'light green' in i:
			return plancher1
	plancher1[joueur].insert(0,'light green')
	if 'light grey' in plancher1[joueur]:
		plancher1[joueur].remove('light grey')
	return plancher1

def reste_vide(totale_reste):

	'''permet de vérifier si le reste est vide en renvoyant un booléen'''

	for i in range(5):
		if len(totale_reste[i]) > 0:
			return False
	return True

def copie_matrice(M):
	'''Fonction copiant une matrice'''
	mat_copie=[]
	for i in range(len(M)):
		mat_copie.append([])
		for j in range(len(M[i])):
			mat_copie[i].append(M[i][j])
	return mat_copie

def remplissage_mur(mur_visu,mur_id,ligne_motifs,nombre_joueur,score,plancher):

	'''Remplis le mur et compte les points raportés par chaque tuile'''

	for joueur in range(nombre_joueur): #pour chaque joueur
		for ligne in range(5): #pour chaque ligne du mur
			if len(ligne_motifs[joueur][ligne])==ligne+1: #si la ligne du motif est pleine
				for couleur in range(5): 
					if mur_visu[1][ligne][couleur]==ligne_motifs[joueur][ligne][0]: #on regarde à quelle couleur elle correspond
						mur_id[joueur][ligne][couleur]=1 #une fois que la couleur a été trouvée on indique que la case est pleine
						score=comptage_score(score,mur_id,joueur,ligne,couleur) #on compte le score que la tuile rapporte
		score[joueur]-=malus_plancher(plancher,joueur) #on applique le malus du plancher à chaque joueur
	
	return mur_id,score

def comptage(mur_id,joueur,y_ajout,x_ajout,var_y,var_x):
	'''fonction qui va compter l'alignement des tuiles sur une des quatres cardinalitées'''
	
	x_ajout += var_x 
	y_ajout += var_y
	if 0<=y_ajout<len(mur_id[joueur]) and 0<=x_ajout<len(mur_id[joueur][0]):
		if mur_id[joueur][y_ajout][x_ajout]==1:		
			return 1 + comptage(
						mur_id,joueur, 
						x_ajout, 
						y_ajout, 
						var_x,
						var_y)
	return 0

def malus_plancher(plancher,joueur):

	'''fonction qui renvoie le malus du plancher d'un joueur'''

	compteur=0
	malus=0
	for i in range(len(plancher[joueur])):
		if plancher[joueur][i]=='light grey' or compteur>6:
			break
		compteur+=1
		if 0<compteur<=2:
			malus+=1
		if 2<compteur<=5:
			malus+=2
		if 5<compteur:
			malus+=3
	return malus	

def comptage_score(score,mur_id,joueur,y_ajout,x_ajout):
	'''fonction qui compte les points rapportés par une case quand on la pose'''
	score_joueur=score[joueur]	
	score_init=score[joueur]

	score[joueur]+= comptage(mur_id, joueur, y_ajout, x_ajout, -1, 0)#top
	score[joueur]+= comptage(mur_id, joueur, y_ajout, x_ajout, 1, 0)#bot
	if score_joueur!=score[joueur]: #si le score a varié cela veut dire qu'il faut compter un point pour la case en elle même
		score[joueur]+=1
		score_joueur=score[joueur]


	score[joueur]+= comptage(mur_id, joueur, y_ajout, x_ajout, 0, 1)#right
	score[joueur]+= comptage(mur_id, joueur, y_ajout, x_ajout, 0, -1)#left
	if score_joueur!=score[joueur]: #si le score a varié cela veut dire qu'il faut compter un point pour la case en elle même
		score[joueur]+=1
		score_joueur=score[joueur]
	
	if score_init==score[joueur]: #dans le cas ou la tuile est solitaire elle vaut quand même un point
		score[joueur]+=1 

	return score

def ligne_bonus(mur_id,joueur):
	'''fonction qui va renvoyer le bonus des lignes pour un joueur'''
	bonus=0
	for lignes in mur_id[joueur]:
		if lignes==[1,1,1,1,1]:
			bonus+=2
	
	return bonus

def colonne_bonus(mur_id, joueur):
	'''fonction qui va renvoyer le bonus des colonnes pour un joueur'''
	bonus=0
	
	for colonnes in range(len(mur_id[joueur][0])):
		compteur=0
		for ligne in range(len(mur_id[joueur])):
			if mur_id[joueur][ligne][colonnes]==1:
				compteur+=1
		if compteur==5:
			bonus+=7
	
	return bonus

def tuiles_bonus(mur_id,joueur,mur_visu):
	tuiles={'blue':0,'red':0,'yellow':0,'green':0,'black':0}

	for ligne in range(len(mur_id[joueur])):
		for colonnes in range(len(mur_id[joueur][0])):
			if mur_id[joueur][ligne][colonnes]==1:
				tuiles[mur_visu[1][ligne][colonnes]]+=1

	bonus=0
	for values in tuiles.values():
		if values==5:
			bonus+=10
	
	return bonus

def total_bonus(mur_id,score,mur_visu):
	'''fonction qui gère les bonus de fin de partie'''
	for joueur in range(len(score)):
		score[joueur]+=ligne_bonus(mur_id,joueur)
		score[joueur]+=colonne_bonus(mur_id,joueur)
		score[joueur]+=tuiles_bonus(mur_id,joueur,mur_visu)
	return score

def score_init(nb_joueurs):
	'''initi le score'''

	score=[]
	for i in range(nb_joueurs):
		score.append(0)
	return score

def lst_ver_fich(lst):

	'''fonction qui transforme une liste en chaine de charactère'''

	char=''
	for element in lst:
		char+=str(element)+','
	return char

def matrice_ver_fich(mat):
	'''transforme une matrice en une ligne ou chaque ligne est séparée par des / '''
	char=''
	for lignes in range(len(mat)):
		for colonnes in range(len(mat[lignes])):
			char+=str(mat[lignes][colonnes])+','
		char+='/'
	return char

def LLL_ver_fich(LLL):
	'''transforme une liste de liste de liste en une ligne, chaque ligne étant séparé par un \\ '''
	char=''
	for joueur in LLL:
		char+=matrice_ver_fich(joueur)
		char+='/\\'
	
	return char

def fich_ver_liste(ligne):
	'''transforme une chaine de charactere en liste'''
	if ligne!='':
		return ligne.split(',')	
	else:
		return []

def fich_ver_matrice(ligne):
	'''transforme une ligne en matrice'''
	ephemere=''
	mat=[]
	for lettre in ligne:
		if lettre!='/':
			ephemere+=lettre
		else:
			mat.append(fich_ver_liste(ephemere[:-1]))
			ephemere='' 
	return mat

def fich_ver_LLL(ligne):
	'''transforme une ligne en liste de liste de liste'''
	Li=[]
	ephemere=''
	for lettre in ligne:
		if lettre!='\\':
			ephemere+=lettre
		else:
			Li.append(fich_ver_matrice(ephemere[:-1])) 
			ephemere=''
	return Li

def char_ver_int_lst(lst):
	
	'''transforme tout ce que contient une liste en entier'''

	for i in range(len(lst)):
		lst[i]=int(lst[i])
	return lst

def char_ver_int_LLL(LLL):

	'''transforme tout ce que contient une liste de liste de liste en entier'''

	for i in range(len(LLL)):
		for j in range(len(LLL[i])):
			for k in range(len(LLL[i][j])):
				LLL[i][j][k]=int(LLL[i][j][k])
	return LLL

def char_ver_bool(char):

	'''transforme une chaine de charactère en booleen'''

	if char=='False':
		return False
	else:
		return True

def sauvegarde(nb_joueurs,jouer_bot,paquet,score,plancher,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu):
	
	'''Fonction qui sauvegarde des paramètres sous forme de chaine de charactère'''
	
	with open('Sauvegarde.txt','w') as f:
		f.write(str(nb_joueurs)+'\n')
		f.write(str(jouer_bot)+'\n')
		f.write(str(lst_ver_fich(paquet))+'\n')
		f.write(str(lst_ver_fich(score))+'\n')
		f.write(str(matrice_ver_fich(plancher))+'\n')
		f.write(str(matrice_ver_fich(plancher1))+'\n')
		f.write(str(matrice_ver_fich(total_reste))+'\n')
		f.write(str(premier_reste)+'\n')
		f.write(str(fabrique_vide)+'\n')
		f.write(str(select_tuile_verif)+'\n')
		f.write(str(joueur)+'\n')
		f.write(str(compt)+'\n')
		f.write(str(matrice_ver_fich(toutes_fabriques))+'\n')
		f.write(str(LLL_ver_fich(ligne_motifs))+'\n')
		f.write(str(choix_dans_reste)+'\n')
		f.write(str(LLL_ver_fich(mur_id))+'\n')
		f.write(str(nb_fabrique)+'\n')
		f.write(str(LLL_ver_fich(mur_visu))+'\n')

def recuperation():

	'''Fonction qui récupère les paramètre stockés dans un fichier et les renvoie sous la forme voulue'''

	f=open('Sauvegarde.txt','r')
	nb_joueurs=int((f.readline())[:-1])
	jouer_bot=char_ver_bool((f.readline())[:-1])
	paquet=fich_ver_liste((f.readline())[:-2])
	score=char_ver_int_lst(fich_ver_liste((f.readline()[:-2])))
	plancher=fich_ver_matrice(f.readline()[:-1])
	plancher1=fich_ver_matrice(f.readline()[:-1])
	total_reste=fich_ver_matrice(f.readline()[:-1])
	premier_reste=char_ver_bool((f.readline())[:-1])
	fabrique_vide=char_ver_bool((f.readline())[:-1])
	select_tuile_verif=char_ver_bool((f.readline())[:-1])
	joueur=int((f.readline())[:-1])
	compt=int((f.readline())[:-1])
	toutes_fabriques=fich_ver_matrice(f.readline()[:-1])
	ligne_motifs=fich_ver_LLL(f.readline()[:-1])
	choix_dans_reste=char_ver_bool((f.readline())[:-1])
	mur_id=char_ver_int_LLL(fich_ver_LLL(f.readline()[:-1]))
	nb_fabrique=int(f.readline()[:-1])
	mur_visu=fich_ver_LLL(f.readline()[:-1])
	f.close()

	return nb_joueurs,jouer_bot,paquet,score,plancher,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu

def fichier_plein(fichier):
	'''fonction qui vérifie si le fichier n'est pas vide'''
	with open(fichier,'r') as f:
		t=f.read()
		if t!='':
			return True
	return False

def fab_vide(toutes_fabriques,nb_fabriques):
	'''fonction qui verifie si les fabriques sont vides'''

	compt = 0
	if toutes_fabriques != None:
		for i in range(nb_fabriques):
			if toutes_fabriques[i][0] == 'white':
				compt += 1
			if compt == nb_fabriques:
				return True #la fabrique est vide
		return False #la fabrique n'est pas vide
	return True #il faut initialiser la fabrique

def vide_ligne_joueur(lignes_motifs):
	'''vide les lignes pleines des joueurs '''
	for i in range(len(lignes_motifs)):
		for j in range(len(lignes_motifs[i])):
			if len(lignes_motifs[i][j]) == j+1:
				lignes_motifs[i][j] = []
	return lignes_motifs

######################################VISUEL###############################################

def deselection_visu(fabrique,nb_fabriques):
	'''enlève le contour orange quand le joueur change sa selection'''
	for i in range(nb_fabriques):
		if fabrique[i][0] != 'white':
			affichage_carre(liste_coord_cercles_x,liste_coord_cercles_y,ancien_cote_carre,i,2,None,None)
		cercle(liste_coord_cercles_x[i],liste_coord_cercles_y[i],rayon,'black', epaisseur=3)

def affichage_carre(liste_coord_cercles_x,liste_coord_cercles_y,cote_carre,indice,epaisseur,couleur,remplissage):

	'''Fonction qui affiche 4 carrées sous forme de croix'''

	rectangle(liste_coord_cercles_x[indice]-(cote_carre*1.5), liste_coord_cercles_y[indice]+(cote_carre*1.5), liste_coord_cercles_x[indice]+(cote_carre*1.5), liste_coord_cercles_y[indice]+(cote_carre*4.5),remplissage=remplissage,epaisseur=epaisseur,couleur=couleur)
	rectangle(liste_coord_cercles_x[indice]-(cote_carre*4.5),liste_coord_cercles_y[indice]-(cote_carre*1.5),liste_coord_cercles_x[indice]-(cote_carre*1.5),liste_coord_cercles_y[indice]+(cote_carre*1.5),remplissage=remplissage,epaisseur=epaisseur,couleur=couleur)
	rectangle(liste_coord_cercles_x[indice]+(cote_carre*1.5), liste_coord_cercles_y[indice]-(cote_carre*1.5), liste_coord_cercles_x[indice]-(cote_carre*1.5), liste_coord_cercles_y[indice]-(cote_carre*4.5),remplissage=remplissage,epaisseur=epaisseur,couleur=couleur)
	rectangle(liste_coord_cercles_x[indice]+(cote_carre*4.5),liste_coord_cercles_y[indice]+(cote_carre*1.5),liste_coord_cercles_x[indice]+(cote_carre*1.5),liste_coord_cercles_y[indice]-(cote_carre*1.5),remplissage=remplissage,epaisseur=epaisseur,couleur=couleur)

def grille_joueur(joueur,ligne_motifs):

	'''affiche les lignes des joueurs'''

	rectangle(largeurFenetre,hauteurFenetre,largeurFenetre-7*(cote_carre),hauteurFenetre-7*(cote_carre), epaisseur=2,remplissage='light gray')
	texte(largeurFenetre-2*(cote_carre),hauteurFenetre-6.5*(cote_carre),chaine="joueur"+str(joueur+1),couleur='black',taille=10,ancrage='center',police='Arial')
	for i in range(1,6):
		for j in range(1,5-i+2):
			rectangle(largeurFenetre-7*(cote_carre)+j*(cote_carre),hauteurFenetre-cote_carre-i*(cote_carre),largeurFenetre-6*(cote_carre)+j*(cote_carre),hauteurFenetre-i*(cote_carre),epaisseur=2)
	for j in range(5):
		y=hauteurFenetre-(6-j)*(cote_carre)
		for i in range(len(ligne_motifs[joueur][j])):
			rectangle(largeurFenetre-(6-i)*(cote_carre),y,largeurFenetre-(5-i)*(cote_carre),y+(cote_carre),couleur='black',remplissage=ligne_motifs[joueur][j][i],epaisseur=2)

def Choix_nombre_joueurs():

	'''écran de sélection du nombres de joueurs'''

	rectangle(largeurFenetre-largeurFenetre//6,0,largeurFenetre,30,couleur='#ae1f1f',remplissage='#ae1f1f')
	texte(largeurFenetre-largeurFenetre//6,2,'Fermer',couleur='white',taille=20,police='Arial') 

	rectangle(0,hauteurFenetre//8,largeurFenetre//3,hauteurFenetre,couleur='#890000',remplissage='red',epaisseur=5)
	texte(largeurFenetre//6 - largeurFenetre//12,hauteurFenetre//2,'2 Joueurs',couleur='white',taille=24,police='Arial')     

	rectangle(largeurFenetre//3,hauteurFenetre//8,largeurFenetre-largeurFenetre//3,hauteurFenetre,couleur='#070078',remplissage='blue',epaisseur=5)
	texte(largeurFenetre//2 - largeurFenetre//12,hauteurFenetre//2,'3 joueurs',couleur='white',taille=24,police='Arial') 
	
	rectangle(largeurFenetre-largeurFenetre//3,hauteurFenetre//8,largeurFenetre,hauteurFenetre,couleur='#045a00',remplissage='green',epaisseur=5)
	texte(largeurFenetre-largeurFenetre//6 - largeurFenetre//12,hauteurFenetre//2,'4 joueurs',couleur='white',taille=24,police='Arial')

	rectangle(largeurFenetre//3,0,largeurFenetre-largeurFenetre//3,hauteurFenetre//8,couleur='#585858',remplissage='gray',epaisseur=5)
	texte(largeurFenetre//2-largeurFenetre//8,hauteurFenetre//30,'Jouer avec le bot',couleur='white',taille=24,police='Arial')

	rectangle(0,0,largeurFenetre//6,30,couleur='orange',remplissage='orange')
	texte(0,2,'Reprendre',couleur='white',taille=20,police='Arial')

def Mur_visuel():
	'''Cette fonction va renvoyer une matrice similiare à tableau de jeu mais avec des couleurs pastelles, qui montre les cases non remplies'''
	mur_visu=[[]] #ce tableau va devenir une matrice carré de coté 5
	if os.path.isfile('selec_mur'):
		with open('selec_mur','r') as f:
			for ligne in f:
				if ligne[:4]=='True':
					mur_visu=fich_ver_LLL(ligne[6:])
					break

	if mur_visu==[[]]:
		lignes=['#558d8b','#8d5557','#bcb769','#82b16e','#5f655b']
		for i in range(5):
			mur_visu[0].append(list(lignes)) #on ajoute la ligne
			lignes.insert(0,lignes[4]) #sur la ligne on déplace la dernière case en première position
			lignes.pop() #une fois déplacé on la supprime
		
		mur_visu.append(Mur_reel())
	
	return mur_visu

def bouton_restart():
	'''affiche le bouton restart'''
	rectangle(0,0,largeurFenetre//6,30,couleur='#aaf481',remplissage='#aaf481')
	texte(0,2,'Restart',couleur='white',taille=20,police='Arial') 

def reprendre_visu(x,y):

    #permet de reprendre la partie sauvegardé

    if x >= 0 and y >= 0 and x <= largeurFenetre//6 and y <= 30:
        return True
    return False

def bouton_fermer():
	'''affiche le bouton fermer'''
	rectangle(largeurFenetre-largeurFenetre//6,0,largeurFenetre,30,couleur='#ae1f1f',remplissage='#ae1f1f',epaisseur=3)
	texte(largeurFenetre-largeurFenetre//6,2,'Fermer',couleur='white',taille=20,police='Arial') 

def bouton_jouer():

	'''dessine le bouton jouer'''

	rectangle(largeurFenetre*2/5,hauteurFenetre*5/6,largeurFenetre*3/5,hauteurFenetre, couleur='#3b6822' ,remplissage='orange',epaisseur=3)
	texte(largeurFenetre/2,hauteurFenetre*11/12,'Jouer',ancrage='center',taille=20, couleur='white',police='Arial')

def visu_plancher(plancher,joueur):

	'''affiche le plancher'''
	for i in range(7):
		rectangle(largeurFenetre-8*(cote_carre),hauteurFenetre-i*(cote_carre),largeurFenetre-7*(cote_carre),hauteurFenetre-(i+1)*(cote_carre),couleur='black',epaisseur=2,remplissage=plancher[joueur][i])
		
	for i in range(2):
		texte(largeurFenetre-7*(cote_carre),hauteurFenetre-(i+1)*(cote_carre),chaine=('-1') ,ancrage='ne', couleur='black',taille=9,police='Arial')
	for i in range(2,5):
		texte(largeurFenetre-7*(cote_carre),hauteurFenetre-(i+1)*(cote_carre),chaine=('-2') ,ancrage='ne', couleur='black',taille=9,police='Arial')
	for i in range(5,7):
		texte(largeurFenetre-7*(cote_carre),hauteurFenetre-(i+1)*(cote_carre),chaine=('-3') ,ancrage='ne', couleur='black',taille=9,police='Arial')

def zone_fabrique(fabrique,nb_fabriques):
	'''affiche la zone des fabriques, remplies'''
	cercle(largeurFenetre//2,0,hauteurFenetre/1.5,epaisseur=5,couleur='#3b6822',remplissage='light grey')

	for i in range(nb_fabriques):
		cercle(liste_coord_cercles_x[i],liste_coord_cercles_y[i],rayon,epaisseur=3)
		for k in range(4):
			rectangle(liste_coord_cercles_x[i]+(ancien_cote_carre*lst_select_carre1_visu[k]), liste_coord_cercles_y[i]+(ancien_cote_carre*lst_select_carre2_visu[k]), liste_coord_cercles_x[i]+(ancien_cote_carre*lst_select_carre3_visu[k]), liste_coord_cercles_y[i]+(ancien_cote_carre*lst_select_carre4_visu[k]),remplissage=fabrique[i][k],epaisseur=2)

def zone_motif():
	'''affiche la zone de jeu des joueurs'''
	rectangle(largeurFenetre,hauteurFenetre,largeurFenetre-7*(cote_carre),hauteurFenetre-7*(cote_carre), epaisseur=2,remplissage='light gray')
	texte(largeurFenetre-2*(cote_carre),hauteurFenetre-6.5*(cote_carre),chaine="joueur1",couleur='black',taille=10,ancrage='center',police='Arial')
	for i in range(1,6):
		for j in range(1,5-i+2):
			rectangle(largeurFenetre-7*(cote_carre)+j*(cote_carre),hauteurFenetre-cote_carre-i*(cote_carre),largeurFenetre-6*(cote_carre)+j*(cote_carre),hauteurFenetre-i*(cote_carre),epaisseur=2)
	
def mur_joueur(nombre_de_joueurs,mur_visuel,mur_id):
	'''affiche le mur des joueur'''
	joueur=1
	for k in range(0,5*(nombre_de_joueurs-1),6):
		for i in range(4,-1,-1):
			for j in range(1,6):
				rectangle(0+j*(cote_carre),hauteurFenetre-(4-i+k)*(cote_carre)-2,(cote_carre)+j*(cote_carre),hauteurFenetre-(4-i+k+1)*(cote_carre)-2,epaisseur=2,remplissage=mur_visuel[mur_id[joueur][i][j-1]][i][j-1])
		joueur+=1
		texte(2*(cote_carre),hauteurFenetre-12-(5+k)*(cote_carre),chaine="joueur"+str(joueur),couleur='black',taille=10,ancrage='center',police='Arial')

	for i in range(4,-1,-1):
		for j in range(1,6):
			rectangle(6*(cote_carre)+j*(cote_carre),hauteurFenetre-(4-i)*(cote_carre)-2,7*(cote_carre)+j*(cote_carre),hauteurFenetre-(4-i+1)*(cote_carre)-2,epaisseur=2,remplissage=mur_visuel[mur_id[0][i][j-1]][i][j-1])
	texte(8*(cote_carre),hauteurFenetre-12-(5)*(cote_carre),chaine="joueur1",couleur='black',taille=10,ancrage='center',police='Arial')
	
def reste():
	'''affiche le reste vide'''
	for i in range(10):
		for j in range(5):
			rectangle(largeurFenetre-(4-j)*(cote_carre),hauteurFenetre-(7+i)*(cote_carre)-1,largeurFenetre-(5-j)*(cote_carre),hauteurFenetre-(8+i)*(cote_carre)-1, couleur='#3b6822',epaisseur=2,remplissage='light grey')

def affiche_grille(nombre_de_joueurs,fabrique,mur_visuel,mur_id,nb_fabriques,total_reste,plancher,joueur):
	'''
	Cette fonction permet d'afficher La grille voulus dans l'ennoncer 
	'''
	rectangle(0,0,largeurFenetre,hauteurFenetre,couleur='#72c147',remplissage='#72c147',epaisseur=3)

	bouton_restart()
	bouton_fermer()
	bouton_jouer()
	visu_plancher(plancher,joueur)
	zone_fabrique(fabrique,nb_fabriques)
	zone_motif()
	mur_joueur(nombre_de_joueurs,mur_visuel,mur_id)
	reste()
	remplissage_visu_reste(total_reste)

def remplissage_visu_lignes(raw_select,lst_motif,joueur):

	'''Remplis la ligne sélectioner par le joueur.'''

	y=hauteurFenetre-(6-raw_select)*(cote_carre)
	for i in range(len(lst_motif[joueur][raw_select])):
		rectangle(largeurFenetre-(6-i)*(cote_carre),y,largeurFenetre-(5-i)*(cote_carre),y+(cote_carre),couleur='black',remplissage=lst_motif[joueur][raw_select][i],epaisseur=2)

def remplissage_visu_reste(total_reste):

	'''remplis visuellement le reste a partir du total_reste'''
	reste()
	for i in range(len(total_reste)):
		for j in range(len(total_reste[i])):
			rectangle(largeurFenetre-(4-i)*(cote_carre),hauteurFenetre-(7+j)*(cote_carre)-1,largeurFenetre-(5-i)*(cote_carre),hauteurFenetre-(8+j)*(cote_carre)-1, couleur='#3b6822',epaisseur=2,remplissage=total_reste[i][0])

def vide_carre(fabrique):
	'''permet de vider les tuiles remplis a la fin d'un tour'''
	affichage_carre(liste_coord_cercles_x,liste_coord_cercles_y,ancien_cote_carre,fabrique,2,'light grey','light grey')

def affichage_score(score):
	'''affiche le score sur un fond gris'''
	y=1/3*hauteurFenetre
	
	rectangle(1/3*largeurFenetre,y,2/3*largeurFenetre,y*2,couleur='black',remplissage='light grey',epaisseur=2)
	texte(1/2*largeurFenetre,y+15,'Scores:',taille=15,ancrage='center',police='Arial')

	for i in range(len(score)):
		texte(1/3*largeurFenetre+10,y+(1/15*hauteurFenetre)*(i+1),'Joueur'+str(i+1)+': '+str(score[i]),taille=12)
	texte(1/2*largeurFenetre,y*2-8,'cliquez ou vouz voulez pour fermer la fenetre',taille=9,ancrage='center',police='Arial')
	attente_clic()

def ecran_fin_de_jeu(score):

	'''affiche l'écran des scores en fin de jeu'''

	rectangle(1/3*largeurFenetre,1/3*hauteurFenetre,2/3*largeurFenetre,1/6*hauteurFenetre,couleur='black',remplissage='light grey',epaisseur=2)
	texte(1/2*largeurFenetre,1/6*hauteurFenetre+30,'La partie est finie',ancrage='center',police='Arial')
	affichage_score(score)

################################# INTERACTIONS ####################

def recuperation_nombre_joueurs(x,y):

	'''permet d'avoir le nombre de joueurs sur la séletion des joueurs.'''

	if x >= 0 and y >= hauteurFenetre//8 and x <= largeurFenetre//3 and y <= hauteurFenetre:
		return 2
	elif x >= largeurFenetre//3 and y >= hauteurFenetre//8 and x <= largeurFenetre-largeurFenetre//3 and y <= hauteurFenetre:
		return 3
	elif x >= largeurFenetre-largeurFenetre//3 and y >= hauteurFenetre//8 and x <= largeurFenetre and y <= hauteurFenetre:
		return 4

def recuperation_carre(x,y,nb_joueurs,fabrique,nb_fabriques):

	'''permet de récupérer une liste des couleur sélectionner et non-sélectionner des fabriques.
	colore les contours des carrés sélectionner.'''


	for i in range(5):
			rectangle(largeurFenetre-(4-i)*(cote_carre),hauteurFenetre-(17)*(cote_carre)-1,largeurFenetre-(5-i)*(cote_carre),hauteurFenetre-7*(cote_carre), couleur='#3b6822',epaisseur=2)
	deselection_visu(fabrique,nb_joueurs)

	for i in range(nb_fabriques):
		lst = []
		no_select = list(fabrique[i])

		if fabrique[i][0] != 'white':
			if sqrt(((x-liste_coord_cercles_x[i])**2)+((y-liste_coord_cercles_y[i])**2)) <= rayon:
				cercle(liste_coord_cercles_x[i],liste_coord_cercles_y[i],rayon,'orange', epaisseur=3)

				for k in range(4):
					
					if (liste_coord_cercles_x[i]+(ancien_cote_carre*lst_select_carre1[k]))<=x<=(liste_coord_cercles_x[i]+(ancien_cote_carre*lst_select_carre2[k])) and (liste_coord_cercles_y[i]+(ancien_cote_carre*lst_select_carre3[k])<=y<=liste_coord_cercles_y[i]+(ancien_cote_carre*lst_select_carre4[k])):	
						for tuiles in range(len(fabrique[i])):
							if fabrique[i][tuiles] == fabrique[i][k]:
								for j in range(4):
									if tuiles == j:
										rectangle(liste_coord_cercles_x[i]+(ancien_cote_carre*lst_select_carre1_visu[j]), liste_coord_cercles_y[i]+(ancien_cote_carre*lst_select_carre2_visu[j]), liste_coord_cercles_x[i]+(ancien_cote_carre*lst_select_carre3_visu[j]), liste_coord_cercles_y[i]+(ancien_cote_carre*lst_select_carre4_visu[j]),couleur='orange',epaisseur=2)
										lst.append(fabrique[i][tuiles])
										no_select.remove(fabrique[i][tuiles])
						return lst, no_select, i

	
	return None, None, None
	
def recuperation_lignes(x,y):

	'''permet d'avoir la ligne sélectionner par le joueur ainsi que de colorer la ligne sélectionner.'''

	for i in range(1,6):
		for j in range(1,5-i+2):
			rectangle(largeurFenetre-7*(cote_carre)+j*(cote_carre),hauteurFenetre-cote_carre-i*(cote_carre),largeurFenetre-6*(cote_carre)+j*(cote_carre),hauteurFenetre-i*(cote_carre),epaisseur=2)
	rectangle(largeurFenetre-8*(cote_carre),hauteurFenetre,largeurFenetre-7*(cote_carre),hauteurFenetre-(7)*(cote_carre),couleur='black',epaisseur=2)

	for i in range(1,6):

		if ((largeurFenetre-i*(cote_carre))>x>(largeurFenetre-6*(cote_carre))) and ((hauteurFenetre-i*(cote_carre))>y>(hauteurFenetre-(i+1)*(cote_carre))):
			rectangle(largeurFenetre-i*(cote_carre),hauteurFenetre-i*(cote_carre),largeurFenetre-6*(cote_carre),hauteurFenetre-(i+1)*(cote_carre),couleur='orange',epaisseur=2)
			return 5-i,True
	
	if (largeurFenetre-8*(cote_carre)<x<largeurFenetre-7*(cote_carre)) and (hauteurFenetre>y>hauteurFenetre-7*(cote_carre)):
		rectangle(largeurFenetre-8*(cote_carre),hauteurFenetre,largeurFenetre-7*(cote_carre),hauteurFenetre-(7)*(cote_carre),couleur='orange',epaisseur=2)
		return 6, True
	
	
	return None,False

def fermeture(x,y):

	'''permet de fermer le jeu en cours'''

	if x >= largeurFenetre - largeurFenetre//6 and y >= 0 and x <= largeurFenetre and y <= 30:
		return False
	return True	

def redemarrer(x,y):

	'''permet de recommencer le jeux pour les tests sans devoir fermer la fenêtre'''

	if x >= 0 and y >= 0 and x <= largeurFenetre//6 and y <= 30:
		return True
	return False

def reprendre(x,y):

	'''zone cliquable dans lequel on peut reprendre un partie '''

	if x >= 0 and y >= 0 and x <= largeurFenetre//6 and y <= 30:
		return True
	return False

def recuperation_reste(x,nb_fabriques,total_reste,fabrique):

	'''permet de récupérer le reste sélectionner par le joueur 
		renvoie donc la liste des tuiles sélectionner ainsi que la colone sélectionner'''

	deselection_visu(fabrique,nb_fabriques)

	for i in range(5):
			rectangle(largeurFenetre-(4-i)*(cote_carre),hauteurFenetre-(17)*(cote_carre)-1,largeurFenetre-(5-i)*(cote_carre),hauteurFenetre-7*(cote_carre), couleur='#3b6822',epaisseur=2)		
	
	for i in range(5):
		if len(total_reste[i]) != 0:
			if largeurFenetre-(4-i)*(cote_carre)>x>largeurFenetre-(5-i)*(cote_carre) :
				rectangle(largeurFenetre-(4-i)*(cote_carre),hauteurFenetre-(17)*(cote_carre)-1,largeurFenetre-(5-i)*(cote_carre),hauteurFenetre-7*(cote_carre), couleur='orange',epaisseur=2)
				return total_reste[i],i

	return None,None

############################## BOT ##############################

def possibilite_IA_reste(total_reste):
	"""créer une liste des possibilités qu'a l'IA dans le reste"""
	result = []
	for i in range(len(total_reste)):
		if len(total_reste[i]) != 0:
			result.append(i+1)
	return result

def possibilite_IA(nb_fabriques):
	"""créer une liste des possibilité qu'a l'IA dans les fabriques"""

	possibilite_IA_lst=[]
	for i in range(nb_fabriques):
		possibilite_IA_lst.append(i)
	possibilite_IA_lst.append(nb_fabriques)
	return possibilite_IA_lst 

def meilleur_coup(total_reste,toutes_fabriques,nb_fabriques,possibilite_IA_lst,ligne_motifs,mur_visu,mur_id):

	lst_possibilite_IA_reste = possibilite_IA_reste(total_reste)
	meilleur_choix = [-1,'x_tuile','y_tuile','le z qui existe pas','x_motif','y_motif','le z qui existe pas'] #pour être sûr que meilleur_choix soit actualisé ont defini un niveau inferieur au plus bas possible

	for choix in possibilite_IA_lst[:-1]: #on teste toutes les fabriques
		for tuile in range(4): #on teste chaque tuile de la fabrique (elles peuvent être de couleur différentes)
			x_IA=liste_coord_cercles_x[choix] 
			y_IA=liste_coord_cercles_y[choix]
			
			if tuile==1:
				x_IA += 2 * ancien_cote_carre
			elif tuile==2:
				x_IA -= 2 * ancien_cote_carre
			elif tuile==3:
				y_IA += 2 * ancien_cote_carre
			elif tuile==4:
				y_IA -= 2 * ancien_cote_carre

			#on récupère la liste des carré lié à la selection des tuiles
			lst_carre,inutil1,inutil2=recuperation_carre(x_IA,y_IA,nb_joueurs,toutes_fabriques,nb_fabriques)
			if lst_carre:
				niveau_coup,x_motif,y_motif,_=coordonnee_motif_IA(ligne_motifs,lst_carre,mur_visu,mur_id) #on regarde que vaut le coup
		
				if niveau_coup>meilleur_choix[0]: #si le coup est meilleur que le dernier testé on le garde
					meilleur_choix[0],meilleur_choix[1],meilleur_choix[2],meilleur_choix[4],meilleur_choix[5]=niveau_coup,x_IA,y_IA,x_motif,y_motif
			
				if meilleur_choix[0]==5: # si c'est un des meilleur coup possible on s'arrette là
					return meilleur_choix

	for choix in lst_possibilite_IA_reste: #même principe qu'au dessus mais dans le reste
		y_IA = hauteurFenetre // 2
		x_IA = (largeurFenetre - 5 * (cote_carre)) + (choix * (cote_carre)) - 1

		lst_carre,inutil1=recuperation_reste(x_IA,nb_fabriques,total_reste,toutes_fabriques)
		if lst_carre:
			niveau_coup,x_motif,y_motif,_=coordonnee_motif_IA(ligne_motifs,lst_carre,mur_visu,mur_id)
	

			print(niveau_coup)
			print(meilleur_choix[0])
			if niveau_coup>meilleur_choix[0]:
				meilleur_choix[0],meilleur_choix[1],meilleur_choix[2],meilleur_choix[4],meilleur_choix[5]=niveau_coup,x_IA,y_IA,x_motif,y_motif
		
			if meilleur_choix[0]==5:
				return meilleur_choix

	return meilleur_choix

def coordonnee_motif_IA(ligne_motifs,lst_carre,mur_visu,mur_id):
	
	'''
	permet de déterminer avec le choix qu'a sélectionner le bot le meilleurs emplacement possible dans les lignes.
	Cela fonctionne de manière hiérarchique si un des choix meilleur qu'un autre, alors le programme va enregistrer 
	ce choix puis ne va pas vérifier les autres possibilité qui seraient moins bien pour la ligne courante.
	Il commence par la lecture des lignes en commençant par la ligne d'une case puis descent petit à petit jusqu'à la dernière ligne 
	tout en vérifiant les conditions meilleur ou égale au choix enregistrer.
	'''

	choix_fais = False
	choix_secondaire_fais = False
	choix_terciaire_fais = False
	choix_quartiere_fais = False
	choix_quintiere_fais = False
	niveau_coup = -1


	y_motif = None
	x_motif=largeurFenetre-6*(cote_carre)+10


	for j in range(len(ligne_motifs[1])):
		if (len(ligne_motifs[1][j]) == 0 or ligne_motifs[1][j][0] == lst_carre[0]) and mur_id[1][j][mur_visu[1][j].index(lst_carre[0])] == 0 and len(ligne_motifs[1][j])<(j+1):
			
			if (j+1)-len(ligne_motifs[1][j]) == len(lst_carre): # si le nombre de carre selectionner est égale à l'espace diponible
				y_motif = hauteurFenetre-(5-j) * (cote_carre) - 10
				choix_fais = True
				choix_secondaire_fais = True
				choix_terciaire_fais = True
				choix_quartiere_fais = True
				choix_quintiere_fais = True
				niveau_coup = 5

			elif not choix_fais and not len(ligne_motifs[1][j]) == 0 and ligne_motifs[1][j][0] == lst_carre[0] and (j+1)-len(ligne_motifs[1][j]) > len(lst_carre): #si on ne peut pas compléter une ligne et qu'on essai de remplir une ligne déjà commencer sans avoir de restes
				y_motif = hauteurFenetre-(5-j) * (cote_carre) - 10
				choix_secondaire_fais = True
				choix_terciaire_fais = True
				choix_quartiere_fais = True
				choix_quintiere_fais = True
				niveau_coup = 4

			elif not choix_secondaire_fais and (j+1)-len(ligne_motifs[1][j]) > len(lst_carre):  #si on ne peut pas compléter une ligne et qu'on essai de remplir une nouvelle ligne sans avoir de restes
				y_motif = hauteurFenetre-(5-j) * (cote_carre) - 10
				choix_terciaire_fais = True
				choix_quartiere_fais = True
				choix_quintiere_fais = True
				niveau_coup=3

			elif not choix_terciaire_fais and len(ligne_motifs[1][j]) == 0: # si on ne peut pas faire aucun des ca précédent, on vois si on peut compléter une nouvelle ligne avec du surplus
				y_motif = hauteurFenetre-(5-j) * (cote_carre) - 10
				choix_quartiere_fais = True
				choix_quintiere_fais = True
				niveau_coup = 2


			elif not choix_quartiere_fais and not len(ligne_motifs[1][j]) == 0 and ligne_motifs[1][j][0] == lst_carre[0]: # si on ne peut pas faire aucun des ca précédent, on vois si on peut compléter une ligne déjà entamé avec du surplus
				y_motif = hauteurFenetre-(5-j) * (cote_carre) - 10
				choix_quintiere_fais = True
				niveau_coup = 1

			elif not choix_quintiere_fais:
				x_motif = largeurFenetre-7*(cote_carre)-5
				y_motif = hauteurFenetre-5  
				niveau_coup = 0
		
	if niveau_coup!=-1:
		return niveau_coup,x_motif,y_motif,None
	else:
	#si rien ne semble possible après avoir tout essayé (parfois cela arrive) on met dans le plancher
		x_motif = largeurFenetre-7*(cote_carre)-5
		y_motif = hauteurFenetre-5  
		niveau_coup = 0
		return niveau_coup,x_motif,y_motif,None

def choix_bot(action_IA,meilleur_choix):

	'''fonction qui renvoie le choix du bot sous forme de coordonnées'''

	print(meilleur_choix)

	mise_a_jour()
	passage_joueur=False
	if action_IA==0: #d'abord les tuiles
		action_IA+=1
		x,y,_=meilleur_choix[1],meilleur_choix[2],meilleur_choix[3]

	elif action_IA==1: #puis le motif
		action_IA+=1
		x,y,_=meilleur_choix[4],meilleur_choix[5],meilleur_choix[6]

	elif action_IA==2: #enfin le bouton jouer
		action_IA=0
		passage_joueur=True
		x,y,_=largeurFenetre//2,hauteurFenetre-1,None
	
	return x,y,passage_joueur,action_IA

####################### MAIN ####################################

def selections_tuiles_fabriques_restes(select_tuile_verif,ligne_recup_verif,select_row,joueur,ligne_motifs,total_reste,lst_reste,plancher,premier_reste,plancher1,fabrique_selection,toutes_fabriques,colonne_a_vider,passage_joueur,jouer_bot,tour_bot,compt,fabrique_vide,lst_carre,nb_joueurs,choix_dans_reste,mur_visu,mur_id,possibilite_IA_lst):
	
	'''fonction qui va remplir les motifs et/ou le plancher et faire passer le tour'''
	
	if select_tuile_verif and ligne_recup_verif: #si des tuiles et les lignes sont selectionnés 
		select_tuile_verif = False
		if select_row != 6: #si choisis de jouer hors du plancher

			
			if (len(ligne_motifs[joueur][select_row]) == 0 or ligne_motifs[joueur][select_row][0] == lst_carre[0]) and mur_id[joueur][select_row][mur_visu[1][select_row].index(lst_carre[0])] == 0: #si la ligne est vide ou que la couleur de la selection correspond à celle de la ligne et que le mur ne contient pas la couleur sélectionner

				espace_dispo = select_row + 1 - len(ligne_motifs[joueur][select_row]) #on regarde ce qui dépasse de la ligne
				surplus = len(lst_carre) - espace_dispo

				
				if len(lst_carre) >= espace_dispo: #si il y a trop de carré on en copie qu'une partie 
					ligne_motifs = remplissage_ligne(ligne_motifs,lst_carre,joueur,select_row,espace_dispo)
				else: #sinon on copie tout
					ligne_motifs = remplissage_ligne(ligne_motifs,lst_carre,joueur,select_row,len(lst_carre))
				
				if surplus > 0: #on met ensuite le surplus dans le plancher
					
					plancher1=copie_matrice(plancher) #afin d'éviter les soucis quand le joueur change d'avis le plancher est une copie 
					plancher1=remplissage_plancher(plancher1,lst_carre,joueur,surplus) #on remplis le plancher avec le surplus

				if len(lst_reste) > 0: # ce qui n'a pas été choisis dans la fabrique vas dans le reste
					total_reste=remplissage_reste(lst_reste, total_reste)
		
				remplissage_visu_lignes(select_row,ligne_motifs,joueur) #on affiche les motifs remplis et le reste
				remplissage_visu_reste(total_reste)
				
				if plancher1: #si il y a un plancher à afficher
					if premier_reste and choix_dans_reste: #on applique le malus si besoin (reste vers motif)
						plancher1 = remplissage_malus(plancher1,joueur)
					visu_plancher(plancher1,joueur) #on l'affiche
					plancher = copie_matrice(plancher1) #et on sauvegarde le choix definitif du joueur 

				if premier_reste and choix_dans_reste: #si le joueur a joué dans le reste et que le premier malus à été distribué
					premier_reste = False 			   #On ne le distribus plsu

		elif select_row == 6: #si on joue dans le plancher
			if plancher1: #on fait une copie du plancher comme plus haut
				if premier_reste and choix_dans_reste: #on applique le malus si besoin (reste vers motif)
					plancher1 = remplissage_malus(plancher1,joueur)
				visu_plancher(plancher1,joueur)
				plancher=copie_matrice(plancher1)

				if premier_reste and choix_dans_reste: #on actualise la distribution du malus
					premier_reste=False
		
			if len(lst_reste) > 0: #on met ce qui reste des fabriques dans le reste
				total_reste = remplissage_reste(lst_reste, total_reste)
				remplissage_visu_reste(total_reste)
			
		if  select_row == 6 or (len(ligne_motifs[joueur][select_row]) == 0 or ligne_motifs[joueur][select_row][0] == lst_carre[0]) and mur_id[joueur][select_row][mur_visu[1][select_row].index(lst_carre[0])] == 0:
			#si le joueur à fait une action qu'il a le droit de faire (jouer dans le plancher ou dans une ligne vide/de la bonne couleur)


			if fabrique_selection is not None: #si on à selectionner une fabrique on vide la fabriques
				toutes_fabriques[fabrique_selection] = ['white','white','white','white']
				vide_carre(fabrique_selection)
			else: #sinon on vide la colonne du reste qu'il faut vider 
				if colonne_a_vider is not None:#car on peut vouloir vider la colonne 0
					for i in range(len(total_reste[colonne_a_vider])):
						total_reste[colonne_a_vider].pop()
					remplissage_visu_reste(total_reste)		
			
			if passage_joueur: #on change de joueur
				joueur += 1
				if fabrique_selection != None:
					possibilite_IA_lst.remove(fabrique_selection)
				
				if jouer_bot:
					tour_bot = not tour_bot
					
				if joueur == nb_joueurs:
						joueur = 0

				fabrique_vide = False
	
	return fabrique_vide,select_tuile_verif,plancher,total_reste,joueur,tour_bot,compt,toutes_fabriques,plancher1,premier_reste,ligne_motifs,choix_dans_reste,possibilite_IA_lst

def selection_tuiles_fonctions(x,y,toutes_fabriques,select_tuile_verif,lst_carre,colonne_a_vider,plancher1,choix_dans_reste,lst_reste,fabrique_selection,total_reste,nb_fabriques):
	
	'''Fonction qui va renvoyer une liste de tuile en fonction des coordonnées du click du joueur'''
	
	if sqrt((largeurFenetre/2 - x) ** 2 + (0 - y) ** 2) < hauteurFenetre/1.5: #si on clique dans le cercle gris 
		choix_dans_reste = False #on precise qu'on a pas choisis dans le reste (gestion du malus)
		lst_carre, lst_reste, fabrique_selection=recuperation_carre(x,y,nb_fabriques,toutes_fabriques,nb_fabriques) #on récupère des tuiles
		if fabrique_selection == None: #si on à pas cliqué sur une fabrique, il n'y a rien de selectionné 
			select_tuile_verif = False 
		else:
			select_tuile_verif = True

	elif ((largeurFenetre - 5 * (cote_carre)) < x < largeurFenetre) and (hauteurFenetre - 7*(cote_carre) > y > (hauteurFenetre - 18 * (cote_carre))): #si on clique dans le reste
		lst_carre,colonne_a_vider = recuperation_reste(x,nb_fabriques,total_reste,toutes_fabriques) #on récupère les tuiles voulues
		lst_reste,fabrique_selection = [],None
		choix_dans_reste = True #on précise qu'on à choisis dans le reste (gestion du malus)
		select_tuile_verif = True

	if lst_carre == None: #si ce qu'on à selectionné ne renvoie aucun carré on empêche le joueur de jouer
		select_tuile_verif = False

	return lst_reste,colonne_a_vider,select_tuile_verif,plancher1,lst_carre,fabrique_selection,choix_dans_reste

def selection_lignes_fonction(x,y,joueur,plancher,ligne_recup_verif,ligne_motifs,lst_carre,plancher1,select_row):
	
	'''Fonction qui va renvoyer la ligne du motif que choisis le joueur'''
	
	if ((largeurFenetre - 8*(cote_carre))<x<largeurFenetre) and ((hauteurFenetre - 7 * (cote_carre)) < y < hauteurFenetre):#si on clique dans les motifs
		select_row, ligne_recup_verif = recuperation_lignes(x,y)
		plancher1=copie_matrice(plancher)
	
		if select_row and select_row != 6 and lst_carre and len(ligne_motifs[joueur][select_row]) == select_row+1 : #si on a fait un choix, qui n'est pas dans le planché
			ligne_recup_verif=False

		if select_row == 6 and lst_carre: #si on à choisis de jouer dans le plancher
			plancher1=copie_matrice(plancher)
			plancher1 = remplissage_plancher(plancher1,lst_carre,joueur,len(lst_carre)) #on remplis le plancher

	return ligne_recup_verif,plancher1,select_row

def selection_nombre_de_joueur(start,jouer_bot,condition_ouverture,nb_joueurs,paquet,score,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu):
	
	'''fonction qui va initialiser la partie et toutes la variables qui dépendent du nombre de joueur'''
	
	while start:
		x,y,_=attente_clic()	
		nb_joueurs = None
		plancher = None
		mur_id = None
		score = None
		ligne_motifs = None
		toutes_fabriques = None
		jouer_bot=False
		total_reste = [[],[],[],[],[]]
		possibilite_IA_lst = None

		if((0<x<largeurFenetre) and (hauteurFenetre//8<y<hauteurFenetre)) or largeurFenetre//3<x<largeurFenetre-largeurFenetre//3 and 0<y<hauteurFenetre//8: #si on clique sur les bouton des joueurs
			nb_joueurs = recuperation_nombre_joueurs(x,y)
			if largeurFenetre//3<x<largeurFenetre-largeurFenetre//3 and 0<y<hauteurFenetre//8: #si on clique sur le bouton 1v1 IA
				nb_joueurs,jouer_bot = 2,True
			efface_tout()																	
			plancher = plancher_joueurs(nb_joueurs)
			mur_id = Mur_id_complet(nb_joueurs)			#on efface tout et on initialise
			score = score_init(nb_joueurs)				#les variables qui dépendent nombre de joueur
			start = False
		
		elif not fermeture(x,y): #si on appuis sur le bouton 'fermer'
				condition_ouverture=False
				start=False
				continue
		
		elif reprendre(x,y) and os.path.isfile('Sauvegarde.txt') and fichier_plein('Sauvegarde.txt'): #si on essaye de charger une sauvegarde
			nb_joueurs,jouer_bot,paquet,score,plancher,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu=recuperation()
			start=False
			condition_ouverture=True
			possibilite_IA_lst=possibilite_IA(nb_fabrique)
	
	if reprendre(x,y): #si on charge une sauvegarde il faut supprimer les fabriques 'vides'
		affiche_grille(nb_joueurs,toutes_fabriques,mur_visu,mur_id,nb_fabrique,total_reste,plancher,joueur)
		for fabrique in range(len(toutes_fabriques)):
			if toutes_fabriques[fabrique]==['white', 'white', 'white', 'white']:
				vide_carre(fabrique)

	return nb_joueurs,jouer_bot,plancher,mur_id,score,condition_ouverture,nb_joueurs,jouer_bot,paquet,score,plancher,plancher1,total_reste,premier_reste,fabrique_vide,select_tuile_verif,joueur,compt,toutes_fabriques,ligne_motifs,choix_dans_reste,mur_id,nb_fabrique,mur_visu,possibilite_IA_lst

def remplir_fabrique_finir_jeu(ligne_motifs,mur_visu,mur_id,score,plancher,condition_ouverture,nb_joueurs,plancher1,toutes_fabriques,compt,nb_fabriques,paquet):

	'''fonction qui gère tout les changement relatif à la fin d'une manche'''

	if len(paquet) == 0:
		paquet = list(paquet_init)
	if ligne_motifs: #si il y a quelquechose dans les motifs on remplis le mur
		mur_id,score=remplissage_mur(mur_visu,mur_id,ligne_motifs,nb_joueurs,score,plancher)
	
	if condition_fermeture(mur_id): #le mur doit être remplis avant pour que la condition puisse être correctement évaluée
		score=total_bonus(mur_id,score,mur_visu)
		ecran_fin_de_jeu(score)
		condition_ouverture = False
		return	condition_ouverture,None,None,mur_id,score,None,None,ligne_motifs,plancher,plancher1,None,None,None
	
	if ligne_motifs: #on a besoin de cette condition pour ne pas afficher le score dès le début
		affichage_score(score) #on affiche le score

	tuile_reste = True
	toutes_fabriques,nb_fabriques = remplissage_fabriques(fabriques(nb_joueurs), paquet) #on remplis les fabriques
	plancher = plancher_joueurs(nb_joueurs)
	plancher1 = list(plancher) 
	premier_reste = True 
	fabrique_vide = False
	compt = 0
	possibilite_IA_lst = possibilite_IA(nb_fabriques)
	if ligne_motifs:
		ligne_motifs = vide_ligne_joueur(ligne_motifs)
	else:
		ligne_motifs = lignes_motifs_init(nb_joueurs)
	

	efface_tout()
	affiche_grille(nb_joueurs,toutes_fabriques,mur_visu,mur_id,nb_fabriques,total_reste,[['light grey','light grey','light grey','light grey','light grey','light grey','light grey']],0) #affiche la grille 
	
	return condition_ouverture,tuile_reste,toutes_fabriques,mur_id,score,fabrique_vide,compt,ligne_motifs,plancher,plancher1,nb_fabriques,premier_reste,possibilite_IA_lst

def condition_fermeture(mur_id):

	'''Fonction qui vérifie si une ligne du mur est pleine pour savoir si la partie doit se terminer'''

	if mur_id:
		for joueur in range(len(mur_id)):
			for lignes in range(len(mur_id[joueur])):
				if mur_id[joueur][lignes].count(1)==5:
					return True
	return False