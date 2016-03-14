# Créé par Allan Dandrieux, Guillaume Roux, Xavier Debiran le 15/03/2015 en Python 3.2

# Importation des ressources de pygame.
import pygame, random, time
from pygame.locals import *


# Réinitialisatiion de tous les modules.
pygame.init()

#variables sons et images
pygame.mixer.music.load("Jazz.wav")
game_over = pygame.mixer.Sound("game_over.wav")
miam_son = pygame.mixer.Sound("miam.wav")
fenetre = pygame.display.set_mode((900, 650))
serpent2 = pygame.image.load("snake2.png")
serpimage = pygame.image.load("snake icon.png")
serpent = pygame.image.load("snake2.png")
serpent_mort = pygame.image.load("snake_mort.png")

# Déclaration de la variable "fenetre" ainsi que de sa largeur et sa hauteur.
fond = pygame.image.load("fond snake.png").convert()
fenetre.blit(fond,(0,0))

pygame.display.set_caption('Snake des Mousquetaires')
pygame.display.set_icon(serpimage)

# Définition des variables couleurs
black = (0,0,0)
red = (200,0,0)
white = (255,255,255)
green = (0,200,0)
rouge_surligne = (255,0,0)
vert_surligne = (0,255,0)
jaune_surligne = (255,255,0)
gray = (200, 200, 200)
gold = (239,216,7)

crashed = False
clock = pygame.time.Clock()
pause = False


# On definit les fonctions
class Jeu(pygame.sprite.Sprite):
    def __init__(self, width = 900, height = 650):
        pygame.sprite.Sprite.__init__(self)
        pygame.init()

        self.horloge = pygame.time.Clock()
        self.width   = width
        self.height  = height
        self.vitesse = 20

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fond = pygame.image.load("fond snake.png").convert()
        self.screen.blit(self.fond,(0,0))
        pygame.display.set_caption("Snake des Mousquetaires")

        self.cerise   = Cerise()
        self.perso   = Perso()
        self.bloc    = Bloc()
        self.limiteh  = Limiteh()
        self.limited = Limited()
        self.limiteg = Limiteg()
        self.limiteb = Limiteb()

        self.g_perso = pygame.sprite.Group(self.perso)
        self.g_cerise = pygame.sprite.GroupSingle(self.cerise)
        self.g_bloc  = pygame.sprite.Group(self.bloc)
        self.g_limiteh = pygame.sprite.Group(self.limiteh)
        self.g_limited = pygame.sprite.Group(self.limited)
        self.g_limiteg = pygame.sprite.Group(self.limiteg)
        self.g_limiteb = pygame.sprite.Group(self.limiteb)


    def mainloop(self):
        global pause
        continuer = True
        self.m = "D"
        score = 0
        while continuer:
            self.horloge.tick(8)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.m = "H"
                        self.perso.image = self.perso.persoH
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        paused()
                    elif event.key == pygame.K_DOWN:
                        self.m = "B"
                        self.perso.image = self.perso.persoB
                    elif event.key == pygame.K_RIGHT:
                        self.m = "D"
                        self.perso.image = self.perso.persoD
                    elif event.key == pygame.K_LEFT:
                        self.m = "G"
                        self.perso.image = self.perso.persoG


            #Ici on bouge le snake en fonction de /self.m/
            if not self.perso.rect.colliderect(self.limiteh.rect):
                ancienRect = self.perso.rect.topleft
                if self.m == "H":
                    self.perso.rect.move_ip(0, -self.vitesse)
                    for i in self.g_bloc:
                        #Echange de coordonnées
                        i.rect.topleft, ancienRect  = ancienRect, i.rect.topleft
                elif self.m == "B":
                    self.perso.rect.move_ip(0, self.vitesse)
                    for i in self.g_bloc:
                        #Echange de coordonnées
                        i.rect.topleft, ancienRect  = ancienRect, i.rect.topleft
                elif self.m == "D":
                    self.perso.rect.move_ip(self.vitesse , 0)
                    for i in self.g_bloc:
                        #Echange de coordonnées
                        i.rect.topleft, ancienRect  = ancienRect, i.rect.topleft
                elif self.m == "G":
                    self.perso.rect.move_ip(-self.vitesse, 0)
                    for i in self.g_bloc:
                        #Echange de coordonnées
                        i.rect.topleft, ancienRect  = ancienRect, i.rect.topleft

            else: #Si collision on fait apparaîte menu de fin
                self.drawBlitFill()
                crash()
                game_fin()
                return

            if self.perso.rect.colliderect(self.limited.rect):
                self.drawBlitFill()
                crash()
                game_fin()
                return

            elif self.perso.rect.colliderect(self.limiteb.rect):
                self.drawBlitFill()
                crash()
                game_fin()
                return

            elif self.perso.rect.colliderect(self.limiteg.rect):
                self.drawBlitFill()
                crash()
                game_fin()
                return


            #Si collision avec une cerise, on en génère & blit une autre et on ajoute un bloc

            scores(score)   #appelle fct scores
            if self.perso.rect.colliderect(self.cerise.rect):

                self.cerise.genererCerise(self.width, self.height)
                self.g_cerise.add(self.cerise)

                self.bloc = Bloc()
                self.g_bloc.add(self.bloc)
                score += 1  #chaque fois que le serpent mange une cerise augemente score de 1

                pygame.mixer.Sound.play(miam_son)   #chaque fois que le serpent mange une cerise un son ce produit


            #On blit tout les groupes d'un coup + flip + fill
            self.drawBlitFill()


    def drawBlitFill(self):
        self.g_perso.draw(self.screen)
        self.g_cerise.draw(self.screen)
        self.g_bloc.draw(self.screen)
        self.g_limiteh.draw(self.screen)
        self.g_limited.draw(self.screen)
        self.g_limiteg.draw(self.screen)
        self.g_limiteb.draw(self.screen)
        pygame.display.flip()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.fond,(0,0))



