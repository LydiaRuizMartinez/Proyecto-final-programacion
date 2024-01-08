import pygame 
from pygame.locals import *
from constantes import *
import funciones as f
import clases as c

if __name__ == "__main__":

    pygame.init()
    
    screen = pygame.display.set_mode(DIMENSION)
    pygame.display.set_caption("Menú principal")

    menuBg = pygame.image.load("menuBg.png").convert_alpha()

    myfont = pygame.font.SysFont('Lucida Console', 20)

    first = True
    fullscreen = False
    msg_s = True
    first = True
    enterName_s = False

    f.playMusic("main")
    f.menu()

    pygame.quit()