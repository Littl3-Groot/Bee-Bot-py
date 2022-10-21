# THOREL LELIAN TG6
import pygame
from pygame import*
from pygame.gfxdraw import*
import random
from random import *
import time
from time import *

def couleur_random():
    couleur = (randint(0,255),randint(0,255),randint(0,255))
    return couleur

def dessine_carre(coord_centre,longueur_cote,couleur):
    box(fenetre,(coord_centre[0]-longueur_cote/2,coord_centre[1]-longueur_cote/2,longueur_cote,longueur_cote),couleur_random())
    #print(coord_centre)
    display.flip()

pygame.init()
largeur = 600
hauteur = 600
fenetre = display.set_mode((largeur,hauteur))
display.set_caption("fractale")
fenetre.fill((255,255,255))
display.flip()

centre_carre = (300,300)
longueur_cote = 300
couleur = (randint(0,255),randint(0,255),randint(0,255))
p = (300,300)

opération =((1, -1), (1, 1), (-1, 1), (-1, -1)) # équivalent de +- ++ -+ -- puisque -1 * 5 = -5
#donc centre_carre[0]+opération[i][0]*longueur_cote/2 = centre_carre[0]+longueur_cote/2)

continuer = 1
while continuer:
    while longueur_cote > 1:


        for i in range (4):

            dessine_carre(p,longueur_cote,couleur)
            sleep(0.1)

            p = (centre_carre[0]+opération[i][0]*longueur_cote,centre_carre[1]+opération[i][1]*longueur_cote)
            print(centre_carre[0], centre_carre[1])

            longueur_cote = 300/2



    #centre_carre = (150,450) # pour boucler à l'infini et faire un truc stylé
    #longueur_cote = 300

    for event in pygame.event.get():

        if event.type in (QUIT,KEYDOWN):
            pygame.quit()
            continuer = 0