#-*-*- <Les Classes> || Début de <Perso> -*-*-#

class Perso(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #Chargement des images
        self.persoB = pygame.image.load("sprite snake bas.png")
        self.persoH = pygame.image.load("sprite snake haut.png")
        self.persoD = pygame.image.load("sprite snake droite.png")
        self.persoG = pygame.image.load("sprite snake gauche.png")

        #Gestion du contour blanc
        self.persoB.set_colorkey((255, 255, 255))
        self.persoH.set_colorkey((255, 255, 255))
        self.persoD.set_colorkey((255, 255, 255))
        self.persoG.set_colorkey((255, 255, 255))

        #Il faut une imageActuelle car il y a 4 têtes diférentes
        self.image = self.persoD
        self.rect = self.image.get_rect()
        self.rect.center = (450, 325)




class Bloc(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("corps snake.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (-60,-60)


class Cerise(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image fruit.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

    def genererCerise(self, width, height):#Genère une cerise aléatoirement
        self.rect.topleft = (random.randrange(70, width-70), \
                             random.randrange(70, height-70))


#-*-*- <Les Classes> || Début de <Mur> -*-*-#


class Limiteh (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ligne bloc.png")
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.topleft = (0, 0)

class Limited (pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("colonne bloc.png")
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.topleft = (850, 0)

class Limiteg (pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("colonne bloc.png")
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.topleft = (0, 0)

class Limiteb (pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ligne bloc.png")
        self.rect = self.image.get_rect()
        self.image.set_colorkey((255, 255, 255))
        self.rect.topleft = (0, 600)



# lance le jeu
def game():
    pygame.mixer.music.play(-1) #joue la musique de fond en boucle
    if __name__ == "__main__":
        partie = Jeu()
        partie.mainloop()


#ecriture en rouge dans une position precise
def text_objects(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()
#ecriture en noire dans une position precise
def text_objet(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
#fct bouton
def bouton(msg,x,y,w,h,ic,ac,action=None):           #msg= ce qui est écrit dessus ; x=abscisse; y=ordonnée, w=epaisseur, h=hauteur, ic=couleur quand souris pas sur rectangle, ac=couleur quand souris sur rectangle, action= ce que va faire qaund on clique dessus
     mouse = pygame.mouse.get_pos()                  #reconnait position de la souris
     clique = pygame.mouse.get_pressed()            #reconnait quand on clique

     if x+w > mouse[0] > x  and y+h > mouse[1] > y: #quand la souris est dans le rectangle et que l'on clique dessus elle produit l'action
        pygame.draw.rect(fenetre, ac, (x,y,w,h))
        if clique[0] == 1 and action != None :
            action()

     else:
        pygame.draw.rect(fenetre, ic, (x,y,w,h))

     smallText = pygame.font.SysFont("Arial",30)
     textSurf, textRect = text_objet(msg, smallText)
     textRect.center = ((x+(w/2)), (y+(h/2)))
     fenetre.blit(textSurf, textRect)


def quitgame(): #quitter le jeu
    pygame.quit()
    quit()

def message_display(text):  # message apparait (voir game over)
    pygame.mixer.Sound.play(game_over)
    largeText = pygame.font.SysFont("Arial",115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((900/2),(650/2))
    fenetre.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(4)

def unpaused(): # enlever la pause
    global pause
    pygame.mixer.music.unpause()
    pause = False


def scores(count):  #fonction score
    font = pygame.font.SysFont(None,40)
    text = font.render("Score: "+str(count),True, rouge_surligne)
    fenetre.blit(text,(400,65))


def paused():   #fonction pause

    pygame.mixer.music.pause()  #met music en pause

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpaused()

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        fenetre.blit(fond,(0,0))    #Affiche le fond
        largeText = pygame.font.SysFont("Arial",130)
        TextSurf, TextRect = text_objects("EN PAUSE", largeText)# on écrit EN PAUSE en police arial en 130 (voir largeText)
        TextRect.center =((900/2),(650/2)) #on le met au centre
        fenetre.blit(TextSurf, TextRect)

        bouton("CONTINUER",30,580/2,150,80,green,vert_surligne,unpaused)  #Fais appel à la fct bouton pour Continuer
        bouton("MENU",370,150,150,80,gold,jaune_surligne,game_intro)
        bouton("QUITTER",720,580/2,150,80,red,rouge_surligne,quitgame) #Fais appel à la fct bouton pour quitter

        pygame.display.update()
# Menu
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        fenetre.blit(serpent2,(0,0))        #Affiche le fond
        largeText = pygame.font.SysFont("Arial",130)
        TextSurf, TextRect = text_objet("Snake", largeText)# on écrit Snake en police arial en 130 (voir largeText)
        TextRect.center =((700),(50)) # on le met à la position x=700 et y = 50
        fenetre.blit(TextSurf, TextRect)

        bouton("JOUER",620,120,150,80,green,vert_surligne,game)  #Fais appel à la fct bouton pour Jouer
        bouton("QUITTER",620,220,150,80,red,rouge_surligne,quitgame) #Fais appel à la fct bouton pour quitter

        pygame.display.update()



#Affiche Rejouer et quitter apres le game over
def game_fin():
     while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        fenetre.blit(serpent_mort,(0,0))    #Affiche le fond
        bouton("REJOUER",220,120,150,80,white,gray,game)#game=lancer le jeu sans le menu
        bouton("QUITTER",620,120,150,80,white,gray,quitgame) #quitgame=Fais appel à la fct bouton pour quitter
        pygame.display.update()


#Affiche le GAME OVER quand le serpent touche un mur ou lui meme
def crash():
    pygame.mixer.music.stop() #stop la musique
    message_display('GAME OVER') #fait appelle fct message_display et fais apparaitre GAME OVER
    pygame.display.flip()

# On lance le menu donc le jeu.
game_intro()


# Pour pouvoir fermer la fenetre sans que Pygame freeze.
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True


    pygame.display.update()

    clock.tick(30)
pygame.quit()
quit()
