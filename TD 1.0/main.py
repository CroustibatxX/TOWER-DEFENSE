from tkinter import *
import time
from math import*



########################################################## Classes #####################################################################


class Niveau:
        """Classe permettant de créer un niveau"""
        def __init__(self,fichier):
                self.liste = 0
                self.fichier = fichier
        
        def generer(self):
                """Méthode permettant de générer le niveau en fonction du fichier.
                On crée une liste générale, contenant une liste par ligne à afficher""" 
                #On ouvre le fichier
                with open(self.fichier, "r") as fichier:
                        structure_niveau = []
                        #On parcourt les lignes du filter                                                                                       
                        for ligne in fichier:
                                ligne_niveau = []
                                #On parcourt les sprites (lettres) contenus dans le fichier
                                for sprite in ligne:
                                        #On ignore les "\n" de fin de ligne
                                        if sprite != '\n':
                                                #On ajoute le sprite à la liste de la ligne
                                                ligne_niveau.append(sprite)
                                #On ajoute la ligne à la liste du niveau
                                structure_niveau.append(ligne_niveau)
                        #On sauvegarde cette structure
                        self.liste = structure_niveau
                        
        def afficher(self):
                """Méthode permettant d'afficher le niveau en fonction 
                de la liste de structure renvoyée par generer()"""
                self.fond=PhotoImage(file="images/fond.gif")
                canvas.create_image(0,0, anchor = NW, image=self.fond)
                self.fond_menu=PhotoImage(file="images/fond_menu.gif")
                canvas.create_image(0,780,anchor = NW, image=self.fond_menu)

                self.mur = PhotoImage(file="images/mur.gif")
                self.depart = PhotoImage(file="images/depart.gif")
                self.arrivee = PhotoImage(file="images/arrivee.gif")
                
                
                #On parcourt la liste du niveau
                num_ligne = 0
                for ligne in self.liste:
                        #On parcourt les listes de lignes
                        num_case = 0
                        for sprite in ligne:
                                #On calcule la position réelle en pixels
                                x = num_case * taille_sprite
                                y = num_ligne * taille_sprite
                                if sprite == 'm':                  #m = Mur
                                       canvas.create_image(x, y,anchor = NW,image=self.mur)
                                elif sprite == 'd':                #d = Départ
                                        canvas.create_image(x, y,anchor = NW,image=self.depart)
                                        
                                elif sprite == 'a':               #a = Arrivée
                                        canvas.create_image(x, y,anchor = NW,image=self.arrivee)
                                num_case += 1
                        num_ligne += 1

                self.tour1_menu_image= PhotoImage(file="images/tour1_menu.gif")
                self.tour1_menu=canvas.create_image(80,800,anchor=NW,image=self.tour1_menu_image)
                self.mine_menu_image=PhotoImage(file="images/mine_menu.gif")
                self.tour1_menu=canvas.create_image(300,800,anchor=NW,image=self.mine_menu_image)

