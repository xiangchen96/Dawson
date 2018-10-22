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


def possible_moves(m, turn):
    "Returns a list with (col_ini, col_dest)"
    movs = []
    if turn == WHITE:
        middle_black_list = filter(lambda j: m[1][j] == BLACK, range(len(m[0])))
        for j in middle_black_list:
            if j-1 >= 0 and m[2][j-1] == turn:
                movs.append((j-1, j))
            if j+1 <= 9 and m[2][j+1] == turn:
                movs.append((j+1, j))
        # no hay obligatorios
        if not movs:
            for j in range(len(m[0])):
                if m[2][j] == turn and m[1][j] == BLANK:
                    movs.append((j, j))
    else:
        listaColBlancoEnMedio = filter(lambda j: m[1][j] == WHITE, range(len(m[0])))
        for j in listaColBlancoEnMedio:
            if j-1 >= 0 and m[0][j-1] == turn:
                movs.append((j-1, j))
            if j+1 <= 9 and m[0][j+1] == turn:
                movs.append((j+1, j))
        # no hay obligatorios
        if not movs:
            for j in range(10):
                if m[0][j] == turn and m[1][j] == BLANK:
                    movs.append((j, j))
    return movs
