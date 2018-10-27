import os
import pygame
import time
import random
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
    def __init__(self, width=5):
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
        # hide winner
        self.screen.fill((0, 0, 0))
        self.draw_state()

    def move(self, i, j, new_i, new_j):
        color = self.board_state[i][j]
        self.board_state[i][j] = BLANK
        self.board_state[new_i][new_j] = color
        self.pass_turn()

    def rect_possible_moves(self):
        movs = self.possible_moves()
        start_row = 0 if self.turn == BLACK else 2
        for col in (mov[0] for mov in movs):
            yield (start_row, col)

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
                square_color = dark_brown if (i+j) % 2 == 0 else clear_brown
                pygame.draw.rect(self.screen, square_color, self.rect_container[i][j])
                if (i, j) in self.rect_possible_moves():
                    self.screen.blit(pawn_contour, (90*j, 90*i))
                if self.board_state[i][j] == BLACK:
                    self.screen.blit(black_pawn, (1+90*j, 90*i))
                elif self.board_state[i][j] == WHITE:
                    self.screen.blit(white_pawn, (1+90*j, 90*i))
        pygame.display.flip()

    def check_winner(self):
        if not self.possible_moves():
            self.finished = True
            label = self.font.render(self.get_winner()+" WINS", 1, (255, 255, 0))
            self.screen.blit(label, (90*self.width/2, 273))

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
                            self.draw_state()
                    return


def reduce_with_xor(L):
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
    return reduce_with_xor((gDawson(i) for i in L))


def to_binary(decimal):
    return [int(i) for i in bin(decimal)[2:]]
