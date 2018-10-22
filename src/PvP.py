import pygame
import time
import dawson
"""
Dawson's chess
Remove 1 -> move an isolated pawn
Remove 2 -> move an outer pawn
Remove 3 and not divide -> move a pawn that is next to an outer pawn
Remove 3 and divide -> move any other pawn
"""

pygame.init()
screen = pygame.display.set_mode((900, 300))

myfont = pygame.font.SysFont("monospace", 20)
running = 1
turn = dawson.WHITE

WIDTH = 10
matrizPos = [[0]*WIDTH] * 3
matrizRect = [["PLACEHOLDER"]*WIDTH for i in range(3)]


def listaRectMovPosibles():
    movs = dawson.possible_moves(matrizPos, turn)
    lista = []
    if turn == dawson.WHITE:
        for j in [x for (x, _) in movs]:
            lista.append((2, j))
    else:
        for j in [x for (x, _) in movs]:
            lista.append((0, j))
    return lista


dawson.reset(matrizPos)
# pinto tablero y fichas iniciales
for i in range(3):
    for j in range(10):
        matrizRect[i][j] = pygame.Rect((90*j), (90*i), 90, 90)
        if (i+j) % 2 == 0:
            pygame.draw.rect(screen, dawson.dark_brown, matrizRect[i][j])
        else:
            pygame.draw.rect(screen, dawson.clear_brown, matrizRect[i][j])

partidaTerminada = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if partidaTerminada:
                dawson.reset(matrizPos)
                turn = dawson.WHITE
                partidaTerminada = False
                # tapo "GANAN BLANCAS"
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 270, 900, 30))
            else:
                pos = pygame.mouse.get_pos()
                for i in range(3):
                    for j in range(10):
                        if matrizRect[i][j].collidepoint(pos) and matrizPos[i][j] == turn:
                            movs = dawson.possible_moves(matrizPos, turn)
                            if j in [x for (x, _) in movs]:
                                aux = 0
                                for (a, b) in movs:
                                    if a == j:
                                        break
                                    else:
                                        aux += 1
                                col, nuevaCol = movs[aux]
                                dawson.move(matrizPos, i, j, 1, nuevaCol)
                                if turn == dawson.WHITE:
                                    turn = dawson.BLACK
                                    if not dawson.possible_moves(matrizPos, turn):
                                        partidaTerminada = True
                                        label = myfont.render("GANAN BLANCAS", 1, (255, 255, 0))
                                        screen.blit(label, (390, 273))
                                else:
                                    turn = dawson.WHITE
                                    if not dawson.possible_moves(matrizPos, turn):
                                        partidaTerminada = True
                                        label = myfont.render("GANAN NEGRAS", 1, (255, 255, 0))
                                        screen.blit(label, (390, 273))
    listaRectMov = listaRectMovPosibles()
    for i in range(3):
        for j in range(10):
            # recuadros
            if (i, j) in listaRectMov:
                screen.blit(dawson.pawn_contour, (90*j, 90*i))
            elif (i+j) % 2 == 0:
                pygame.draw.rect(screen, dawson.dark_brown, matrizRect[i][j])
            else:
                pygame.draw.rect(screen, dawson.clear_brown, matrizRect[i][j])
            # peones
            if matrizPos[i][j] == dawson.BLACK:
                screen.blit(dawson.black_pawn, (1+90*j, 90*i))
            elif matrizPos[i][j] == dawson.WHITE:
                screen.blit(dawson.white_pawn, (1+90*j, 90*i))
    pygame.display.flip()

quit()
