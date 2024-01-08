import random
import pygame
import clases as c
from constantes import *
import time
from collections import deque
import sys
import pickle

def print_text(screen, font, x:int, y:int, text:str, fcolor=(255, 255, 255)) -> None:

    """ Esta función imprime texto en la pantalla.
    Args:
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        font: tipo de fuente
        x(int): posición en x
        y(int): posición en y
        text(str): texto
        fcolor: color del texto (por defecto es blanco)
    Returns:
        None
    """

    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def crear_serpiente(serpiente:deque, alcance:int) -> None:

    """ Esta función crea la serpiente de 3 cuadrados de longitud.
    Args:
        serpiente(deque): similar a una lista
        alcance(int): posición
    Returns:
        None
    """

    serpiente.clear()
    serpiente.append((2, alcance))
    serpiente.append((1, alcance))
    serpiente.append((0, alcance))

def crear_comida(serpiente:deque, alcance_x:tuple, alcance_y:tuple) -> int:

    """ Esta función crea la posición en la que se encuentra la comida de la serpiente.
    Args:
        serpiente(deque): similar a una lista
        alcance_x(tuple) = (0, ANCHO_PANTALLA // SIZE - 1)
        alcance_y(tuple) = (2, ALTO_PANTALLA // SIZE - 1)
    Returns:
        int: dos números enteros que indican las posiciones en los ejes x e y
    """

    x = random.randint(alcance_x[0], alcance_x[1])
    y = random.randint(alcance_y[0], alcance_y[1])

    while (x,y) in serpiente:
        x = random.randint(alcance_x[0], alcance_x[1])
        y = random.randint(alcance_y[0], alcance_y[1])

    return x,y

def mainLoop() -> None:

    """ Esta función actualiza la pantalla.
    Args:
        None
    Returns:
        None
    """

    global mainLoop_s, first, fullscreen, DIMENSION

    while mainLoop_s:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop_s = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            playMusic("main")
            changescn("menu")
        
        pygame.display.flip()

def changescn(scn:str, text="", btnfnc="") -> None:

    """ Esta función cambia los escenarios.
    Args:
        scn(str): escenario
        text=""
        btnfnc=""
    Returns:
        None
    """
    
    global menu_s, enterName_s, mainLoop_s, instructions_s, msg_s, scores_s, music_s, minijuego_s, gameover_s 
    menu_s = enterName_s = mainLoop_s = instructions_s = msg_s = scores_s = music_s = minijuego_s = gameover_s = False
    
    if scn == "menu":
        menu_s = True
        menu()
    
    elif scn == "enterName":
        enterName_s = True
        enterName()

    elif scn == "minijuego":
        minijuego_s = True
        minijuego()        

    elif scn == "music":
        music_s = True
        music()

    elif scn == "gameover":
        gameover_s = True
        gameover()

    elif scn == "mainLoop":
        mainLoop_s = True
        mainLoop()
        
    elif scn == "instructions":
        instructions_s = True
        instructions()
        
    elif scn == "msg":
        msg_s = True
        msg(text,btnfnc)
        
    elif scn == "scores":
        scores_s = True
        scores()

def msg(text:str,btnfnc:str) -> None:

    """ Esta función cambio de pantalla.
    Args:
        text(str)
        btnfnc(str)
    Returns:
        None
    """
    
    global msg_s, first
    
    msgOkBtn = c.button(GRIS, ANCHO_PANTALLA/2 - 100, ALTO_PANTALLA/2, 200, 25, "ok")
    label = pygame.font.SysFont('Lucida Console', 30).render(text, 1, NEGRO)
    
    if text == "Game Over!":
        first = True
        
    while msg_s:
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.fill(MORADO)
        screen.blit(label, (ANCHO_PANTALLA/2 - label.get_width()/2, ALTO_PANTALLA/2 - label.get_height()/2 - 50))
        msgOkBtn.draw(screen, NEGRO)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type==pygame.QUIT:
                msg_s = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if msgOkBtn.isOver(pos):
                    if text == "Game Over!":
                        playMusic("main")
    
                    changescn(btnfnc)
                    
            if event.type == pygame.KEYDOWN:
                                
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)

