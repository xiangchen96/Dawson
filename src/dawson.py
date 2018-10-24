import os
import pygame
from functools import lru_cache

here = os.path.dirname(os.path.abspath(__file__))
black_pawn = pygame.image.load(os.path.join(here, "../images/bpawn.png"))
white_pawn = pygame.image.load(os.path.join(here, "../images/wpawn.png"))
pawn_contour = pygame.image.load(os.path.join(here, "../images/contour.png"))

dark_brown = 102, 51, 0
clear_brown = 166, 127, 88

BLACK = -1
WHITE = 1
BLANK = 0


class Dawson:
    def __init__(self):
        width = int(input('Introduce the number of columns: '))
        self.width = width
        self.board_state = [[0]*width]*3
        self.screen = pygame.display.set_mode((90*width, 300))
        self.font = pygame.font.SysFont("monospace", 20)
        self.rect_container = [[0]*self.width for _ in range(3)]
        for i in range(3):
            for j in range(width):
                self.rect_container[i][j] = pygame.Rect((90*j), (90*i), 90, 90)
        self.reset()

    def reset(self):
        self.board_state[0] = [BLACK]*self.width
        self.board_state[1] = [BLANK]*self.width
        self.board_state[2] = [WHITE]*self.width
        self.turn = WHITE
        self.finished = False
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0, 270, 900, 30))
        self.draw_state()

    def move(self, i, j, new_i, new_j):
        color = self.board_state[i][j]
        self.board_state[i][j] = BLANK
        self.board_state[new_i][new_j] = color

    def rect_possible_moves(self):
        movs = self.possible_moves()
        lista = []
        if self.turn == WHITE:
            for j in (x for (x, _) in movs):
                lista.append((2, j))
        else:
            for j in (x for (x, _) in movs):
                lista.append((0, j))
        return lista

    def pass_turn(self):
        self.turn = BLACK if self.turn == WHITE else WHITE

    def get_winner(self):
        return "BLACK" if self.turn == WHITE else "WHITE"

    def possible_moves(self):
        """
        Returns a list with (origin_col, next_col)
        """
        movs = []
        m = self.board_state
        if self.turn == WHITE:
            center_row_blacks = (j for j in range(self.width) if m[1][j] == BLACK)
            # mandatory moves
            for j in center_row_blacks:
                if j-1 >= 0 and m[2][j-1] == WHITE:
                    movs.append((j-1, j))
                if j+1 < len(m[0]) and m[2][j+1] == WHITE:
                    movs.append((j+1, j))
            if not movs:
                for j in range(self.width):
                    if m[2][j] == WHITE and m[1][j] == BLANK:
                        movs.append((j, j))
        else:
            center_row_whites = (j for j in range(self.width) if m[1][j] == WHITE)
            for j in center_row_whites:
                if j-1 >= 0 and m[0][j-1] == BLACK:
                    movs.append((j-1, j))
                if j+1 < len(m[0]) and m[0][j+1] == BLACK:
                    movs.append((j+1, j))
            if not movs:
                for j in range(self.width):
                    if m[0][j] == BLACK and m[1][j] == BLANK:
                        movs.append((j, j))
        return movs

    def draw_state(self):
        for i in range(3):
            for j in range(self.width):
                if (i+j) % 2 == 0:
                    pygame.draw.rect(self.screen, dark_brown, self.rect_container[i][j])
                else:
                    pygame.draw.rect(self.screen, clear_brown, self.rect_container[i][j])
                if (i, j) in self.rect_possible_moves():
                    self.screen.blit(pawn_contour, (90*j, 90*i))
                # pawns
                if self.board_state[i][j] == BLACK:
                    self.screen.blit(black_pawn, (1+90*j, 90*i))
                elif self.board_state[i][j] == WHITE:
                    self.screen.blit(white_pawn, (1+90*j, 90*i))

    def draw_winner_label(self):
        label = self.font.render(self.get_winner()+" WINS", 1, (255, 255, 0))
        self.screen.blit(label, (90*self.width/2, 273))

    def process_click(self, pos):
        for i in range(3):
            for j in range(self.width):
                if self.rect_container[i][j].collidepoint(pos) and self.board_state[i][j] == self.turn:
                    movs = self.possible_moves()
                    if j in [x for (x, _) in movs]:
                        aux = 0
                        for (a, b) in movs:
                            if a == j:
                                break
                            else:
                                aux += 1
                        col, new_col = movs[aux]
                        self.move(i, j, 1, new_col)
                        self.pass_turn()
                        if not self.possible_moves():
                            self.finished = True
                            self.draw_winner_label()


def digital_sum(L):
    suma = 0
    for i in L:
        suma ^= i
    return suma


def mex(L):
    L = set(L)
    n = 0
    while n in L:
        n += 1
    return n


def sgDawson(L):
    return digital_sum((gDawson(i) for i in L))


def to_binary(decimal):
    return list(int(i) for i in bin(decimal)[2:])


def successors(n):
    if n < 1:
        return []
    if n == 1:
        return [[0]]
    lista = []
    lista.append([n-2])
    if n >= 3:
        lista.append([n-3])
        j = n-3
        for i in range(1, int((j/2))+1):
            lista.append([i, j-i])
    return lista


@lru_cache(maxsize=None)
def gDawson(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    listaMex = []
    for i in successors(n):
        if len(i) == 1:
            listaMex.append(gDawson(i[0]))
        else:
            listaMex.append(gDawson(i[0]) ^ gDawson(i[1]))
    return mex(listaMex)


def apnim(posN, i=0):
    suma = digital_sum(posN)
    if suma:
        bina, found = len(to_binary(suma)), False
        while not found:
            sumando = to_binary(posN[i])
            if len(sumando) < bina or sumando[-bina] == 0:
                i += 1
            else:
                found = True
        return digital_sum([suma, posN[i]]), i
    else:
        return


def calcMovDawson(L):
    # CASOS BASE
    if sgDawson(L) == 0:
        return "Es P"
    if len(L) == 1 and L[0] == 1:
        return []
    result = L[:]
    valPilas = list(map(gDawson, L))
    gBuscado, indpilaCambiar = apnim(valPilas)
    pila = L[indpilaCambiar]
    if pila >= 2 and gDawson(pila-2) == gBuscado:
        result[indpilaCambiar] = pila-2
        result = [a for a in result if a != 0]
        return result
    for i in successors(pila):
        if len(i) == 1 and sgDawson(i) == gBuscado:
            result[indpilaCambiar] = i[0]
            result = [a for a in result if a != 0]
            return result
        else:
            if sgDawson(i) == gBuscado:
                result[indpilaCambiar] = i[0]
                result.insert(indpilaCambiar+1, i[1])
                result = [a for a in result if a != 0]
                return result
