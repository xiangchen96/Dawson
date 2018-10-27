import pygame
import time
from dawson import Dawson

pygame.init()
width = int(input('Introduce the number of columns: '))

# game = Dawson(width, 'EvP')
# game = Dawson(width, 'PvP')
game = Dawson(width, 'PvE')
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            game.process_click(pos)

quit()
