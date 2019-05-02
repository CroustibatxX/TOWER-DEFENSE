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
                self.trol = PhotoImage(file="images/trol.gif")
                
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
                                if liste_ennemi.remove(self.monstre) is not None:
                                        liste_ennemi.remove(self.monstre) 
                                canvas.delete(self.monstre)
                                canvas.delete(self.barre_vie)
                                
                                             

                        if self.case_x < spriteX_max:
                                if niveau.liste[self.case_y][self.case_x+1] == 'a':           
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
                        if ((100*self.vie_monstre)/self.vie_monstre_ref)<=15:
                                self.jaune=False
                                self.color='red'
                                self.rouge=True
                
        def centre(self):
                self.centreX=self.case_x-30
                self.centreY=self.case_y-30
                
        
        def vie(self):
                if liste_ennemi[0]==self.monstre:
                        print(self.vie_monstre)
                        self.vie_monstre-=1
                        print(liste_ennemi)


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
                       

        
class TourBleu:
        def __int__(self,niveau):
                self.color="bleu"
                self.cost=10
                
        
























class Tour:
        def __init__(self,niveau,xdepart,ydepart):
                self.xdepart=xdepart
                self.ydepart=ydepart
                self.niveau=niveau
                self.tour1_menu_image= PhotoImage(file="images/tour1_menu.gif")
                self.tour1_image=PhotoImage(file="images/tour1.gif")
                self.tour1_menu=canvas.create_image(xdepart,ydepart,anchor=NW,image=self.tour1_menu_image)
                self.list_tour=[]
                
                

                #Variable vitesse tir des tours 
                self.vitesse_tir=vitesse_tir

        def clic(self,event):
                """ Gestion de l'événement Clic gauche """
                global DETECTION_CLIC_SUR_OBJET

                # position du pointeur de la souris
                X = event.x
                Y = event.y
                # coordonnées de l'objet
                [xmin,ymin,xmax,ymax] = canvas.bbox(self.tour1_menu)
                
                if xmin<=X<=xmax and ymin<=Y<=ymax:
                        DETECTION_CLIC_SUR_OBJET = True
                        self.cercleT1=canvas.create_oval(X-centre_cercleT1,Y-centre_cercleT1,X+centre_cercleT1,Y+centre_cercleT1)
                        self.tour1=canvas.create_image(X-centreTour1,Y-centreTour1,anchor=NW,image=self.tour1_image)

                else:
                        DETECTION_CLIC_SUR_OBJET = False

                

        def drag(self,event):
                """ Gestion de l'événement bouton gauche enfoncé """
                X = event.x
                Y = event.y
                
                if DETECTION_CLIC_SUR_OBJET == True:
                        # limite de l'objet dans la zone graphique
                        if X<centreTour1:X=centreTour1
                        if X>largeur-centreTour1: X=largeur-centreTour1
                        if Y<centreTour1: Y=centreTour1
                        if Y>hauteur-centreTour1: Y=hauteur-centreTour1
                        # mise à jour de la position de l'objet (drag)
                        canvas.coords(self.tour1,X-centreTour1,Y-centreTour1)
                        canvas.coords(self.cercleT1,X-centre_cercleT1,Y-centre_cercleT1,X+centre_cercleT1,Y+centre_cercleT1)
                        


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
                
                if DETECTION_CLIC_SUR_OBJET == True:
                        if  Y>=(spriteY_max*taille_sprite):
                                canvas.delete(self.tour1) 
                                canvas.delete(self.cercleT1)
                        if Y<(spriteY_max*taille_sprite):       
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="0" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="d" or niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="a":
                                        canvas.delete(self.tour1) 
                                        canvas.delete(self.cercleT1)
                                        
                                if niveau.liste[self.caseY_Arrondi][self.caseX_Arrondi]=="m":
                                        if [self.caseX_Arrondi,self.caseY_Arrondi] in self.list_tour:
                                                canvas.delete(self.tour1) 
                                                canvas.delete(self.cercleT1)
                                                canvas.delete(self.hitboxT1)      

                                        else:
                                                canvas.coords(self.tour1,self.caseX_Arrondi*taille_sprite,self.caseY_Arrondi*taille_sprite)
                                                canvas.delete(self.cercleT1)

                                                self.xTour=(self.caseX_Arrondi*taille_sprite)+centreTour1
                                                self.yTour=(self.caseY_Arrondi*taille_sprite)+centreTour1

                                                self.xminHitboxT1=((self.caseX_Arrondi*taille_sprite)+centreTour1)-centre_cercleT1
                                                self.yminHitboxT1=((self.caseY_Arrondi*taille_sprite)+centreTour1)-centre_cercleT1
                                                self.xmaxHitboxT1=((self.caseX_Arrondi*taille_sprite)+centreTour1)+centre_cercleT1
                                                self.ymaxHitboxT1=((self.caseY_Arrondi*taille_sprite)+centreTour1)+centre_cercleT1

                                                hitboxT1=canvas.create_oval(self.xminHitboxT1,self.yminHitboxT1,self.xmaxHitboxT1,self.ymaxHitboxT1,width=0,fill='',tags="zoneT1")#Creation de la hitbox
                                                self.liste()
                                                
                        
                                      



        def liste(self):
                self.list_case=[self.caseX_Arrondi,self.caseY_Arrondi]
                self.list_tour.append(self.list_case)
                
        def projectile(self):
                self.xminTir=(self.caseX_Arrondi*taille_sprite)+25
                self.yminTir=(self.caseY_Arrondi*taille_sprite)+25
                self.xmaxTir=(self.caseX_Arrondi*taille_sprite)+35
                self.ymaxTir=(self.caseY_Arrondi*taille_sprite)+35

                self.tir=canvas.create_oval(self.xminTir,self.yminTir,self.xmaxTir,self.ymaxTir,fill='red')
                self.deplacement_projectile()

        def deplacement_projectile(self):
               if self.xminTir!=centrex or self.yminTir!=centrey:
                       canvas.coords(self.tir,self.xminTir+10,self.yminTir+10,self.xmaxTir+10,self.ymaxTir+10)
                       canvas.after(100,self.projectile)
                

        
                       


        
                


        def distance(self):
                d_ennemi=sqrt((self.yTour-mechant.centreY)^2+(self.xTour-mechant.centreX)^2)
                