class Mechant:
        def __init__(self,niveau,vitesse,vie,vitesse_tir):
                self.niveau=niveau
                
                #Variable des ennemis
                self.case_x=0
                self.case_y=0
                self.x = 60
                self.y = 0
                self.vitesse=vitesse
                self.vie_monstre=vie
                self.vie_monstre_ref=vie
                
                #Variable barre de vie des ennemis
                self.color='green'
                self.xBV=60
                self.xmaxBV=60
                self.yBV=0
                self.jaune=False
                self.rouge=False
                
                #Variable vitesse tir des tours 
                self.vitesse_tir=vitesse_tir

                

        def creation(self):
                self.img_monstre=PhotoImage(file="images/monstre.gif")
                self.monstre=canvas.create_image(self.case_x,self.case_y,image=self.img_monstre,anchor=NW,tag="monstre1")
                self.barre_vie=canvas.create_rectangle(self.xBV+10,self.yBV+45,self.xmaxBV+50,self.yBV+48,fill=self.color)#Creation barre de vie 
                liste_ennemi.append(self.monstre)
                
                self.detection()

        def deplacement(self):
                droite=0
                bas=0
                self.indication()
                canvas.itemconfigure(self.barre_vie,fill=self.color)
                
                if len(canvas.find_withtag("monstre1"))>0:
                        if self.vie_monstre<=0:
                                if self.monstre in liste_ennemi:
                                        liste_ennemi.remove(self.monstre) 
                                canvas.delete(self.monstre)
                                canvas.delete(self.barre_vie)
                                
                                             

                        if self.case_x < spriteX_max:
                                if niveau.liste[self.case_y][self.case_x+1] == 'a':           
                                        if self.monstre in liste_ennemi:
                                                liste_ennemi.remove(self.monstre)
                                        canvas.delete(self.monstre)
                                        canvas.delete(self.barre_vie)

                        if self.case_y < spriteY_max:
                                if niveau.liste[self.case_y+1][self.case_x] != 'm':
                                        bas=1
                        if self.case_x < spriteX_max-1:
                                if niveau.liste[self.case_y][self.case_x+1] != 'm':
                                        droite=1
                        if bas==1:
                                self.case_y += 1
                                self.y = self.case_y * taille_sprite
                                self.yBV=self.case_y * taille_sprite
                                self.xmaxBV=self.case_x * taille_sprite
                                if self.jaune==True:
                                        self.xmaxBV-=20
                                if self.rouge==True:
                                        self.xmaxBV-=35
                                canvas.coords(self.monstre,self.x,self.y)
                                canvas.coords(self.barre_vie,self.xBV+10,self.yBV+45,self.xmaxBV+50,self.yBV+48)
                                
                        if droite==1:
                                self.case_x += 1
                                self.x = self.case_x * taille_sprite
                                self.xBV=self.case_x * taille_sprite
                                self.xmaxBV=self.case_x * taille_sprite
                                if self.jaune==True:
                                        self.xmaxBV-=20
                                if self.rouge==True:
                                        self.xmaxBV-=35
                                canvas.coords(self.monstre,self.x,self.y)
                                canvas.coords(self.barre_vie,self.xBV+10,self.yBV+45,self.xmaxBV+50,self.yBV+48)
                             
                        canvas.after(self.vitesse,self.deplacement)
                
                
         
        def indication (self):
                if ((100*self.vie_monstre)/self.vie_monstre_ref)<=55:
                        self.color='yellow'
                        self.jaune=True
                        if ((100*self.vie_monstre)/self.vie_monstre_ref)<=20:
                                self.jaune=False
                                self.color='red'
                                self.rouge=True
                
        def vie(self):
                if liste_ennemi[0]==self.monstre:
                        self.vie_monstre-=1
                        
        def detection(self):
                if len(canvas.find_withtag("zoneT1"))>0:#On test si il y a des hitbox sur le terrain pour ne pas lancer toute la fonction en boucle
                                bbox=canvas.bbox(self.monstre)
                                if bbox is not None: 
                                        xminM,yminM,xmaxM,ymaxM=canvas.bbox(self.monstre) #Coordonnées de l'ennemi
                                        hitbox=canvas.find_overlapping(xminM,yminM,xmaxM,ymaxM) #On regarde quand les coordonnées de l'ennemi entre en collision avec un objet
                                        for i in hitbox:                                                      
                                                tag=canvas.gettags(i) #On chercher le tag de notre hitbox('zoneT1')
                                                if len(tag)>0:
                                                        if tag ==('zoneT1',) or tag==('zoneT1', 'current') : #Si il est present on lance la fonction attaque
                                                                self.vie()
                

                canvas.after(self.vitesse_tir,self.detection)
                       

        
