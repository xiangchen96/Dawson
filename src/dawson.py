import os
import pygame

here = os.path.dirname(os.path.abspath(__file__))
black_pawn = pygame.image.load(os.path.join(here, "../images/bpawn.png"))
white_pawn = pygame.image.load(os.path.join(here, "../images/wpawn.png"))
pawn_contour = pygame.image.load(os.path.join(here, "../images/contour.png"))

dark_brown = 102, 51, 0
clear_brown = 166, 127, 88

BLACK = -1
WHITE = 1
BLANK = 0


def move(m, i0, j0, i, j):
    color = m[i0][j0]
    m[i0][j0] = BLANK
    m[i][j] = color


def reset(m):
    width = len(m[0])
    m[0] = [BLACK]*width
    m[1] = [BLANK]*width
    m[2] = [WHITE]*width


def rect_possible_moves(m, turn):
    movs = possible_moves(m, turn)
    lista = []
    if turn == WHITE:
        for j in (x for (x, _) in movs):
            lista.append((2, j))
    else:
        for j in (x for (x, _) in movs):
            lista.append((0, j))
    return lista


def pass_turn(turn):
    if turn == BLACK:
        return WHITE
    else:
        return BLACK


def draw_state(screen, matrizPos, matrizRect, moves_rect):
    for i in range(3):
        for j in range(len(matrizPos[0])):
            if (i, j) in moves_rect:
                screen.blit(pawn_contour, (90*j, 90*i))
            elif (i+j) % 2 == 0:
                pygame.draw.rect(screen, dark_brown, matrizRect[i][j])
            else:
                pygame.draw.rect(screen, clear_brown, matrizRect[i][j])
            # pawns
            if matrizPos[i][j] == BLACK:
                screen.blit(black_pawn, (1+90*j, 90*i))
            elif matrizPos[i][j] == WHITE:
                screen.blit(white_pawn, (1+90*j, 90*i))


def possible_moves(m, turn):
    """
    Returns a list with (col_ini, col_dest)
    """
    movs = []
    if turn == WHITE:
        middle_black_list = filter(lambda j: m[1][j] == BLACK, range(len(m[0])))
        # mandatory moves
        for j in middle_black_list:
            if j-1 >= 0 and m[2][j-1] == WHITE:
                movs.append((j-1, j))
            if j+1 < len(m[0]) and m[2][j+1] == WHITE:
                movs.append((j+1, j))
        if not movs:
            for j in range(len(m[0])):
                if m[2][j] == turn and m[1][j] == BLANK:
                    movs.append((j, j))
    else:
        listaColBlancoEnMedio = filter(lambda j: m[1][j] == WHITE, range(len(m[0])))
        for j in listaColBlancoEnMedio:
            if j-1 >= 0 and m[0][j-1] == BLACK:
                movs.append((j-1, j))
            if j+1 < len(m[0]) and m[0][j+1] == BLACK:
                movs.append((j+1, j))
        # no hay obligatorios
        if not movs:
            for j in range(len(m[0])):
                if m[0][j] == BLACK and m[1][j] == BLANK:
                    movs.append((j, j))
    return movs
