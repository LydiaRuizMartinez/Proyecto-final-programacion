import pygame
from constantes import *

class button():
    def __init__(self, color, x, y, width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            myfont = pygame.font.SysFont('Lucida Console', 20)
            text = myfont.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = pygame.mouse.get_pos()
        if self.isOver(pos):
            self.color = BLANCO
        else:
            self.color = GRIS

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
                
        return False    

class InputBox:
    
    COLOR_INACTIVE = NEGRO
    COLOR_ACTIVE = BLANCO

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        myfont = pygame.font.SysFont('Lucida Console', 20)
        self.txt_surface = myfont.render(text, True, NEGRO)
        self.active = False

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                myfont = pygame.font.SysFont('Lucida Console', 20)
                self.txt_surface = myfont.render(self.text, True, self.color)
                
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2) 