class Tour:
        def __init__(self,niveau,xdepart,ydepart):
                self.xdepart=xdepart
                self.ydepart=ydepart
                self.niveau=niveau
                
                
        def creation(self):
                self.tour1_menu_image= PhotoImage(file="images/tour1_menu.gif")
                self.tour1_image=PhotoImage(file="images/tour1.gif")
                self.tour1_menu=canvas.create_image(self.xdepart,self.ydepart,anchor=NW,image=self.tour1_menu_image)

        def clic(self,event):
                """ Gestion de l'événement Clic gauche """
                global DETECTION_CLIC_SUR_TOUR
                
                # position du pointeur de la souris
                X = event.x
                Y = event.y
                # coordonnées de l'objet
                [xmin,ymin,xmax,ymax] = canvas.bbox(self.tour1_menu)
                
                if xmin<=X<=xmax and ymin<=Y<=ymax:
                        DETECTION_CLIC_SUR_TOUR = True
                        self.cercleT1=canvas.create_oval(X-centre_cercle,Y-centre_cercle,X+centre_cercle,Y+centre_cercle)
                        self.tour1=canvas.create_image(X-centreTour,Y-centreTour,anchor=NW,image=self.tour1_image)

                else:
                        DETECTION_CLIC_SUR_TOUR = False

                

        def drag(self,event):
                """ Gestion de l'événement bouton gauche enfoncé """
                X = event.x
                Y = event.y
                
                if DETECTION_CLIC_SUR_TOUR == True:
                        # limite de l'objet dans la zone graphique
                        if X<centreTour:X=centreTour
                        if X>largeur-centreTour: X=largeur-centreTour
                        if Y<centreTour: Y=centreTour
                        if Y>hauteur-centreTour: Y=hauteur-centreTour
                        # mise à jour de la position de l'objet (drag)
                        canvas.coords(self.tour1,X-centreTour,Y-centreTour)
                        canvas.coords(self.cercleT1,X-centre_cercle,Y-centre_cercle,X+centre_cercle,Y+centre_cercle)

        def case(self,event):
                if DETECTION_CLIC_SUR_TOUR == True:
                        X=event.x
                        Y=event.y

                        self.caseX= X/taille_sprite
                        self.caseY= Y/taille_sprite

                        self.caseX_Arrondi=floor(self.caseX)# arrondi en dessous
                        self.caseY_Arrondi=floor(self.caseY)# arrondi en dessous

                        if self.caseX_Arrondi>spriteX_max:
                                self.caseX_Arrondi=spriteX_max # variable pour ne pas depasser l'ecran
                        if self.caseX_Arrondi<0:
                                self.caseX_Arrondi=0
                        if self.caseY_Arrondi>spriteY_max:
                                self.caseY_Arrondi=spriteY_max # variabale pour ne pas depasser l'ecran
                
                
        def positionnement(self,event):
                if DETECTION_CLIC_SUR_TOUR == True:
                        X=event.x
                        Y=event.y
                        if  Y>=(spriteY_max*taille_sprite):
                                canvas.delete(self.tour1) 
                                canvas.delete(self.cercleT1)
                        if Y<(spriteY_max*taille_sprite):       
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="0" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="d" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="a":
                                        canvas.delete(self.tour1) 
                                        canvas.delete(self.cercleT1)
                                        
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="m":
                                        if [self.caseX_Arrondi,self.caseY_Arrondi] in liste_tour:
                                                canvas.delete(self.tour1) 
                                                canvas.delete(self.cercleT1)
                                                     

                                        else:
                                                canvas.coords(self.tour1,self.caseX_Arrondi*taille_sprite,self.caseY_Arrondi*taille_sprite)
                                                canvas.delete(self.cercleT1)

                                                self.xTour=(self.caseX_Arrondi*taille_sprite)+centreTour
                                                self.yTour=(self.caseY_Arrondi*taille_sprite)+centreTour

                                                self.xminHitboxT1=((self.caseX_Arrondi*taille_sprite)+centreTour)-centre_cercle
                                                self.yminHitboxT1=((self.caseY_Arrondi*taille_sprite)+centreTour)-centre_cercle
                                                self.xmaxHitboxT1=((self.caseX_Arrondi*taille_sprite)+centreTour)+centre_cercle
                                                self.ymaxHitboxT1=((self.caseY_Arrondi*taille_sprite)+centreTour)+centre_cercle

                                                hitboxT1=canvas.create_oval(self.xminHitboxT1,self.yminHitboxT1,self.xmaxHitboxT1,self.ymaxHitboxT1,width=0,fill='',tags="zoneT1")#Creation de la hitbox
                                                self.liste()
                                                
                        
                                      



        def liste(self):
                self.list_case=[self.caseX_Arrondi,self.caseY_Arrondi]
                liste_tour.append(self.list_case)
                
        