def vie(mechant):
        mechant.centre()
        mechant.vie()







def vague():
        global a,Nb_ennemi,scenario,Vague,liste_ennemi
        
        if a<Nb_ennemi:
                mechant=Mechant(niveau,500,5,1000)#(niveau,vitesse_deplacement,vie,vitesse_tir)
                mechant.creation()
                mechant.deplacement()              
                Vague=True
                a+=1
                canvas.after(700,vague)
                
        if a==Nb_ennemi and len(canvas.find_withtag("monstre1"))==0:
                a=0
                liste_ennemi=[]
                
        
                

def temporaire():
                mechant=Mechant(niveau,2000,3)
                mechant.creation()
                mechant.deplacement()
                mechant.detection()

def clic_gauche(event):
        tour.clic(event)
        def drag(event):
                tour.drag(event)
                tour.case(event)                               

        def relacher(event):
                tour.positionnement(event)
                
        canvas.bind('<B1-Motion>',drag) # événement bouton gauche enfoncé (hold down)
        canvas.bind('<ButtonRelease-1>',relacher)


################################################ Variables #########################################################

choix = 'niveaux1'
taille_sprite=60
spriteX_max=24
spriteY_max=13
centreTour1=30
tailleCercle1=170
largeur=1500
hauteur=960
DETECTION_CLIC_SUR_OBJET = False
vitesse_tir=500
centre_cercleT1=150
Nb_ennemi=3
a=0
scenario=0
Vague=True
liste_ennemi=[]
centrex=1400
centrey=500


############################################## Principal ##########################################################

fenetre=Tk()
fenetre.attributes('-fullscreen', 1)





canvas = Canvas(fenetre, width=largeur, height=hauteur)

canvas.pack()
                                                                                                                                                                                                                                                               



niveau = Niveau(choix)
niveau.generer()
niveau.afficher()


tour=Tour(niveau,80,800)

canvas.bind('<Button-1>',clic_gauche) # évévement clic gauche (press)




Button(fenetre,text="LANCER",command=vague,anchor=S).pack()       
Button(fenetre, text="Quitter", command=fenetre.destroy,anchor=S).pack()



fenetre.mainloop()    