def playMusic(music:str) -> None:

    """ Esta función hace que suene la música y se pare.
    Args:
        music(str): música asociada a ese nombre ("main": la canción suena o "stop": la canción para)
    Returns:
        None
    """

    if music == "main":
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)
        
    elif music == "stop":
        pygame.mixer.music.stop()

def principal() -> None:

    """ Esta función realiza el juego principal (el de la serpiente).
    Args:
        None
    Returns:
        None
    """

    global score

    screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption ('Python Snake')
    
    fuente1 = pygame.font.SysFont ('Lucida Console', 18, bold = True) 

    color_serpiente = 0   

    pos_x = 1
    pos_y = 0

    
    alcance_x = (0, ANCHO_PANTALLA // SIZE - 1)
    alcance_y = (2, ALTO_PANTALLA // SIZE - 1)
    
    serpiente = deque()   # Similar a una lista
    crear_serpiente(serpiente,alcance_y[0])

    comida_x,comida_y = crear_comida(serpiente,alcance_x,alcance_y)   
 
    game_over = True
    start = False 
    v_o = 0.5  
    velocidad = v_o
    hora_ultimo_mvto = None   
    stop = False 
    juego = True

    while juego:
        for event in pygame.event.get():   # Comprobamos la lista con los posibles eventos sucedidos
            if event.type == pygame.QUIT:
                juego = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        crear_serpiente(serpiente,alcance_y[0])
                        comida_x,comida_y = crear_comida(serpiente,alcance_x,alcance_y)
                        pos_x = 1
                        pos_y = 0  
                        hora_ultimo_mvto = time.time()
                elif event.key == pygame.K_SPACE:
                    if not game_over:
                        stop = not stop
                elif event.key in (pygame.K_w, pygame.K_UP):                 
                    if not pos_y:
                        pos_x = 0
                        pos_y = -1   
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    if not pos_y:
                        pos_x = 0
                        pos_y = 1  
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    if not pos_x:
                        pos_x = -1 
                        pos_y = 0
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    if not pos_x:
                        pos_x = 1   
                        pos_y = 0

        screen.fill(VERDE_CLARO)  
        pygame.draw.rect(screen, MORADO, (0,0, ANCHO_PANTALLA,40))

        for x in range(SIZE, ANCHO_PANTALLA, SIZE):  
            pygame.draw.line(screen, VERDE_OSCURO, (x, alcance_y[0] * SIZE), (x, ALTO_PANTALLA), 2)
        for y in range(alcance_y[0] * SIZE, ALTO_PANTALLA, SIZE): 
            pygame.draw.line(screen, VERDE_OSCURO, (0, y), (ANCHO_PANTALLA, y), 2)
        
        if game_over:
            if start:
                changescn("minijuego")
                
        else:
            hora_actual = time.time()
            if hora_actual - hora_ultimo_mvto > velocidad:
                if not stop:
                    hora_ultimo_mvto = hora_actual
                    siguiente_mvto = (serpiente[0][0] + pos_x, serpiente[0][1] + pos_y)
                    if siguiente_mvto[0] == comida_x and siguiente_mvto[1] == comida_y:
                        comida_x,comida_y = crear_comida(serpiente,alcance_x,alcance_y)
                        serpiente.appendleft(siguiente_mvto)
                        score += 100
                        color_serpiente +=1
                        if color_serpiente > 3:
                            color_serpiente = 0
                        velocidad = v_o - 0.0004 * score 
                    else:
                        if alcance_x[0] <= siguiente_mvto[0] <= alcance_x[1] and alcance_y[0] <= siguiente_mvto[1] <= alcance_y[1] \
                                and siguiente_mvto not in serpiente:
                            serpiente.appendleft(siguiente_mvto)
                            serpiente.pop()
                        else:
                            game_over = True
 
        if not game_over:
            pygame.draw.rect(screen, CLARO, (comida_x * SIZE, comida_y * SIZE, SIZE, SIZE), 0)
 
        for cuadro in serpiente:
            if color_serpiente == 0:
                pygame.draw.rect(screen, FUCSIA, (cuadro[0] * SIZE + ANCHO_CUADRICULA, cuadro[1] * SIZE + ANCHO_CUADRICULA,
                                                SIZE - ANCHO_CUADRICULA * 2, SIZE - ANCHO_CUADRICULA * 2), 0)
            elif color_serpiente == 1:
                pygame.draw.rect(screen, AZUL, (cuadro[0] * SIZE + ANCHO_CUADRICULA, cuadro[1] * SIZE + ANCHO_CUADRICULA,
                                                SIZE - ANCHO_CUADRICULA * 2, SIZE - ANCHO_CUADRICULA * 2), 0)
            elif color_serpiente == 2:
                pygame.draw.rect(screen, NARANJA, (cuadro[0] * SIZE + ANCHO_CUADRICULA, cuadro[1] * SIZE + ANCHO_CUADRICULA,
                                                SIZE - ANCHO_CUADRICULA * 2, SIZE - ANCHO_CUADRICULA * 2), 0)
            elif color_serpiente == 3:
                pygame.draw.rect(screen, BLANCO, (cuadro[0] * SIZE + ANCHO_CUADRICULA, cuadro[1] * SIZE + ANCHO_CUADRICULA,
                                                SIZE - ANCHO_CUADRICULA * 2, SIZE - ANCHO_CUADRICULA * 2), 0)
    
            print_text (screen, fuente1, 30, 7, f'Username: {username} ')
            print_text (screen, fuente1, 450, 7, f'Score: {score} ')
 
        pygame.display.update()

def menu() -> None:

    """ Esta función muestra el menú principal.
    Args:
        None
    Returns:
        None
    """
    
    global menu_s, firts, score_dict

    try:
        score_dict = leer_marcador()
    except:
        score_dict = dict()
        
    playBtn = c.button(GRIS, 200, 240, 200, 25, "PLAY")
    scoresBtn = c.button(GRIS, 200, 270, 200, 25, "LEADERBOARD")
    instBtn = c.button(GRIS, 200, 300, 200, 25, "INSTRUCTIONS")
    musicBtn = c.button(GRIS, 200, 330, 200, 25, "MUSIC")
    exitBtn = c.button(GRIS, 200, 360, 200, 25, "EXIT")
    backBtn = c.button(GRIS, 350, 400, 200, 25, "Back")

    while menu_s:
        
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        menuBg = pygame.image.load("menuBg.png").convert_alpha()   # Fondo del menú
        screen.blit(menuBg, (0, 0))
        playBtn.draw(screen, (0,0,0))
        scoresBtn.draw(screen, (0,0,0))
        instBtn.draw(screen, (0,0,0))
        musicBtn.draw(screen, (0,0,0))
        exitBtn.draw(screen, (0,0,0))

        if first == False:
        
            backBtn.draw(screen, (0,0,0))
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # toma la posicion del mouse
 
            if event.type == pygame.QUIT:
                menu_s = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if playBtn.isOver(pos):         
                    changescn("enterName")
                
                if instBtn.isOver(pos):
                    changescn("instructions")
                
                if musicBtn.isOver(pos):
                    changescn("music")
                
                if exitBtn.isOver(pos):
                    menu_s = False
                    sys.exit()
                    
                if backBtn.isOver(pos):
                    changescn("mainLoop")
                    
                if scoresBtn.isOver(pos):
                    changescn("scores")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False
                    
        pygame.display.flip()

def scores() -> None:

    """ Esta función muestra en el leaderboard las puntuaciones de los 10 mejores en orden decreciente.
    Args:
        None
    Returns:
        None
    """

    tag = "NAME".ljust(10) + "SCORE".center(10) 
    
    jugadores = len(score_dict)

    sorted_score_dict = dict(sorted(score_dict.items(), key=lambda item:item[1],reverse=True))
    nombre = list(sorted_score_dict)

    if jugadores > 0:
        place0 = str(nombre[0]).ljust(10) + str(sorted_score_dict.get(nombre[0])).center(10)
    else:
        place0 = "---"
    
    if jugadores > 1:
        place1 = str(nombre[1]).ljust(10) + str(sorted_score_dict.get(nombre[1])).center(10)
    else:
        place1 = "---"

    if jugadores > 2:
        place2 = str(nombre[2]).ljust(10) + str(sorted_score_dict.get(nombre[2])).center(10)
    else:
        place2 = "---"
        
    if jugadores > 3:
        place3 = str(nombre[3]).ljust(10) + str(sorted_score_dict.get(nombre[3])).center(10)
    else:
        place3 = "---"
        
    if jugadores > 4:
        place4 = str(nombre[4]).ljust(10) + str(sorted_score_dict.get(nombre[4])).center(10)
    else:
        place4 = "---"
        
    if jugadores > 5:
        place5 = str(nombre[5]).ljust(10) + str(sorted_score_dict.get(nombre[5])).center(10)
    else:
        place5 = "---"

    if jugadores > 6:
        place6 = str(nombre[6]).ljust(10) + str(sorted_score_dict.get(nombre[6])).center(10)
    else:
        place6 = "---"  

    if jugadores > 7:
        place7 = str(nombre[7]).ljust(10) + str(sorted_score_dict.get(nombre[7])).center(10)
    else:
        place7 = "---"
        
    if jugadores > 8:
        place8 = str(nombre[8]).ljust(10) + str(sorted_score_dict.get(nombre[8])).center(10)
    else:
        place8 = "---"

    if jugadores > 9:
        place9 = str(nombre[9]).ljust(10) + str(sorted_score_dict.get(nombre[9])).center(10)
    else:
        place9 = "---"

    scoresBack = c.button(GRIS, 50, 435, 200, 25, "Back")
    scoresClear = c.button(GRIS, 350, 435, 200, 25, "Clear Score")

    myfont = pygame.font.SysFont('Lucida Console', 20)
    scoresTitle = myfont.render("SCORES - TOP10", 1, BLANCO)

    tag2 = myfont.render(tag, 1, BLANCO)
    score0 = myfont.render(place0, 1, BLANCO)
    score1 = myfont.render(place1, 1, BLANCO)
    score2 = myfont.render(place2, 1, BLANCO)
    score3 = myfont.render(place3, 1, BLANCO)
    score4 = myfont.render(place4, 1, BLANCO)
    score5 = myfont.render(place5, 1, BLANCO)
    score6 = myfont.render(place6, 1, BLANCO)
    score7 = myfont.render(place7, 1, BLANCO)
    score8 = myfont.render(place8, 1, BLANCO)
    score9 = myfont.render(place9, 1, BLANCO)

    global scores_s
    
    while scores_s:
        
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.fill(MORADO)
        
        pygame.draw.rect(screen,NEGRO,(25,20,550,400))
        
        screen.blit(scoresTitle, (30, 30))
        screen.blit(tag2, (30, 80))
        screen.blit(score0, (30, 120))
        screen.blit(score1, (30, 150))
        screen.blit(score2, (30, 180))
        screen.blit(score3, (30, 210))
        screen.blit(score4, (30, 240))
        screen.blit(score5, (30, 270))
        screen.blit(score6, (30, 300))
        screen.blit(score7, (30, 330))
        screen.blit(score8, (30, 360))
        screen.blit(score9, (30, 390))
        
        scoresBack.draw(screen, (0,0,0))
        scoresClear.draw(screen, (0,0,0))
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
 
            if event.type == pygame.QUIT:
                scores_s = False
                sys.exit()
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

            if event.type == pygame.MOUSEBUTTONDOWN:          
                if scoresBack.isOver(pos):
                    changescn("menu")
                    
                elif scoresClear.isOver(pos):
                    clearScores()

        pygame.display.flip()
        
def clearScores() -> None:

    """ Esta función elimina las puntuaciones del leaderboard.
    Args:
        None
    Returns:
        None
    """

    score_dict.clear()
    guardar_marcador(score_dict)
    changescn("scores")

def instructions() -> None:
    
    """ Esta función muestra las instrucciones.
    Args:
        None
    Returns:
        None
    """

    global instructions_s
    
    backBtn = c.button(GRIS, 350, 435, 200, 25, "Back")
    myfont = pygame.font.SysFont('Lucida Console', 20)
    myfont1 = pygame.font.SysFont('Lucida Console',14)
    label0 = myfont.render("INSTRUCTIONS:", 1, BLANCO)
    label1 = myfont1.render("- Press the enter key to make the snake start moving", 1, BLANCO)
    label2 = myfont1.render("- To change direction, use the w, a, s, d or direction keys", 1, BLANCO)
    label3 = myfont1.render("- Your goal is to eat the gray squares", 1, BLANCO)
    label4 = myfont1.render("- If you crash, another game will appear allowing you to continue ", 1, BLANCO)
    label5 = myfont1.render("playing if you hit it. Combine the six figures in such a way that,", 1, BLANCO)
    label6 = myfont1.render("using +, - and *, you get the number you need to reach", 1, BLANCO)

    while instructions_s:
        
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.fill(MORADO)
        
        pygame.draw.rect(screen,NEGRO,(25,20,550,400))
        
        screen.blit(label0, (30, 30))
        screen.blit(label1, (30, 80))
        screen.blit(label2, (30, 120))
        screen.blit(label3, (30, 160))
        screen.blit(label4, (30, 200))
        screen.blit(label5, (30, 220))
        screen.blit(label6, (30, 240))

        backBtn.draw(screen, (0,0,0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                instructions_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")


def enterName() -> None:

    """ Esta función sirve para introducir el nombre.
    Args:
        None
    Returns:
        None
    """

    global enterName_s, user_text, first, username, score
    
    enterOkBtn = c.button(GRIS, 200, 350, 200, 25, "OK")
    enterBackBtn = c.button(GRIS, 350, 400, 200, 25, "Back")
    myfont = pygame.font.SysFont('Lucida Console', 20)
    labelEnterName = myfont.render("Enter your username:", 1, BLANCO)
    input_box1 = c.InputBox(200, 300, 140, 32)  

    while enterName_s:
        
        menuBg = pygame.image.load("menuBg.png").convert_alpha()   # Fondo del menú
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.blit(menuBg, (0, 0)) 
        enterOkBtn.draw(screen, (0,0,0)) 
        enterBackBtn.draw(screen, (0,0,0))

        screen.blit(labelEnterName, (180, 270))  
        
        input_box1.update()
        input_box1.draw(screen) 
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box1.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if enterOkBtn.isOver(pos):
                    
                    if input_box1.text == "":
                        changescn("msg", text="You have to enter name", btnfnc="enterName")
                            
                    else:
                        username = str(input_box1.text)
                        score = 0
                        principal()
                        changescn("mainLoop")
         
                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                enterName_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
                    
        pygame.display.flip()

def minijuego() -> None:

    """ Esta función realiza el segundo juego, el de las cifras.
    Args:
        None
    Returns:
        None
    """

    global minijuego_s, user_text, first
    
    enterOkBtn = c.button(GRIS, 200, 350, 200, 25, "OK")
    enterBackBtn = c.button(GRIS, 350, 400, 200, 25, "Back")
    myfont = pygame.font.SysFont('Lucida Console', 20)
    
    numeros, operaciones = numeros_y_operaciones()
    numero_objetivo = encontrar_numero_objetivo(numeros, operaciones)
    while numero_objetivo > 999 or numero_objetivo < 100:
        numeros, operaciones = numeros_y_operaciones()
        numero_objetivo = encontrar_numero_objetivo(numeros, operaciones)

    numeros.sort()

    total = str(numeros[0]) + "," + str(numeros[1]) + "," + str(numeros[2]) + "," + str(numeros[3]) + "," + str(numeros[4]) + "," + str(numeros[5]) + " --> " + str(numero_objetivo)
    labelNumbers = myfont.render(total, 1, BLANCO)
    input_box1 = c.InputBox(80, 300, 40, 32)  
    input_box2 = c.InputBox(120, 300, 40, 32)  
    input_box3 = c.InputBox(160, 300, 40, 32)  
    input_box4 = c.InputBox(200, 300, 40, 32)  
    input_box5 = c.InputBox(240, 300, 40, 32)  
    input_box6 = c.InputBox(280, 300, 40, 32)  
    input_box7 = c.InputBox(320, 300, 40, 32)
    input_box8 = c.InputBox(360, 300, 40, 32)
    input_box9 = c.InputBox(400, 300, 40, 32)
    input_box10 = c.InputBox(440, 300, 40, 32)
    input_box11 = c.InputBox(480, 300, 40, 32)
    
    while minijuego_s:
        
        menuBg = pygame.image.load("menuBg.png").convert_alpha()   # Fondo del menú
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.blit(menuBg, (0, 0)) 
        enterOkBtn.draw(screen, (0,0,0)) 
        enterBackBtn.draw(screen, (0,0,0))

        screen.blit(labelNumbers, (180, 270))  
        
        input_box1.draw(screen) 
        input_box2.draw(screen) 
        input_box3.draw(screen) 
        input_box4.draw(screen) 
        input_box5.draw(screen) 
        input_box6.draw(screen) 
        input_box7.draw(screen)
        input_box8.draw(screen) 
        input_box9.draw(screen) 
        input_box10.draw(screen) 
        input_box11.draw(screen) 
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box1.handle_event(event)
            input_box2.handle_event(event)
            input_box3.handle_event(event)
            input_box4.handle_event(event)
            input_box5.handle_event(event)
            input_box6.handle_event(event)
            input_box7.handle_event(event)
            input_box8.handle_event(event)
            input_box9.handle_event(event)
            input_box10.handle_event(event)
            input_box11.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:

                if enterOkBtn.isOver(pos):
                    numeros_str = [str(numeros[0]), str(numeros[1]), str(numeros[2]), str(numeros[3]), str(numeros[4]), str(numeros[5]) ]
                    if input_box1.text == "" and input_box3.text == "" and input_box5.text == "" and input_box7.text == "" and input_box9.text == "" and input_box11.text == "" :
                        changescn("msg", text="Follow the instructions", btnfnc="enterNumbers")
                    elif (input_box1.text or input_box3.text or input_box5.text or input_box7.text or input_box9.text or input_box11.text) not in numeros_str:
                        changescn("msg", text="Follow the instructions", btnfnc="enterNumbers")
                    elif (input_box2.text or input_box4.text or input_box6.text or input_box8.text or input_box10.text) not in ["+", "-", "*"]:
                        changescn("msg", text="Follow the instructions", btnfnc="enterNumbers")
                    else:
                        valor = input_box1.text + input_box2.text + input_box3.text + input_box4.text + input_box5.text + input_box6.text + input_box7.text + input_box8.text + input_box9.text + input_box10.text + input_box11.text
                        resultado = eval(str(valor))

                        if resultado == numero_objetivo:
                            principal()
                            changescn("mainLoop")
                    
                        elif resultado != numero_objetivo:
                            changescn("gameover")

                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                sys.exit()
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
                    
        pygame.display.flip()

def music() -> None:

    """ Esta realiza reproduce o para la música en la sección music del menú principal.
    Args:
        None
    Returns:
        None
    """

    global music_s
    
    ONBtn = c.button(GRIS, 200, 250, 200, 25, "ON")
    OFFBtn = c.button(GRIS, 200, 280, 200, 25, "OFF")
    backBtn = c.button(GRIS, 350, 400, 200, 25, "Back")
    myfont = pygame.font.SysFont('Lucida Console', 20)
    labelEnterMusic = myfont.render("Music:", 1, BLANCO)

    while music_s:
        
        menuBg = pygame.image.load("menuBg.png").convert_alpha()   # Fondo del menú
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.blit(menuBg, (0, 0)) 
        ONBtn.draw(screen, (0,0,0)) 
        OFFBtn.draw(screen, (0,0,0)) 
        backBtn.draw(screen, (0,0,0))
        screen.blit(labelEnterMusic, (200, 220)) 

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")

                if OFFBtn.isOver(pos):
                    playMusic("stop")

                if ONBtn.isOver(pos):
                    playMusic("main")
                    
            if event.type == pygame.QUIT:
                music_s = False
                sys.exit()
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")        
        
        pygame.display.flip()

def gameover() -> None:

    """ Esta función guarda la puntuación una vez hemos perdido la partida y la actualiza si es mayor que la 
        anterior asociada a ese mismo usuario.
    Args:
        None
    Returns:
        None
    """

    global gameover_s
    
    
    backBtn = c.button(GRIS, 350, 400, 200, 25, "Back")

    while gameover_s:
        
        screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        screen.fill(NEGRO)
        fuente2 = pygame.font.SysFont ('Lucida Console', 80) 
        f2_ancho, f2_alto = fuente2.size('GAME OVER') 
        print_text(screen, fuente2, (ANCHO_PANTALLA - f2_ancho)//2, (ALTO_PANTALLA - f2_alto)//2, 'GAME OVER', ROJO)
        backBtn.draw(screen, (0,0,0))

        if username in score_dict:
            if score_dict[username] < score:
                score_dict[username] = score
        else:
            score_dict[username] = score
        
        guardar_marcador(score_dict)
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if backBtn.isOver(pos):
                    changescn("menu")

            if event.type == pygame.QUIT:
                gameover_s = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")        
        
        pygame.display.flip()

def numeros_y_operaciones() -> list:

    """ Esta función genera los números y las operaciones a usar en el segundo juego.
    Args:
        None
    Returns:
        list: dos listas, una con 6 cifras(int) y otra con 5 caracteres de operaciones(str).
    """

    posibles_numeros = [1,2,3,4,5,6,7,8,9,10,25,50,75,100]
    numero_numeros = 6
    numeros = []

    while numero_numeros > 0:
        numeros.append(posibles_numeros[random.randint(0,len(posibles_numeros)-1)])
        posibles_numeros.remove(numeros[-1])
        numero_numeros -= 1

    posibles_operaciones = ["+", "-", "*"]
    numero_operaciones = 5
    operaciones = []

    while numero_operaciones > 0:
        operaciones.append(posibles_operaciones[random.randint(0,len(posibles_operaciones)-1)])
        numero_operaciones -= 1

    return numeros, operaciones

def encontrar_numero_objetivo(numeros:list, operaciones:list) -> int:

    """ Esta función genera el número objetivo del segundo juego.
    Args:
        numeros(list): 6 cifras
        operaciones(list): 5 operaciones
    Returns:
        int: el número objetivo
    """
    numero_objetivo_str = str(numeros[0])+str(operaciones[0])+str(numeros[1])+str(operaciones[1])+str(numeros[2])+str(operaciones[2])+str(numeros[3])+str(operaciones[3])+str(numeros[4])+str(operaciones[4])+str(numeros[5])
    numero_objetivo = eval(numero_objetivo_str)
    
    return numero_objetivo

def leer_marcador() -> dict:

    """ Esta función lee datos de un fichero binario: usuarios y puntuaciones.
    Args:
        None
    Returns:
        dict: score_dict (diccionario con las puntuaciones asociadas a cada usuario)
    """

    with open("score.obj", "rb") as fichero:
        score_dict = pickle.load(fichero)
        return score_dict

def guardar_marcador(score_dict:dict) -> None:

    """ Esta función guarda datos en un fichero binario: usuarios y puntuaciones.
    Args:
        score_dict(dict): diccionario con las puntuaciones asociadas a cada usuario
    Returns:
        None
    """

    with open("score.obj", "wb") as fichero:
        pickle.dump(score_dict, fichero)