class Tour_Argent:
        def __init__(self,niveau,xdepart,ydepart):
                self.xdepart=xdepart
                self.ydepart=ydepart
                self.niveau=niveau
                
                
        def creation(self):
                self.mine_menu_image=PhotoImage(file="images/mine_menu.gif")
                self.mine_menu=canvas.create_image(self.xdepart,self.ydepart,anchor=NW,image=self.mine_menu_image)
                self.mine_image=PhotoImage(file="images/mine.gif")

        def clic(self,event):
                """ Gestion de l'événement Clic gauche """
                global DETECTION_CLIC_SUR_MINE
                
                # position du pointeur de la souris
                X = event.x
                Y = event.y
                # coordonnées de l'objet
                [xmin,ymin,xmax,ymax] = canvas.bbox(self.mine_menu)
                
                if xmin<=X<=xmax and ymin<=Y<=ymax:
                        DETECTION_CLIC_SUR_MINE = True
                        self.mine=canvas.create_image(X-centreTour,Y-centreTour,anchor=NW,image=self.mine_image)

                else:
                        DETECTION_CLIC_SUR_MINE = False

                

        def drag(self,event):
                """ Gestion de l'événement bouton gauche enfoncé """
                X = event.x
                Y = event.y
                
                if DETECTION_CLIC_SUR_MINE == True:
                        # limite de l'objet dans la zone graphique
                        if X<centreTour:X=centreTour
                        if X>largeur-centreTour: X=largeur-centreTour
                        if Y<centreTour: Y=centreTour
                        if Y>hauteur-centreTour: Y=hauteur-centreTour
                        # mise à jour de la position de l'objet (drag)
                        canvas.coords(self.mine,X-centreTour,Y-centreTour)
                        

        def case(self,event):
                X=event.x
                Y=event.y

                caseX= X/taille_sprite
                caseY= Y/taille_sprite

                self.caseX_Arrondi=floor(caseX)# arrondi en dessous
                self.caseY_Arrondi=floor(caseY)# arrondi en dessous

                if self.caseX_Arrondi>spriteX_max:
                        self.caseX_Arrondi=spriteX_max # variable pour ne pas depasser l'ecran
                if self.caseX_Arrondi<0:
                        self.caseX_Arrondi=0
                if self.caseY_Arrondi>spriteY_max:
                        self.caseY_Arrondi=spriteY_max # variabale pour ne pas depasser l'ecran
                
                
        def positionnement(self,event):
                X=event.x
                Y=event.y
                
                if DETECTION_CLIC_SUR_MINE == True:
                        if  Y>=(spriteY_max*taille_sprite):
                                canvas.delete(self.mine) 
                                
                        if Y<(spriteY_max*taille_sprite):       
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="0" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="d" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="a":
                                        canvas.delete(self.mine) 
                                        
                                        
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="m":
                                        if [self.caseX_Arrondi,self.caseY_Arrondi] in liste_tour:
                                                canvas.delete(self.mine) 
                                                
                                                     

                                        else:
                                                canvas.coords(self.mine,self.caseX_Arrondi*taille_sprite,self.caseY_Arrondi*taille_sprite)
                                                
                                                self.liste()
                                                self.prod_argent()
                        
        def liste(self):
                self.list_case=[self.caseX_Arrondi,self.caseY_Arrondi]
                liste_tour.append(self.list_case)                

        
        def prod_argent(self):
                global argent
                if menu_check==False:
                        if Vague==True:
                                argent+=5
                                print("argent",argent)
                                
                        canvas.after(500,self.prod_argent)
                









def b_lancer():
        start()
        vague()




def vague():
        global boucle1,Nb_ennemi,Vague,liste_ennemi
        
        if menu_check==False:
                if scenario==1:
                        if boucle1<Nb_ennemi:
                                mechant=Mechant(niveau,500,30,50)#(niveau,vitesse_deplacement,vie,vitesse_tir)
                                mechant.creation()
                                mechant.deplacement()              
                                Vague=True
                                boucle1+=1
                                
                        if boucle1==Nb_ennemi and len(canvas.find_withtag("monstre1"))==0:
                                start()
                                boucle1=0
                                liste_ennemi=[]
                                Vague=False
                        
                if scenario==4:
                        if boucle1<Nb_ennemi:
                                mechant=Mechant(niveau,500,30,50)#(niveau,vitesse_deplacement,vie,vitesse_tir)
                                mechant.creation()
                                mechant.deplacement()              
                                Vague=True
                                boucle1+=1
                                
                        if boucle1==Nb_ennemi and len(canvas.find_withtag("monstre1"))==0:
                                start()
                                boucle1=0
                                liste_ennemi=[]
                                Vague=False


                canvas.after(1000,vague)                
        

                












