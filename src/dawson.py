import os
import pygame
import time
import random
from functools import lru_cache

here = os.path.dirname(os.path.abspath(__file__))
black_pawn = pygame.image.load(os.path.join(here, "../images/bpawn.png"))
white_pawn = pygame.image.load(os.path.join(here, "../images/wpawn.png"))
pawn_contour = pygame.image.load(os.path.join(here, "../images/contour.png"))

DARK_BROWN = 102, 51, 0
CLEAR_BROWN = 166, 127, 88

BLACK = -1
WHITE = 1
BLANK = 0


class Dawson:
    def __init__(self, width=5, mode='PvP'):
        self.width = width
        self.board_state = [[0]*width for _ in range(3)]
        self.rect_container = [[0]*width for _ in range(3)]
        self.screen = pygame.display.set_mode((90*width, 300))
        self.font = pygame.font.SysFont("monospace", 20)
        self.mode = mode
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
        self.screen.fill((0, 0, 0))  # hide winner
        self.draw_state()
        if self.mode == 'EvP':
            self.move_IA()

    def move(self, i, j, new_i, new_j):
        color = self.board_state[i][j]
        self.board_state[i][j] = BLANK
        self.board_state[new_i][new_j] = color
        self.pass_turn()
        self.draw_state()

    def possible_moves_coords(self):
        start_row = 0 if self.turn == BLACK else 2
        for col in (mov[0] for mov in self.possible_moves()):
            yield (start_row, col)

    def pass_turn(self):
        self.turn = BLACK if self.turn == WHITE else WHITE

    def get_winner_name(self):
        return "BLACK" if self.turn == WHITE else "WHITE"

    def possible_moves(self):
        """
        Returns a list with (origin_col, next_col)
        """
        movs = []
        m = self.board_state
        start_row = 0 if self.turn == BLACK else 2
        opponent = WHITE if self.turn == BLACK else BLACK
        middle_row_opponents = (col for col in range(self.width) if m[1][col] == opponent)
        for j in middle_row_opponents:
            if j-1 >= 0 and m[start_row][j-1] == self.turn:
                movs.append((j-1, j))
            if j+1 < self.width and m[start_row][j+1] == self.turn:
                movs.append((j+1, j))
        if not movs:
            for j in range(self.width):
                if m[start_row][j] == self.turn and m[1][j] == BLANK:
                    movs.append((j, j))
        return movs

    def draw_state(self):
        for i in range(3):
            for j in range(self.width):
                square_color = DARK_BROWN if (i+j) % 2 == 0 else CLEAR_BROWN
                pygame.draw.rect(self.screen, square_color, self.rect_container[i][j])
                if (i, j) in self.possible_moves_coords():
                    self.screen.blit(pawn_contour, (90*j, 90*i))
                if self.board_state[i][j] == BLACK:
                    self.screen.blit(black_pawn, (1+90*j, 90*i))
                elif self.board_state[i][j] == WHITE:
                    self.screen.blit(white_pawn, (1+90*j, 90*i))
        pygame.display.flip()

    def check_winner(self):
        if not self.possible_moves():
            self.finished = True
            label = self.font.render(self.get_winner_name()+" WINS", 1, (255, 255, 0))
            self.screen.blit(label, (90*self.width/2, 273))
            pygame.display.flip()

    def move_IA(self):
        time.sleep(.4)
        if not make_required_move(self.board_state, self.turn):
            listaBuscada = get_best_move(self.board_state)
            print("Le paso a Dawson", board_state_to_list(self.board_state))
            movs = self.possible_moves()
            random.shuffle(movs)
            start_row = 2 if self.turn == WHITE else 0
            for (j0, j) in movs:
                copiaMatrizPos = [a[:] for a in self.board_state]
                copiaMatrizPos[start_row][j0] = BLANK
                copiaMatrizPos[1][j] = self.turn
                next_turn = WHITE if self.turn == BLACK else BLACK
                make_all_required_moves(copiaMatrizPos, next_turn)
                if not listaBuscada or listaBuscada == board_state_to_list(copiaMatrizPos):
                    self.move(start_row, j0, 1, j)
                    self.check_winner()
                    break
        else:
            self.pass_turn()
            self.draw_state()
            self.check_winner()

    def process_click(self, pos):
        if self.finished:
            self.reset()
            return
        for i in range(3):
            for j in range(self.width):
                if self.rect_container[i][j].collidepoint(pos):
                    if self.board_state[i][j] == self.turn:
                        movs = self.possible_moves()
                        for (col, new_col) in (mov for mov in movs if mov[0] == j):
                            self.move(i, j, 1, new_col)
                            self.check_winner()
                            if self.mode in ['PvE', 'EvP']:
                                self.move_IA()
                            return True
                    return False


def reduce_xor(L):
    suma = 0
    for i in L:
        suma ^= i
    return suma


def mex(L):
    """Return the minimum excluded value of a list"""
    L = set(L)
    n = 0
    while n in L:
        n += 1
    return n


def successors(n):
    if n == 0:
        return []
    if n == 1:
        return [(0,)]
    successors_list = [(n-2,)]
    if n >= 3:
        successors_list.append((n-3,))
        j = n-3
        for i in range(1, int((j/2))+1):
            successors_list.append((i, j-i))
    return successors_list


@lru_cache(maxsize=None)
def gDawson(n):
    """Return the G-value of a single Dawson game"""
    if n == 0:
        return 0
    if n == 1:
        return 1
    successors_g = []
    for next_state in successors(n):
        if len(next_state) == 1:
            successors_g.append(gDawson(next_state[0]))
        else:
            successors_g.append(gDawson(next_state[0]) ^ gDawson(next_state[1]))
    return mex(successors_g)


def sgDawson(L):
    """Return the G-value of the sum of multiple Dawson games"""
    return reduce_xor((gDawson(i) for i in L))


def to_binary(decimal):
    return [int(i) for i in bin(decimal)[2:]]


def make_required_move(M, turn):
    opponent = BLACK if turn == WHITE else WHITE
    start_row = 0 if turn == BLACK else 2
    middle_row_opponents = (j for j in range(len(M[0])) if M[1][j] == opponent)
    for j in middle_row_opponents:
        if j-1 >= 0 and M[start_row][j-1] == turn:
            M[start_row][j-1] = BLANK
            M[1][j] = turn
            return True
        if j+1 < len(M[0]) and M[start_row][j+1] == turn:
            M[start_row][j+1] = BLANK
            M[1][j] = turn
            return True
    return False


def make_all_required_moves(M, turn):
    while make_required_move(M, turn):
        next_turn = BLACK if turn == WHITE else WHITE
        if not make_required_move(M, next_turn):
            break


def get_best_move(M):
    L = board_state_to_list(M)
    if sgDawson(L) == 0:
        return None
    if L == [1]:
        return []
    result = L[:]
    valPilas = [gDawson(i) for i in L]
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


def board_state_to_list(M):
    result = []
    counter = 0
    for j in range(len(M[0])):
        if M[0][j] == BLACK and M[1][j] == BLANK and M[2][j] == WHITE:
            counter += 1
        else:
            if counter != 0:
                result.append(counter)
            counter = 0
    if counter != 0:  # last pile
        result.append(counter)
    return result


def apnim(posN, i=0):
    suma = reduce_xor(posN)
    bina, found = len(to_binary(suma)), False
    while not found:
        sumando = to_binary(posN[i])
        if len(sumando) < bina or sumando[-bina] == 0:
            i += 1
        else:
            found = True
    return reduce_xor([suma, posN[i]]), i