def start():
        global scenario
        scenario+=1
        if boucle1==Nb_ennemi and len(canvas.find_withtag("monstre1"))==0:
                scenario+=1

        
                




def clic_gauche(event):
        
        tour.clic(event)
        tour_argent.clic(event)

        def drag(event):
                tour.drag(event)
                tour.case(event)
                tour_argent.drag(event)
                tour_argent.case(event)                               

        def relacher(event):
                tour.positionnement(event)
                tour_argent.positionnement(event)

        canvas.bind('<B1-Motion>',drag) # événement bouton gauche enfoncé (hold down)
        canvas.bind('<ButtonRelease-1>',relacher)


def verif(event):
    saving = messagebox.askokcancel('Quitter ?', 'Êtes-vous certain ?')
    if saving :
        global quitter
        quitter = True
        fenetre.destroy()

        

def quitter_jeu():
    global quitter
    quitter = True
    fenetre.destroy()
    

def menu():
        
        global menu_check,liste_tour,boucle1,scenario,argent,Vague,Nb_ennemi,liste_ennemi
        menu_check=True
        print(liste_tour)
        #Initialisation des varibales 
        liste_tour=[]
        liste_ennemi=[]
        boucle1=0
        scenario=0
        argent=100
        Vague=False
        Nb_ennemi=3
        
        b_lancer.pack_forget()
        b_menu.pack_forget()
        canvas.delete(ALL)

        canvas.create_image(0,0,image=fond, anchor=NW)
        canvas.create_image(900,438, image=titre)

        bouton_jouer.place(x=300,y=600)
        bouton_quitter.place(x=1000,y=600)



def destroy():
        bouton_jouer.place_forget()
        bouton_quitter.place_forget()
        canvas.delete(ALL)


        
def jeu():
        global  menu_check 
        menu_check=False
        destroy()
        niveau.generer()
        niveau.afficher()
        #placé ici pour reset la vie après avoir fermé la fenêtre
        vie_joueur = 5

        tour.creation()
        tour_argent.creation()
        canvas.bind('<Button-1>',clic_gauche)
        compteur_vie = Label (canvas, text="Vies restantes : " +str(vie_joueur), font="bold", fg="red", bg="grey")
        canvas.bind('<Button-1>',clic_gauche)
        canvas.create_window(1200,900,window=compteur_vie)
        b_lancer.pack()       
        b_menu.pack()
       
        if quitter==True :
              quitter_jeu()
        
       

################################################ Variables #########################################################

choix = 'niveaux1'
taille_sprite=60
spriteX_max=24
spriteY_max=13
centreTour=30

largeur=1500
hauteur=960
DETECTION_CLIC_SUR_TOUR = False
DETECTION_CLIC_SUR_MINE= False
centre_cercle=150

Nb_ennemi=3
boucle1=0
scenario=0
Vague=False
liste_ennemi=[]
liste_tour=[]
argent=100

quitter=False
menu_check=True





######## Fenêtre Menu Initialisation ################################################################################
fenetre = Tk()
fenetre.attributes("-fullscreen",1)
fenetre.bind("<Escape>", verif)



        
canvas=Canvas(fenetre, width=1500, height=960,cursor="pirate")
canvas.pack(fill="both",expand=1) 
                       
# image
fond = PhotoImage(file="images/fond menu.gif")
bouton1 = PhotoImage(file = "images/bouton jouer.gif")
bouton2 = PhotoImage(file = "images/bouton quitter.gif")
titre = PhotoImage(file = "images/titre.gif")
#image de fond
canvas.create_image(0,0,image=fond, anchor=NW)
canvas.create_image(900,438, image=titre)


bouton_jouer = Button(canvas,image=bouton1,command=jeu,anchor="ne")
bouton_jouer.place(x=300,y=600)

bouton_quitter = Button(canvas,image=bouton2,command=quitter_jeu,anchor="center")
bouton_quitter.place(x=1000,y=600)                        



b_lancer=Button(fenetre,text="Lancer la vague",command=b_lancer, anchor=S)      
b_menu=Button(fenetre, text="Menu", command=menu,anchor=S)
b_lancer.pack_forget()
b_menu.pack_forget()

niveau = Niveau(choix)

tour=Tour(niveau,80,800)      
tour_argent=Tour_Argent(niveau,300,800)        
        
fenetre.mainloop()

                                                                                                                                                                                                                                                        
